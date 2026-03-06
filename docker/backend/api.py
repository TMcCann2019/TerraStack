from fastapi import FastAPI, HTTPException
import psycopg2
import os

app = FastAPI(title="TerraStack Backend")

# Read DB connection info from environment variables (Secrets/ConfigMap)
DB_HOST = os.getenv("DB_HOST", "db-svc")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "terrastack")
DB_USER = os.getenv("DB_USER", "terrastack")
DB_PASS = os.getenv("DB_PASSWORD", "terrastack")

@app.get("/")
def read_root():
    return {"message": "TerraStack Backend Running"}

@app.get("/health")
def health():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        conn.close()
        return {"database": "connected"}
    except Exception as e:
        return {"database": "error", "details": str(e)}

@app.get("/quote")
def get_quote(sqft: float):
    if sqft <= 0:
        raise HTTPException(status_code=400, detail="Square footage must be greater than 0")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("SELECT quote, author FROM quotes ORDER BY RANDOM() LIMIT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result:
            quote_text, author = result
            # Example pricing logic based on sqft
            price_per_sqft = 0.5  # $0.50 per sq ft for yard work
            price = sqft * price_per_sqft
            return {"quote": quote_text, "author": author, "sqft": sqft, "estimated_price": price}
        else:
            return {"error": "No quotes found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))