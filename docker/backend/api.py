from fastapi import FastAPI, HTTPException, Query
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from contextlib import closing

app = FastAPI(title="TerraStack Yard Work API")

DB_HOST = os.getenv("DB_HOST", "db-svc")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "terrastack")
DB_USER = os.getenv("DB_USER", "terrastack")
DB_PASS = os.getenv("DB_PASSWORD", "terrastack")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        cursor_factory=RealDictCursor
    )

@app.get("/yard-quote")
def yard_quote(sqft: int = Query(..., gt=0, description="Square footage of yard")):
    """
    Return suggested yard work task and price based on square footage.
    """
    try:
        with closing(get_db_connection()) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT task, estimated_hours, rate_per_hour,
                           estimated_hours * rate_per_hour AS total_cost
                    FROM yard_quotes
                    WHERE %s BETWEEN min_sqft AND max_sqft
                    LIMIT 1
                """, (sqft,))
                result = cur.fetchone()
                if not result:
                    return {"message": "No quote available for this size"}
                return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))