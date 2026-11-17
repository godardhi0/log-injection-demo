from werkzeug.security import check_password_hash, generate_password_hash

# Fake user database. A real site would use a real database.
_USERS = {
    "client42": generate_password_hash("Secret!2026"),
}


def verify_credentials(username: str, password: str) -> bool:
    password_hash = _USERS.get(username)
    if password_hash is None:
        return False
    return check_password_hash(password_hash, password)