# error_handlers.py
from flask import jsonify, request

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        """Error handler for 404 Not Found."""
        app.logger.error('Resource not found: %s', request.url)
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Error handler for 500 Internal Server Error."""
        app.logger.error('Internal server error: %s', error)
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """General error handler."""
        status_code = 500
        if hasattr(error, 'code') and 500 <= error.code < 600:
            status_code = error.code
        response = jsonify({'error': 'An unexpected error occurred'})
        response.status_code = status_code
        app.logger.error('Internal server error: %s', error)
        return response
