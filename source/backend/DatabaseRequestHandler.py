### This class serves as an intermediary between the database and the backend-server
###

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError


class DatabaseRequestHandler:
    def __init__(self, database_engine_string):
        self.engine = create_engine(database_engine_string, echo=True)
        self.inspector = inspect(self.engine)

    def get_tables(self):
        """Fetch the list of tables from the database."""
        try:
            return self.inspector.get_table_names()
        except SQLAlchemyError as e:
            return {"error": f"Database error: {str(e)}"}

    def get_table_data_count(self, table_name):
        """Fetch count of rows from a specific table."""
        try:
            with self.engine.connect() as connection:
                query = text(f"SELECT COUNT(*) FROM {table_name}")
                result = connection.execute(query).scalar()
            return result
        except SQLAlchemyError as e:
            return {"error": f"Query error: {str(e)}"}