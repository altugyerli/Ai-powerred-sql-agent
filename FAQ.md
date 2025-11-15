# Frequently Asked Questions

## General Questions

### Q: What is the AI-Powered SQL Agent?
**A:** It's an intelligent system that converts natural language questions into SQL queries using AI. You can ask questions in plain English and get database results without knowing SQL.

### Q: Do I need to know SQL to use this?
**A:** No! The entire point is to make databases accessible to non-technical users. Just ask questions in natural language.

### Q: What databases are supported?
**A:** Currently, MySQL is fully supported. PostgreSQL, SQLite, and Oracle support are planned for future releases.

## Technical Questions

### Q: What LLM does it use?
**A:** It uses IBM's Granite 3.2 8B Instruct model, which is optimized for instruction-following tasks.

### Q: What is LCEL?
**A:** LCEL (LangChain Expression Language) is a modern framework for composing AI applications. It provides type safety, composability, and streaming support.

### Q: Can I use a different LLM?
**A:** Yes! You can modify the `llm_agent.py` file to use any LLM supported by LangChain.

### Q: How do I set up the project?
**A:** Follow the Quick Start guide in [README.md](README.md). It takes about 5 minutes.

## Configuration Questions

### Q: Where do I put my API credentials?
**A:** Create a `.env` file based on `.env.example` and add your credentials there.

### Q: What if I don't have IBM Watson credentials?
**A:** You'll need to sign up for IBM Cloud and create a Watson project. See the README for links.

### Q: Can I change the LLM parameters?
**A:** Yes! Modify the `SQLAgentConfig` class or set environment variables.

## Usage Questions

### Q: How do I ask complex questions?
**A:** Be specific and clear. For example:
- ✅ "Show me the top 10 customers by total spending in 2024"
- ❌ "Show me data"

### Q: What if the agent gives wrong results?
**A:** Try rephrasing your question or breaking it into smaller parts. Check the verbose output to see what SQL was generated.

### Q: Can I use it in production?
**A:** Yes, but ensure proper error handling, monitoring, and testing. See [SECURITY.md](SECURITY.md) for best practices.

### Q: How do I run it interactively?
**A:** Use `agent.run_interactive()` or run `make interactive`.

## Performance Questions

### Q: Why is my query slow?
**A:** Large queries might take time. Try:
- Reducing `MAX_TOKENS`
- Using more specific queries
- Checking database indexes

### Q: How can I improve performance?
**A:** 
- Use connection pooling
- Optimize database indexes
- Reduce query complexity
- Cache frequently asked questions

## Troubleshooting

### Q: I get "Connection refused" error
**A:** Check that:
- MySQL server is running
- Credentials in `.env` are correct
- Host and port are correct

### Q: The agent doesn't understand my question
**A:** Try:
- Using simpler language
- Being more specific
- Asking about table structure first

### Q: I get "API key invalid" error
**A:** Verify your IBM Watson credentials are correct and active.

## Contributing

### Q: How can I contribute?
**A:** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Q: Can I add support for other databases?
**A:** Yes! We welcome database support contributions.

### Q: How do I report bugs?
**A:** Open an issue on GitHub with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior

## Support

### Q: Where can I get help?
**A:** 
- Check [EXAMPLES.md](EXAMPLES.md) for usage examples
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Open an issue on GitHub
- Start a discussion on GitHub

### Q: Is there a community?
**A:** Yes! Join discussions on GitHub to connect with other users.

---

Can't find your answer? [Open an issue](https://github.com/altugyerli/Ai-powerred-sql-agent/issues) or [start a discussion](https://github.com/altugyerli/Ai-powerred-sql-agent/discussions).

