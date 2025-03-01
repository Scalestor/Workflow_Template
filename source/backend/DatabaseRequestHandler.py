### This class serves as an intermediary between the database and the backend-server
###

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError


def create_standard_response(status, message, data=None):
    """
    Standardizes the API response format.
    :param status: 'success' or 'error'
    :param message: Message to convey (success message or error message)
    :param data: The actual data (None if no data, empty dictionary if error)
    :return: A standardized JSON response
    """
    response = {
        "status": status,
        "message": message,
        "data": data if data is not None else {}
    }
    return response    

class DatabaseRequestHandler:
    def __init__(self, database_engine_string):
        """
        Initializes the DatabaseRequestHandler with a connection string.
        The engine is created from the given connection string.
        :param database_engine_string: The database connection URL.
        """
        self.engine = create_engine(database_engine_string, echo=True)
        self.inspector = inspect(self.engine)

    def _execute_query(self, query, params=None):
        """
        Executes a given SQL query with parameters and returns the result.
        :param query: The SQL query to execute.
        :param params: Parameters to pass to the query (optional).
        :return: Query result or error message.
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params or {}).fetchall()
            return create_standard_response("success", "Query executed successfully", result)
        except SQLAlchemyError as e:
            return create_standard_response("error", f"Query error: {str(e)}", {})

    def get_tables(self):
        """Fetch the list of tables from the database."""
        try:
            tables = self.inspector.get_table_names()
            return create_standard_response("success", "Tables retrieved successfully", tables)
        except SQLAlchemyError as e:
            return create_standard_response("error", f"Database error: {str(e)}", {})

    def get_table_data_count(self, table_name):
        """Fetch count of rows from a specific table."""
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self._execute_query(query)
        if result["status"] == "error":
            return result  # Return the error if the query failed
        return create_standard_response("success", f"Count of rows in {table_name}", result["data"])

    def get_table_data(self, table_name, limit=100):
        """Fetch data from a specific table with an optional limit."""
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        result = self._execute_query(query)
        if result["status"] == "error":
            return result  # Return the error if the query failed
        return create_standard_response("success", f"Data from {table_name}", result["data"])

    def get_table_metadata(self, table_name):
        """Fetch metadata (column names) for a specific table."""
        try:
            columns = self.inspector.get_columns(table_name)
            metadata = [{"name": column["name"], "type": column["type"]} for column in columns]
            return create_standard_response("success", f"Metadata for table {table_name}", metadata)
        except SQLAlchemyError as e:
            return create_standard_response("error", f"Metadata error: {str(e)}", {})

    def execute_custom_query(self, query, params=None):
        """
        Executes a custom query that isn't predefined, with optional parameters.
        :param query: The SQL query to execute.
        :param params: Parameters to pass to the query (optional).
        :return: Query result or error message.
        """
        return self._execute_query(query, params)        