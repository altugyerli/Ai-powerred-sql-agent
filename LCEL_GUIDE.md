# LCEL (LangChain Expression Language) Guide

## What is LCEL?

LCEL is LangChain's modern framework for composing AI applications. It provides:
- **Runnable Interface**: Unified abstraction for all components
- **Composability**: Chain operations together with `|` operator
- **Type Safety**: Full type hints throughout
- **Streaming**: Real-time response generation
- **Debugging**: Built-in tracing and debugging

## Core Concepts

### 1. Runnable Interface

All LCEL components implement the `Runnable` interface:

```python
from langchain_core.runnables import Runnable

class Runnable:
    def invoke(input) → output           # Synchronous execution
    def stream(input) → Iterator         # Stream results
    def batch(inputs) → List[output]     # Batch processing
    def __or__(other) → Runnable         # Pipe operator (|)
```

### 2. Pipe Operator (|)

Chain runnables together:

```python
# Create individual runnables
step1 = RunnableLambda(validate_input)
step2 = RunnableLambda(process_data)
step3 = RunnableLambda(format_output)

# Compose with pipe operator
chain = step1 | step2 | step3

# Execute
result = chain.invoke(data)
```

### 3. RunnableLambda

Wrap functions as runnables:

```python
from langchain_core.runnables import RunnableLambda

def my_function(x):
    return x.upper()

runnable = RunnableLambda(my_function)
result = runnable.invoke("hello")  # "HELLO"
```

### 4. RunnablePassthrough

Pass data through unchanged:

```python
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough() | process_step
```

### 5. RunnableParallel

Execute operations in parallel:

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    step1=RunnableLambda(func1),
    step2=RunnableLambda(func2),
)

result = parallel.invoke(data)
# Returns: {"step1": result1, "step2": result2}
```

## Tools in LCEL

### Creating Tools

```python
from langchain_core.tools import Tool

tool = Tool(
    name="my_tool",
    func=my_function,
    description="What this tool does"
)
```

### LangChain Community Tools

```python
from langchain_community.tools.sql_database.tool import (
    QuerySQLDatabaseTool,
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)

tools = [
    QuerySQLDatabaseTool(db=db),
    InfoSQLDatabaseTool(db=db),
    ListSQLDatabaseTool(db=db),
]
```

## Agents with LCEL

### REACT Agent Pattern

```python
from langchain.agents import create_react_agent, AgentExecutor

# Create agent
agent = create_react_agent(llm, tools, prompt)

# Create executor (Runnable)
executor = AgentExecutor(agent=agent, tools=tools)

# Execute
result = executor.invoke({"input": question})
```

### Agent Execution Methods

```python
# Synchronous
result = executor.invoke({"input": question})

# Streaming
for chunk in executor.stream({"input": question}):
    print(chunk)

# Batch
results = executor.batch([
    {"input": q1},
    {"input": q2},
])
```

## In This Project

### Tools Used

1. **QuerySQLDatabaseTool**: Execute SQL queries
2. **InfoSQLDatabaseTool**: Get table schema
3. **ListSQLDatabaseTool**: List tables
4. **Custom Tools**: Validation and recovery

### LCEL Features Used

- **Runnable Interface**: All components are runnables
- **AgentExecutor**: Manages tool execution
- **create_react_agent**: REACT pattern
- **ChatPromptTemplate**: Structured prompts
- **Tool**: Custom tool creation

### Execution Flow

```
User Input
    ↓
[LCEL Runnable: AgentExecutor]
    ├─ Reason about question
    ├─ Select tool
    ├─ Execute tool (Runnable)
    ├─ Observe results
    └─ Repeat until done
    ↓
Formatted Output
```

## Best Practices

1. **Use Runnable Interface**: All components should be runnables
2. **Compose with Pipe**: Use `|` for clean composition
3. **Handle Errors**: Use error recovery tools
4. **Stream When Possible**: Use `.stream()` for real-time responses
5. **Type Hints**: Always add type hints

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LCEL Documentation](https://python.langchain.com/docs/expression_language/)
- [Tools Documentation](https://python.langchain.com/docs/modules/tools/)
- [Agents Documentation](https://python.langchain.com/docs/modules/agents/)

---

For more details, see [ARCHITECTURE.md](ARCHITECTURE.md)

