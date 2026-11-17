import logging

from flask import Blueprint, current_app, render_template, request

from app.services.auth_service import verify_credentials
from app.services.log_sanitizer import sanitize_for_log

bp = Blueprint("secure", __name__, url_prefix="/secure")
logger = logging.getLogger("demo.secure")


@bp.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    status = 200

    if request.method == "POST":
        ip = request.remote_addr
        raw_username = request.form.get("username", "")
        password = request.form.get("password", "")

        # The input is cleaned BEFORE any use in a log
        safe_username = sanitize_for_log(
            raw_username, current_app.config["MAX_LOG_FIELD_LENGTH"]
        )

        if verify_credentials(raw_username, password):
            logger.info('LOGIN_SUCCESS user="%s" ip=%s', safe_username, ip)
            message = "Connexion réussie."
        else:
            limiter = current_app.extensions["rate_limiter"]
            failures = limiter.record_failure(ip)

            logger.warning('LOGIN_FAILED user="%s" ip=%s', safe_username, ip)

            if limiter.is_exceeded(failures):
                logger.critical(
                    "ALERT possible brute force ip=%s failures=%d window=%ds",
                    ip, failures, limiter.window_seconds,
                )
                message = "Trop de tentatives. Réessayez plus tard."
                status = 429
            else:
                message = "Identifiants incorrects."

    return render_template("login.html", titre="Version corrigée", message=message), status