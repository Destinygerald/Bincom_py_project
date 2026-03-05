import uvicorn
from fastapi import FastAPI
from config import settings
from contextlib import asynccontextmanager
from routes.votes import router as vote_route
from _config.db import engine, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect, text


app = FastAPI()

app.include_router(vote_route)

@app.get("/")
async def root():
    return { "message": "Server Healthy" }


                    

async def load_dump(db: AsyncSession):
    try:
        with open("bincom_test.sql", "r") as f:
            statements = [s.strip() for s in f.read().split(';') if s.strip()]
        
        async with engine.begin() as conn:
            for statement in statements:
                await conn.execute(text(statement))
            print("**************** SUCCESSFUL *****************")
    except Exception as e:
        print(f"Failed to load: {e}")

async def check_tables(engine):
    def get_tables(sync_conn):
        insp = inspect(sync_conn)
        # Pass None to avoid double-quoting the database
        return insp.get_table_names(schema=None)

    async with engine.connect() as conn:
        tables = await conn.run_sync(get_tables)
        print(f"Visible tables: {tables}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app...")
    
    async with AsyncSessionLocal() as session:
        await load_dump(session)  # Execute SQL dump on startup
    await check_tables(engine)
    yield
    print("Shutting down app...")

app.router.lifespan_context = lifespan

@app.get("/")
async def root():
    return {"message": "FastAPI with MySQL dump executed on startup!"}


if (__name__ == "__main__"):
    uvicorn.run(app, host=settings.host, port=settings.port)