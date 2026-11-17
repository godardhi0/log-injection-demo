from app import create_app

app = create_app()

if __name__ == "__main__":
    # 127.0.0.1 = localhost only: the demo cannot be reached from outside
    app.run(host="127.0.0.1", port=5000, debug=False)