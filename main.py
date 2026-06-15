from fastapi import FastAPI, HTTPException
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Air-Gapped AI Data Analyst")

# Fetch the database URL from .env
DB_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    """Creates a connection to the PostgreSQL database."""
    try:
        # RealDictCursor returns rows as dictionaries
        conn = psycopg2.connect(
            DB_URL,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None


@app.get("/")
async def system_status():
    return {
        "status": "System Online",
        "message": "The Sovereign Architecture is awake."
    }


@app.get("/test-db")
async def test_database_connection():
    """Tests the connection using our restricted AI role."""
    conn = get_db_connection()

    if not conn:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    try:
        cursor = conn.cursor()

        # AI role only has SELECT permission
        cursor.execute(
            "SELECT company_name, industry FROM clients;"
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )