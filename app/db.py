import psycopg2
from psycopg2 import extras, sql
from fastapi.responses import JSONResponse
import logging
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG
DEFAULT_FIELDS = ("name", "year", "author")


def connect(database, host, user, password, port):
    conn = psycopg2.connect(
        database=database, host=host, user=user, password=password, port=port
    )
    return conn


def query_db(
    conn,
    schema,
    table,
    select_fields=DEFAULT_FIELDS,
    name=None,
    year=None,
    author=None,
    limit=100,
):
    # Nightmare code, originally I wanted this whole thing to be a lambda (sunglasses emoji)
    with conn.cursor(cursor_factory=extras.DictCursor) as cur:
        logging.debug(f"Preparing query for table: {schema}.{table} with limit: {limit}")
        query = sql.Composed(
            [
                sql.SQL("SELECT "),
                sql.SQL(", ").join(sql.Identifier(field) for field in select_fields),
                sql.SQL(f" FROM "),
                sql.Identifier(schema),
                sql.SQL("."),
                sql.Identifier(table),
                sql.SQL(f" WHERE "),
                sql.Identifier("name"),
                sql.SQL("="),
                sql.SQL("COALESCE(%s, name) "),
                sql.SQL(f"AND "),
                sql.Identifier("year"),
                sql.SQL("="),
                sql.SQL("COALESCE(%s, year) "),
                sql.SQL(f"AND "),
                sql.Identifier("author"),
                sql.SQL("="),
                sql.SQL("COALESCE(%s, author) "),
                sql.SQL("LIMIT "),
                sql.Literal(limit),
            ]
        )
        logging.debug(f"Constructed query: {query.as_string(conn)}")  # Log the full query
        cur.execute(query, (name, year, author))
#        result = cur.fetchall()
        result = [dict(row) for row in cur.fetchall()]
        logging.info(f"Query executed successfully. Rows fetched: {len(result)}")
#    return JSONResponse(result)
    return result
