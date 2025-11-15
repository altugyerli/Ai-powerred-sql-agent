# Usage Examples

## Basic Setup with LCEL + Tools

```python
from sql_agent import SQLAgent

# Initialize the agent (builds LCEL + Tools internally)
agent = SQLAgent()

# The agent has access to:
# - QuerySQLDatabaseTool: Execute SQL
# - InfoSQLDatabaseTool: Get schema
# - ListSQLDatabaseTool: List tables
# - validate_sql_query: Validate queries
# - recover_from_error: Error recovery
```

## Example Queries

### 1. Simple Count Query

```python
result = agent.query("How many albums are in the database?")
print(result)
```

**Output:**
```
{
    'question': 'How many albums are in the database?',
    'answer': 'There are 347 albums in the database.',
    'status': 'success'
}
```

**Agent Process (REACT Loop):**
1. Reason: "I need to count albums"
2. Act: Use ListSQLDatabaseTool to find Album table
3. Act: Use InfoSQLDatabaseTool to understand schema
4. Act: Use QuerySQLDatabaseTool to execute: SELECT COUNT(*) FROM Album
5. Observe: Result is 347
6. Answer: "There are 347 albums in the database."

### 2. Table Description

```python
result = agent.query("Describe the structure of the PlaylistTrack table")
print(result)
```

**Agent Process:**
1. Use ListSQLDatabaseTool to find PlaylistTrack
2. Use InfoSQLDatabaseTool to get schema details
3. Format and return structure information

### 3. Aggregation Query

```python
result = agent.query("How many employees are there?")
print(result)
```

### 4. Filtering Query

```python
result = agent.query("Show me customers from Canada")
print(result)
```

### 5. Sorting and Limiting

```python
result = agent.query("List the top 10 best-selling artists")
print(result)
```

### 6. Complex Multi-Table Query

```python
result = agent.query(
    "What is the total revenue by genre? "
    "Show only genres with revenue over $1000"
)
print(result)
```

### 7. Date-Based Query

```python
result = agent.query("How many invoices were created in 2013?")
print(result)
```

### 8. Join Query

```python
result = agent.query(
    "Show me all albums with their artists' names"
)
print(result)
```

## Interactive Mode (LCEL + Tools)

```python
from sql_agent import SQLAgent

agent = SQLAgent()
agent.run_interactive()
```

**Interactive Session:**
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

## Advanced Usage

### Custom Configuration

```python
from sql_agent import SQLAgent, SQLAgentConfig

config = SQLAgentConfig()
config.temperature = 0.1  # More deterministic
config.max_tokens = 2048  # Longer responses

agent = SQLAgent(config=config)
result = agent.query("Your question here")
```

### Error Handling with Tool Recovery

```python
from sql_agent import SQLAgent

agent = SQLAgent()

try:
    result = agent.query("Your question")
    if result['status'] == 'success':
        print(f"Answer: {result['answer']}")
    else:
        print(f"Error: {result['answer']}")
except Exception as e:
    print(f"Error: {e}")
```

### Batch Processing with Runnable Interface

```python
from sql_agent import SQLAgent

agent = SQLAgent()

questions = [
    "How many albums are there?",
    "How many artists are there?",
    "How many customers are there?",
]

# Using batch() from Runnable interface
results = agent.agent_executor.batch(
    [{"input": q} for q in questions]
)

for result in results:
    print(f"Q: {result['input']}")
    print(f"A: {result['output']}\n")
```

### Streaming Results with Runnable Interface

```python
from sql_agent import SQLAgent

agent = SQLAgent()

# Stream results in real-time
for chunk in agent.agent_executor.stream(
    {"input": "How many albums are there?"}
):
    print(chunk, end="", flush=True)
```

## Tips & Tricks

### 1. Be Specific
❌ "Show me data"
✅ "Show me all customers from the USA with their total spending"

### 2. Use Natural Language
❌ "SELECT * FROM Album WHERE ArtistId = 1"
✅ "Show me all albums by artist ID 1"

### 3. Ask for Explanations
✅ "Explain the relationship between Album and Artist tables"

### 4. Request Formatting
✅ "Show me the top 5 genres sorted by popularity"

### 5. Let the Agent Use Tools
The agent will automatically:
- List tables to understand structure
- Get schema information
- Validate queries
- Recover from errors

## Troubleshooting

### Query Not Understood
If the agent doesn't understand your query:
- Rephrasing with simpler language
- Breaking complex queries into smaller parts
- Providing more context
- The agent will use tools to explore the database

### Incorrect Results
- Verify the database is properly connected
- Check table and column names
- Ask the agent to describe the table structure first
- The agent can use validate_sql_query tool

### Performance Issues
- Reduce `MAX_TOKENS` for faster responses
- Increase `TEMPERATURE` for more creative solutions
- Use more specific queries
- Check database indexes

### Tool Errors
- The agent has recover_from_error tool
- It will suggest fixes for common SQL errors
- Check database permissions
- Verify connection credentials

---

For more information, see [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md)

