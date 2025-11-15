# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in the AI-Powered SQL Agent, please email us at:
**99094570+altugyerli@users.noreply.github.com**

Please do **NOT** open a public issue for security vulnerabilities.

Include the following information:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

## Security Best Practices

### 1. Environment Variables
- **Never** commit `.env` files to version control
- Use `.env.example` as a template
- Rotate API keys regularly
- Use strong, unique passwords for database access

### 2. Database Credentials
- Store credentials in environment variables only
- Use database users with minimal required permissions
- Enable SSL/TLS for database connections
- Implement connection timeouts

### 3. API Keys
- Keep IBM Watson API keys confidential
- Rotate keys periodically
- Use separate keys for development and production
- Monitor API usage for unusual activity

### 4. SQL Injection Prevention
- The agent uses parameterized queries
- Input validation is performed at multiple levels
- Never directly concatenate user input into queries

### 5. Data Privacy
- Be aware of sensitive data in queries
- Implement appropriate access controls
- Log queries securely
- Comply with data protection regulations (GDPR, CCPA, etc.)

## Supported Versions

| Version | Status | Support Until |
|---------|--------|---------------|
| 1.0.x   | Active | 2026-11-15    |

## Security Updates

Security updates will be released as soon as possible after discovery.
Users are encouraged to update to the latest version promptly.

## Dependencies

We regularly monitor dependencies for security vulnerabilities using:
- GitHub Dependabot
- pip-audit
- Safety

## Compliance

This project follows security best practices including:
- Input validation and sanitization
- Secure error handling
- Minimal privilege principle
- Regular security audits

## Questions?

For security-related questions, please contact:
**99094570+altugyerli@users.noreply.github.com**

---

Last Updated: 2025-11-15

