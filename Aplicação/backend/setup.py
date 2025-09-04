from setuptools import setup, find_packages

setup(
    name="pm-ai-backend",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.6",
        "uvicorn[standard]==0.32.1",
        "pydantic==2.10.3",
        "pydantic-settings==2.7.0",
        "SQLAlchemy[asyncio]==2.0.36",
        "asyncpg==0.30.0",
        "alembic==1.14.0",
        "PyJWT==2.10.1",
        "passlib[bcrypt]==1.7.4",
        "httpx==0.28.1",
        "python-multipart==0.0.12",
        "pandas==2.2.3",
        "openpyxl==3.1.5",
        "reportlab==4.2.5",
        "redis==5.2.1",
        "celery==5.4.0",
        "structlog==24.4.0",
        "prometheus-client==0.21.1",
        "python-dotenv==1.0.1",
        "email-validator==2.2.0",
    ],
    extras_require={
        "test": [
            "pytest==8.3.4",
            "pytest-asyncio==0.24.0",
            "pytest-cov==6.0.0",
            "pytest-mock==3.14.0",
            "aiosqlite==0.20.0",
        ],
        "dev": [
            "ruff==0.8.4",
            "black==24.10.0",
            "mypy==1.13.0",
        ]
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
