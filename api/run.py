from flask import Flask

app = Flask(__name__)
import views


@app.before_first_request
def create_tables():
    pass


if __name__ == '__main__':
    app.run(app=app, debug=True)
