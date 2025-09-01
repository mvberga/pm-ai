from setuptools import setup, find_packages

setup(
    name="pm-ai-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.0",
        "uvicorn[standard]==0.30.6",
        "pydantic==2.8.2",
        "pydantic-settings==2.4.0",
        "SQLAlchemy[asyncio]==2.0.35",
        "asyncpg==0.29.0",
        "alembic==1.13.2",
        "PyJWT==2.8.0",
        "passlib[bcrypt]==1.7.4",
        "httpx==0.27.0",
        "python-multipart==0.0.6",
    ],
    extras_require={
        "test": [
            "pytest==8.0.0",
            "pytest-asyncio==0.23.5",
            "pytest-cov==4.1.0",
            "aiosqlite==0.19.0",
        ]
    }
)
