from flask import Flask

from config import Config
from app.logging_config import setup_logging
from app.routes import vulnerable, secure
from app.services.rate_limiter import SlidingWindowRateLimiter


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    setup_logging(app.config["LOG_DIR"], app.config["LOG_FORMAT"])

    # One limiter shared by the whole application
    app.extensions["rate_limiter"] = SlidingWindowRateLimiter(
        max_attempts=app.config["MAX_FAILED_ATTEMPTS"],
        window_seconds=app.config["WINDOW_SECONDS"],
    )

    app.register_blueprint(vulnerable.bp)
    app.register_blueprint(secure.bp)
    return app