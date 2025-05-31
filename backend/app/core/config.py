import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")