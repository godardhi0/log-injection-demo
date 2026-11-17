import logging

from flask import Blueprint, render_template, request

from app.services.auth_service import verify_credentials

bp = Blueprint("vulnerable", __name__, url_prefix="/vulnerable")
logger = logging.getLogger("demo.vulnerable")


@bp.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if verify_credentials(username, password):
            logger.info("Connexion réussie pour : " + username)
            message = "Connexion réussie."
        else:
            # FLAW (CWE-117): the user input is written as is in the log.
            # Nothing is counted and no alert exists (CWE-778).
            logger.warning("Échec de connexion pour : " + username)
            message = "Identifiants incorrects."

    return render_template("login.html", titre="Version vulnérable", message=message)