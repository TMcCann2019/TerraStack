from fastapi import FastAPI
import psycopg2
import os

app = FastAPI(title="TerraStack API")

DB_HOST = os.getenv("DB_HOST", "terrastack-db")
DB_NAME = "terrastack"
DB_USER = "postgres"
DB_PASS = "password"

@app.get("/")
def read_root():
    return {"message": "TerraStack API Running"}

@app.get("/health")
def health():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        conn.close()
        return {"database": "connected"}
    except Exception as e:
        return {"database": "error", "details": str(e)}