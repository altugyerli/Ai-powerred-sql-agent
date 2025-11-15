# Architecture Overview

## System Design

The AI-Powered SQL Agent is built on **LangChain Expression Language (LCEL)** with **LangChain Community Tools**, implementing the REACT (Reasoning + Acting) agent pattern.

## LCEL + Tools Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  User Query (Natural Language)                │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────┐
        │  LLM (IBM Granite 3.2 8B Instruct)    │
        │  with Tool Access                      │
        └────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │ Query   │    │ Info     │    │ List     │
    │ Tool    │    │ Tool     │    │ Tool     │
    └─────────┘    └──────────┘    └──────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────┐
        │  REACT Agent Loop                      │
        │  • Reason about question               │
        │  • Select tool                         │
        │  • Execute tool                        │
        │  • Observe results                     │
        │  • Repeat until done                   │
        └────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────┐
        │  AgentExecutor (Runnable)              │
        │  • Manages tool execution              │
        │  • Handles errors                      │
        │  • Formats output                      │
        └────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Formatted Response (Dict)                        │
│  {                                                            │
│    "question": "...",                                         │
│    "answer": "...",                                           │
│    "status": "success"                                        │
│  }                                                            │
└──────────────────────────────────────────────────────────────┘
```

## LCEL + Tools Code Implementation

```python
# Step 1: Create tools from LangChain community
tools = [
    QuerySQLDatabaseTool(db=db),      # Execute SQL queries
    InfoSQLDatabaseTool(db=db),       # Get table schema
    ListSQLDatabaseTool(db=db),       # List tables
    validate_sql_query,               # Custom validation
    recover_from_error,               # Custom recovery
]

# Step 2: Create REACT agent with tools
agent = create_react_agent(llm, tools, prompt)

# Step 3: Create AgentExecutor (Runnable)
executor = AgentExecutor(agent=agent, tools=tools)

# Step 4: Execute using Runnable interface
result = executor.invoke({"input": question})

# Step 5: Stream results
for chunk in executor.stream({"input": question}):
    print(chunk)
```

## LCEL + Tools Components

### 1. **LangChain Community Tools**

#### QuerySQLDatabaseTool
```python
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

query_tool = QuerySQLDatabaseTool(db=db)
```
- Executes SQL queries on the database
- Returns query results
- Handles database errors
- Part of LCEL Runnable interface

#### InfoSQLDatabaseTool
```python
from langchain_community.tools.sql_database.tool import InfoSQLDatabaseTool

info_tool = InfoSQLDatabaseTool(db=db)
```
- Retrieves table schema information
- Shows column names and types
- Provides table structure details
- Helps LLM understand database

#### ListSQLDatabaseTool
```python
from langchain_community.tools.sql_database.tool import ListSQLDatabaseTool

list_tool = ListSQLDatabaseTool(db=db)
```
- Lists all available tables
- Shows database structure
- Helps LLM discover tables
- Essential for exploration

### 2. **Custom Tools**

#### validate_sql_query
```python
validate_tool = Tool(
    name="validate_sql_query",
    func=self._validate_sql_query,
    description="Validate if a SQL query is safe and well-formed"
)
```
- Checks for dangerous SQL keywords
- Validates query syntax
- Prevents SQL injection
- Provides safety feedback

#### recover_from_error
```python
error_recovery_tool = Tool(
    name="recover_from_error",
    func=self._recover_from_error,
    description="Recover from SQL execution errors"
)
```
- Analyzes error messages
- Suggests fixes
- Helps LLM recover
- Improves robustness

### 3. **REACT Agent Pattern**

```python
from langchain.agents import create_react_agent, AgentExecutor

# Create agent with tools
agent = create_react_agent(llm, tools, prompt)

# Create executor
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)
```

**REACT Loop:**
1. **Reason**: LLM thinks about the question
2. **Act**: LLM selects and uses a tool
3. **Observe**: Tool returns results
4. **Repeat**: Loop until answer found

### 4. **Runnable Interface**

All components implement LCEL's Runnable interface:

```python
# Synchronous execution
result = executor.invoke({"input": question})

# Streaming execution
for chunk in executor.stream({"input": question}):
    print(chunk)

# Batch execution
results = executor.batch([{"input": q} for q in questions])
```

## Key Features

### Type Safety
```python
from typing import Dict, Any

def query(self, question: str) -> Dict[str, Any]:
    """Execute a natural language query"""
    return self.agent_executor.invoke({"input": question})
```

### Composability
LCEL allows chaining operations:
```python
chain = input_processor | llm | sql_executor | output_formatter
```

### Streaming Support
Real-time response streaming for long-running queries.

### Debugging
Built-in tracing and debugging capabilities.

## Configuration

### LLM Parameters
- **Temperature**: 0.2 (deterministic responses)
- **Max Tokens**: 1024 (sufficient for complex queries)
- **Top-P**: 0.95 (nucleus sampling)
- **Repetition Penalty**: 1.2 (avoid repetition)

### Database Connection
- Connection pooling for efficiency
- Automatic reconnection handling
- Query timeout management

## Error Handling

The system implements multi-level error handling:

1. **Input Validation**: Check query format
2. **LLM Validation**: Verify generated SQL
3. **Execution Handling**: Catch database errors
4. **Recovery**: Regenerate queries on failure

## Performance Optimization

- **Schema Caching**: Reduces token usage
- **Query Optimization**: Efficient SQL generation
- **Connection Pooling**: Reuses database connections
- **Token Efficiency**: Minimal context for schema

## Extensibility

### Adding New Database Support
1. Implement database connector
2. Update SQLDatabase configuration
3. Add connection tests

### Custom Tools
Extend agent with custom tools:
```python
from langchain.tools import Tool

custom_tool = Tool(
    name="tool_name",
    func=tool_function,
    description="Tool description"
)
```

---

For more details, see [README.md](README.md)

