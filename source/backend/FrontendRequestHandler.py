### This class handles the requests against the database handler.

###

from flask import Flask, request, jsonify
from source.backend.DatabaseRequestHandler import DatabaseRequestHandler


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

class FrontendRequestHandler:
    def __init__(self, db_handler:DatabaseRequestHandler):
        self.db_handler = db_handler

    def handle_tables_request(self):
        """Handle request for fetching available tables."""
        db_response = self.db_handler.get_tables()
        if "error" == db_response.get("status"):
            return jsonify({"error": db_response["message"]}), 500
        
        response = create_standard_response(status="success",message="Tables present in the database",data=db_response.get("data"))

        return jsonify(response)

    def handle_data_request(self, table_name):
        """Handle request for fetching data (e.g., row count) from a table."""
        # Check if the table exists
        db_response = self.db_handler.get_table_data_count(table_name)
        if "error" == db_response.get("status"):
            return jsonify({"error": db_response["message"]}), 500
        

        response = create_standard_response(status="success",message=f"Data from query SELECT COUNT(*) FROM {table_name}",data=db_response.get("data"))
        return jsonify(response)