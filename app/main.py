from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
from .config import settings
from .db import connect, query_db

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG

@app.get("/")
async def root():
    return {"message": "Welcome to the bookstore!"}


@app.get("/book/")
async def book(
    name: str = None, year: int = None, author: str = None, limit: int = 100
):
    try:
        logging.debug("Incoming request to /book endpoint.")
        logging.debug(f"Parameters received: name={name}, year={year}, author={author}, limit={limit}")

        conn = connect(
            database=settings.database,
            host=settings.host,
            port=settings.port,
            user=settings.user,
            password=settings.password,
        )
        result = query_db(
            conn,
            settings.db_schema,
            "book",
            ("name", "author", "year"),
            name=name,
            year=year,
            author=author,
            limit=limit,
        )
        print(result) 
#        return JSONResponse(result)
        return result
    except Exception as e:
         logging.error(f"Error in /book endpoint: {str(e)}")
#        return JSONResponse({"message": str(e)}, status_code=500)
         return JSONResponse(content={"message": str(e)}, status_code=500)


@app.get("/db_info/")
def db_info():
    try:
        connect(
            database=settings.database,
            host=settings.host,
            port=settings.port,
            user=settings.user,
            password=settings.password,
        )
        return {
            "message": f"Connected to {settings.host}:{settings.port}/{settings.database}. User: {settings.user}."
        }
    except Exception as e:
        return JSONResponse(
            {
                "message": f"{str(e)} {settings.host}:{settings.port}/{settings.database}. User: {settings.user}."
            },
            status_code=500,
        )
