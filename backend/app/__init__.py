"""
StrangeVerse backend — Flask application factory.
"""

import os
import warnings

# Suppress multiprocessing resource_tracker noise from deps (e.g. transformers)
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # JSON: allow non-ASCII in responses (Flask 2.3+)
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False
    
    # Logging
    logger = setup_logger('strangeverse')
    
    # Log startup once in debug (reloader child only)
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process
    
    if should_log_startup:
        logger.info("=" * 50)
        logger.info("StrangeVerse backend starting...")
        logger.info("=" * 50)
    
    # CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register cleanup so simulation child processes exit on server shutdown
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Registered simulation process cleanup handler")
    
    # Request logging
    @app.before_request
    def log_request():
        logger = get_logger('strangeverse.request')
        logger.debug(f"request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"body: {request.get_json(silent=True)}")
    
    @app.after_request
    def log_response(response):
        logger = get_logger('strangeverse.request')
        logger.debug(f"response: {response.status_code}")
        return response
    
    # Blueprints
    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    # Health
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'StrangeVerse Backend'}
    
    if should_log_startup:
        logger.info("StrangeVerse backend ready")
    
    return app

