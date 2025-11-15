# Contributing to AI-Powered SQL Agent

Thank you for your interest in contributing! We welcome contributions from everyone.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Ai-powerred-sql-agent.git
   cd Ai-powerred-sql-agent
   ```

3. **Create a virtual environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Creating a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-postgresql-support`
- `fix/handle-null-values`
- `docs/update-readme`

### Code Style

We follow PEP 8 standards. Format your code with Black:

```bash
black sql_agent.py llm_agent.py
```

Check for linting issues:

```bash
flake8 sql_agent.py llm_agent.py
```

### Testing

Write tests for new features:

```bash
pytest tests/
pytest tests/ --cov
```

## Commit Guidelines

- Use clear, descriptive commit messages
- Reference issues when applicable: `Fixes #123`
- Keep commits atomic and focused

Example:
```
Add support for PostgreSQL databases

- Implement PostgreSQL connection handler
- Add database URI validation
- Update tests for new database type

Fixes #45
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**:
   ```bash
   pytest tests/
   ```
4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request** with a clear description

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Testing
How to test these changes

## Checklist
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
```

## Areas for Contribution

- 🐛 **Bug Fixes**: Report and fix issues
- ✨ **Features**: Add new database support, improve error handling
- 📚 **Documentation**: Improve README, add examples
- 🧪 **Tests**: Increase test coverage
- 🎨 **UI/UX**: Improve interactive mode

## Questions?

- Open an [Issue](https://github.com/altugyerli/Ai-powerred-sql-agent/issues)
- Start a [Discussion](https://github.com/altugyerli/Ai-powerred-sql-agent/discussions)

---

**Thank you for contributing! 🙏**

