import os

# Keep unit tests independent of a local PostgreSQL server/driver.
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
