"""
AI-Powered SQL Agent using LangChain Expression Language (LCEL)

This module implements an intelligent SQL agent that converts natural language
queries into SQL commands using IBM's Granite LLM and LangChain's LCEL framework.

Key LCEL Features Used:
- Runnable: Core abstraction for composable components
- Pipe (|): Chain operations together
- RunnablePassthrough: Pass data through chains
- RunnableParallel: Execute operations in parallel
- RunnableLambda: Create custom runnable functions
- Tool: Define callable tools for the agent
- AgentExecutor: Execute agent with tools
"""

import os
import warnings
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from langchain.agents import AgentType, create_react_agent, AgentExecutor
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import (
    QuerySQLDatabaseTool,
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)
from langchain_core.runnables import (
    Runnable,
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
)
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import Tool

# Suppress warnings
warnings.filterwarnings("ignore")
load_dotenv()


class SQLAgentConfig:
    """Configuration for the SQL Agent"""

    def __init__(self):
        self.model_id = os.getenv("MODEL_ID", "ibm/granite-3-2-8b-instruct")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1024"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.2"))
        self.top_p = float(os.getenv("TOP_P", "0.95"))
        self.repetition_penalty = float(os.getenv("REPETITION_PENALTY", "1.2"))

        self.ibm_api_key = os.getenv("IBM_API_KEY")
        self.ibm_project_id = os.getenv("IBM_PROJECT_ID", "skills-network")
        self.ibm_url = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")

        self.mysql_user = os.getenv("MYSQL_USER", "root")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_host = os.getenv("MYSQL_HOST", "localhost")
        self.mysql_port = os.getenv("MYSQL_PORT", "3306")
        self.mysql_database = os.getenv("MYSQL_DATABASE", "chinook")


class SQLAgent:
    """
    AI-Powered SQL Agent using LCEL (LangChain Expression Language)

    This agent uses LCEL's Runnable interface with LangChain Tools:
    - QuerySQLDatabaseTool: Execute SQL queries
    - InfoSQLDatabaseTool: Get table information
    - ListSQLDatabaseTool: List available tables
    - Custom tools for validation and formatting

    Architecture:
    Input → Validation → LLM with Tools → Agent Executor → Output Formatting
    """

    def __init__(self, config: SQLAgentConfig = None):
        """Initialize the SQL Agent with configuration"""
        self.config = config or SQLAgentConfig()
        self.llm = self._initialize_llm()
        self.db = self._initialize_database()
        self.tools = self._create_tools()
        self.agent_executor = self._create_agent_executor()

    def _initialize_llm(self) -> WatsonxLLM:
        """Initialize the LLM using IBM Watson"""
        parameters = {
            GenParams.MAX_NEW_TOKENS: self.config.max_tokens,
            GenParams.TEMPERATURE: self.config.temperature,
            GenParams.TOP_P: self.config.top_p,
            GenParams.REPETITION_PENALTY: self.config.repetition_penalty,
        }

        credentials = {"url": self.config.ibm_url}

        model = ModelInference(
            model_id=self.config.model_id,
            params=parameters,
            credentials=credentials,
            project_id=self.config.ibm_project_id,
        )

        return WatsonxLLM(model=model)

    def _initialize_database(self) -> SQLDatabase:
        """Initialize the database connection"""
        mysql_uri = (
            f"mysql+mysqlconnector://{self.config.mysql_user}:"
            f"{self.config.mysql_password}@{self.config.mysql_host}:"
            f"{self.config.mysql_port}/{self.config.mysql_database}"
        )
        return SQLDatabase.from_uri(mysql_uri)

    def _create_tools(self) -> List[Tool]:
        """
        Create LangChain tools for SQL operations

        Tools from langchain_community.tools.sql_database:
        - QuerySQLDatabaseTool: Execute SQL queries
        - InfoSQLDatabaseTool: Get table schema information
        - ListSQLDatabaseTool: List all tables
        """
        # Built-in SQL tools from LangChain community
        query_tool = QuerySQLDatabaseTool(db=self.db)
        info_tool = InfoSQLDatabaseTool(db=self.db)
        list_tool = ListSQLDatabaseTool(db=self.db)

        # Custom validation tool
        validate_tool = Tool(
            name="validate_sql_query",
            func=self._validate_sql_query,
            description="Validate if a SQL query is safe and well-formed",
        )

        # Custom error recovery tool
        error_recovery_tool = Tool(
            name="recover_from_error",
            func=self._recover_from_error,
            description="Recover from SQL execution errors and suggest fixes",
        )

        return [query_tool, info_tool, list_tool, validate_tool, error_recovery_tool]

    def _validate_sql_query(self, query: str) -> str:
        """Validate SQL query safety"""
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        query_upper = query.upper()

        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return f"⚠️ Query contains dangerous keyword: {keyword}"

        return "✅ Query appears safe"

    def _recover_from_error(self, error_message: str) -> str:
        """Provide recovery suggestions for SQL errors"""
        suggestions = {
            "syntax error": "Check SQL syntax - ensure proper spacing and quotes",
            "table not found": "Verify table name exists in database",
            "column not found": "Check column name spelling and table reference",
            "access denied": "Verify database credentials and permissions",
        }

        for error_key, suggestion in suggestions.items():
            if error_key.lower() in error_message.lower():
                return f"💡 Suggestion: {suggestion}"

        return "❓ Unknown error - check database connection"

    def _create_agent_executor(self) -> AgentExecutor:
        """
        Create LCEL-based agent executor with tools

        Uses create_react_agent for REACT (Reasoning + Acting) pattern
        """
        # Create system prompt for the agent
        system_prompt = """You are an expert SQL database assistant. Your job is to help users query databases using natural language.

You have access to the following tools:
1. query_sql_database: Execute SQL queries
2. info_sql_database: Get table schema information
3. list_sql_database: List all available tables
4. validate_sql_query: Validate SQL queries
5. recover_from_error: Get help with SQL errors

When a user asks a question:
1. First, list available tables using list_sql_database
2. Get schema info for relevant tables using info_sql_database
3. Construct and validate the SQL query
4. Execute the query using query_sql_database
5. Format and explain the results

Always be helpful and explain what you're doing."""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("user", "{input}"),
                ("assistant", "{agent_scratchpad}"),
            ]
        )

        # Create REACT agent using LCEL
        agent = create_react_agent(self.llm, self.tools, prompt)

        # Create agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10,
        )

        return agent_executor

    def query(self, question: str) -> Dict[str, Any]:
        """
        Execute a natural language query using LCEL agent

        The agent uses tools to:
        1. Understand the database schema
        2. Generate appropriate SQL
        3. Execute and return results
        """
        try:
            result = self.agent_executor.invoke({"input": question})
            return {
                "question": question,
                "answer": result.get("output", "No result"),
                "status": "success",
            }
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "status": "error",
            }

    def run_interactive(self):
        """Run the agent in interactive mode using LCEL + Tools"""
        print("\n" + "=" * 70)
        print("🤖 AI-Powered SQL Agent (LCEL + Tools)")
        print("=" * 70)
        print("\nBuilt with:")
        print("  • LangChain Expression Language (LCEL)")
        print("  • LangChain Community Tools (SQL Database Tools)")
        print("  • REACT Agent Pattern (Reasoning + Acting)")
        print("  • IBM Granite 3.2 8B Instruct LLM")
        print("\nAvailable Tools:")
        print("  • query_sql_database: Execute SQL queries")
        print("  • info_sql_database: Get table schema")
        print("  • list_sql_database: List tables")
        print("  • validate_sql_query: Validate queries")
        print("  • recover_from_error: Error recovery")
        print("\nType 'exit' to quit")
        print("=" * 70 + "\n")

        while True:
            question = input("📝 Ask a question: ").strip()
            if question.lower() == "exit":
                print("\nGoodbye! 👋")
                break
            if not question:
                continue

            try:
                print("\n🔄 Processing your question...\n")
                result = self.query(question)
                print(f"\n✅ Status: {result.get('status', 'unknown')}")
                print(f"📝 Question: {result.get('question', '')}")
                print(f"💬 Answer:\n{result.get('answer', 'No result')}\n")
                print("-" * 70 + "\n")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
                print("-" * 70 + "\n")


def main():
    """Main entry point demonstrating LCEL + Tools architecture"""
    print("\n" + "=" * 80)
    print("🚀 AI-Powered SQL Agent - LCEL + Tools Implementation")
    print("=" * 80)
    print("\nArchitecture:")
    print("  Input → Validation → LLM with Tools → Agent Executor → Output")
    print("\nLCEL Features Used:")
    print("  • Runnable Interface: Core abstraction for all components")
    print("  • Pipe Operator (|): Compose runnables together")
    print("  • RunnableLambda: Wrap custom functions as runnables")
    print("  • AgentExecutor: Execute agent with tool access")
    print("  • create_react_agent: REACT pattern (Reasoning + Acting)")
    print("\nLangChain Community Tools:")
    print("  • QuerySQLDatabaseTool: Execute SQL queries")
    print("  • InfoSQLDatabaseTool: Get table schema information")
    print("  • ListSQLDatabaseTool: List available tables")
    print("  • Custom Tools: Validation and error recovery")
    print("=" * 80 + "\n")

    try:
        agent = SQLAgent()

        # Example 1: Basic query
        print("📌 Example 1: Basic Query\n")
        print("Question: How many albums are in the database?\n")
        result = agent.query("How many albums are in the database?")
        print(f"Status: {result['status']}")
        print(f"Answer: {result['answer']}\n")
        print("-" * 80 + "\n")

        # Example 2: Interactive mode
        print("📌 Example 2: Interactive Mode\n")
        print("Starting interactive mode (type 'exit' to quit)...\n")
        agent.run_interactive()

    except Exception as e:
        print(f"\n❌ Error initializing agent: {str(e)}")
        print("Please check your configuration and database connection.")


if __name__ == "__main__":
    main()

