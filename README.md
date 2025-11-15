# 🤖 AI-Powered SQL Agent

> Transform natural language questions into SQL queries with the power of AI. No SQL expertise required.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-green.svg)](https://python.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

The **AI-Powered SQL Agent** is an intelligent system that bridges the gap between natural language and database queries. Using advanced LLM capabilities and **LangChain's Expression Language (LCEL)**, this agent enables anyone to query databases using everyday language—no SQL knowledge needed.

### Key Features

- 🗣️ **Natural Language Processing**: Ask questions in plain English
- 🔄 **Intelligent Query Generation**: Automatically converts NLQ to SQL
- 🛡️ **Error Recovery**: Handles and corrects SQL errors automatically
- 📊 **Multi-Query Support**: Executes complex queries across multiple tables
- ⚡ **Token Efficient**: Optimized schema retrieval for better performance
- 🔗 **LCEL Architecture**: Built on LangChain's modern expression language

### LCEL + Tools Architecture

This project demonstrates advanced LCEL capabilities with LangChain Community Tools:

**LCEL Features:**
- **Runnable Interface**: Core abstraction for all composable components
- **Pipe Operator (|)**: Chain operations together seamlessly
- **RunnableLambda**: Wrap custom functions as runnables
- **AgentExecutor**: Execute agents with tool access
- **create_react_agent**: REACT pattern (Reasoning + Acting)
- **invoke()**: Execute the complete chain
- **stream()**: Real-time response streaming

**LangChain Community Tools:**
- **QuerySQLDatabaseTool**: Execute SQL queries on database
- **InfoSQLDatabaseTool**: Get table schema and structure information
- **ListSQLDatabaseTool**: List all available tables in database
- **Custom Tools**: Validation and error recovery tools

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- MySQL Server
- IBM Watson API credentials (for LLM)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/altugyerli/Ai-powerred-sql-agent.git
cd Ai-powerred-sql-agent
```

2. **Create virtual environment**
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# IBM Watson Credentials
IBM_API_KEY=your_api_key_here
IBM_PROJECT_ID=your_project_id

# MySQL Configuration
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=chinook
```

## 📖 Usage

### Basic Example with LCEL + Tools

```python
from sql_agent import SQLAgent

# Initialize the agent (builds LCEL + Tools internally)
agent = SQLAgent()

# The agent automatically has access to:
# - QuerySQLDatabaseTool: Execute SQL queries
# - InfoSQLDatabaseTool: Get table schema
# - ListSQLDatabaseTool: List tables
# - validate_sql_query: Validate queries
# - recover_from_error: Error recovery

# Execute query using LCEL agent
result = agent.query("How many albums are in the database?")
print(result)
# Output: {
#   'question': 'How many albums are in the database?',
#   'answer': 'There are 347 albums in the database.',
#   'status': 'success'
# }
```

### LCEL Runnable Interface Methods

```python
from sql_agent import SQLAgent

agent = SQLAgent()

# Method 1: invoke() - Synchronous execution
result = agent.query("How many albums?")
print(result)

# Method 2: stream() - Real-time streaming with tools
for chunk in agent.agent_executor.stream({"input": "How many albums?"}):
    print(chunk, end="", flush=True)

# Method 3: batch() - Process multiple queries
questions = [
    {"input": "How many albums?"},
    {"input": "How many artists?"},
    {"input": "How many customers?"}
]
results = agent.agent_executor.batch(questions)
for result in results:
    print(result)
```

### Advanced Queries

```python
# Complex multi-table queries
agent.query("Show me the top 5 artists by total sales")

# Aggregations and filtering
agent.query("Which customers spent more than $50?")

# Table descriptions
agent.query("Describe the structure of the PlaylistTrack table")
```

### Interactive Mode (LCEL + Tools)

```python
from sql_agent import SQLAgent

agent = SQLAgent()
agent.run_interactive()  # Uses LCEL + Tools internally
```

**Interactive Session Output:**
```
======================================================================
🤖 AI-Powered SQL Agent (LCEL + Tools)
======================================================================

Built with:
  • LangChain Expression Language (LCEL)
  • LangChain Community Tools (SQL Database Tools)
  • REACT Agent Pattern (Reasoning + Acting)
  • IBM Granite 3.2 8B Instruct LLM

Available Tools:
  • query_sql_database: Execute SQL queries
  • info_sql_database: Get table schema
  • list_sql_database: List tables
  • validate_sql_query: Validate queries
  • recover_from_error: Error recovery

Type 'exit' to quit
======================================================================

📝 Ask a question: How many customers are there?

🔄 Processing your question...

✅ Status: success
📝 Question: How many customers are there?
💬 Answer:
There are 59 customers in the database.
```

## 🏗️ Architecture

### LCEL + Tools-Based Design

This project leverages **LangChain Expression Language (LCEL)** with **LangChain Community Tools**:

- **Runnable Interface**: All components implement the Runnable abstraction
- **Tool Integration**: Use LangChain's built-in SQL database tools
- **REACT Agent**: Reasoning + Acting pattern for intelligent decision making
- **Type Safety**: Full type hints throughout
- **Streaming Support**: Real-time response streaming with `.stream()`
- **Error Handling**: Comprehensive error recovery mechanisms

### LCEL + Tools Architecture

```
User Query (Natural Language)
    ↓
[LLM with Tool Access]
    ├─→ QuerySQLDatabaseTool (Execute SQL)
    ├─→ InfoSQLDatabaseTool (Get Schema)
    ├─→ ListSQLDatabaseTool (List Tables)
    ├─→ validate_sql_query (Custom Tool)
    └─→ recover_from_error (Custom Tool)
    ↓
[REACT Agent Loop]
    • Reason about the question
    • Select appropriate tool
    • Execute tool
    • Observe results
    • Repeat until answer found
    ↓
Formatted Response
```

### Tool-Based Execution Flow

```python
# Create tools from LangChain community
tools = [
    QuerySQLDatabaseTool(db=db),      # Execute queries
    InfoSQLDatabaseTool(db=db),       # Get table info
    ListSQLDatabaseTool(db=db),       # List tables
    validate_sql_query,               # Custom validation
    recover_from_error,               # Custom recovery
]

# Create REACT agent with tools
agent = create_react_agent(llm, tools, prompt)

# Execute with AgentExecutor
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": question})
```

### Runnable Interface

All components implement LangChain's `Runnable` interface:

```python
class Runnable:
    def invoke(input) → output      # Execute synchronously
    def stream(input) → Iterator    # Stream results
    def batch(inputs) → List        # Process multiple inputs
```

## � How It Works

### REACT Agent Loop

When you ask a question, the agent follows the REACT pattern:

1. **Reason**: LLM analyzes the question and decides what to do
2. **Act**: LLM selects and calls appropriate tools
3. **Observe**: Tools return results
4. **Repeat**: Loop continues until answer is found

### Example: "How many albums are there?"

```
1. REASON
   LLM: "I need to count albums. First, let me list tables."

2. ACT
   Tool: ListSQLDatabaseTool
   Result: Tables include Album, Artist, Track, etc.

3. OBSERVE
   LLM: "Found Album table. Now let me get its schema."

4. ACT
   Tool: InfoSQLDatabaseTool
   Result: Album table has AlbumId, Title, ArtistId columns

5. OBSERVE
   LLM: "Now I'll count the albums."

6. ACT
   Tool: QuerySQLDatabaseTool
   SQL: SELECT COUNT(*) FROM Album
   Result: 347

7. ANSWER
   "There are 347 albums in the database."
```

### Tools Available to Agent

- **QuerySQLDatabaseTool**: Execute SQL queries
- **InfoSQLDatabaseTool**: Get table schema and structure
- **ListSQLDatabaseTool**: List all available tables
- **validate_sql_query**: Check query safety
- **recover_from_error**: Suggest fixes for errors

## �📦 Project Structure

```
.
├── sql_agent.py           # Main agent implementation
├── llm_agent.py          # LLM configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## 🔧 Configuration Details

### LLM Parameters

- **Model**: IBM Granite 3.2 8B Instruct
- **Max Tokens**: 1024
- **Temperature**: 0.2 (deterministic)
- **Top-P**: 0.95
- **Repetition Penalty**: 1.2

### Database Support

Currently optimized for **MySQL**. Easily extensible to:
- PostgreSQL
- SQLite
- Oracle
- SQL Server

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Test a specific query:

```bash
python sql_agent.py
```

## 📚 Example Queries

| Query | Purpose |
|-------|---------|
| "How many albums are there?" | Count aggregation |
| "List top 10 artists" | Sorting & limiting |
| "Describe the Customer table" | Schema inspection |
| "Show sales by genre" | Grouping & aggregation |

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Learn More

### Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed system architecture and LCEL + Tools design
- **[LCEL_GUIDE.md](LCEL_GUIDE.md)** - Complete guide to LCEL concepts and features
- **[EXAMPLES.md](EXAMPLES.md)** - Comprehensive usage examples
- **[FAQ.md](FAQ.md)** - Frequently asked questions

### External Resources
- [LangChain Documentation](https://python.langchain.com/)
- [LCEL Documentation](https://python.langchain.com/docs/expression_language/)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)
- [Agents Documentation](https://python.langchain.com/docs/modules/agents/)
- [IBM Watson Documentation](https://www.ibm.com/cloud/watson)

## �🙏 Acknowledgments

- [LangChain](https://python.langchain.com/) - For LCEL framework and community tools
- [IBM Watson](https://www.ibm.com/cloud/watson) - For LLM capabilities
- [MySQL](https://www.mysql.com/) - Database engine
- [Chinook Database](https://github.com/lerocha/chinook-database) - Sample database

## 📧 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/altugyerli/Ai-powerred-sql-agent/issues)
- Start a [Discussion](https://github.com/altugyerli/Ai-powerred-sql-agent/discussions)

---

**Made with ❤️ by [Altuğ Yerli](https://github.com/altugyerli)**

*Powered by LangChain LCEL + Community Tools*

