"""
Setup configuration for AI-Powered SQL Agent
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-powered-sql-agent",
    version="1.0.0",
    author="Altuğ Yerli",
    author_email="99094570+altugyerli@users.noreply.github.com",
    description="Transform natural language questions into SQL queries using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/altugyerli/Ai-powerred-sql-agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=[
        "langchain==0.2.1",
        "langchain-ibm==0.1.7",
        "langchain-community==0.0.59",
        "langchain-experimental==0.0.59",
        "ibm-watsonx-ai==1.0.4",
        "ibm-watson-machine-learning==1.0.357",
        "mysql-connector-python==8.4.0",
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sql-agent=sql_agent:main",
        ],
    },
)

