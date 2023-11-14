import logging

from flask import Flask
from flask import make_response
from flask.typing import ResponseValue
from flask_app.route.books_issued import books_issued_blueprint

logger = logging.getLogger("k8s-books_backend")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s",
    force=True,
)
logger.info("Starting Books Issued Flask Backend")

app = Flask(__name__, template_folder="/tmp")


"""Flask App to interact with Database, save and retrieve records
"""

__VERSION__=1.0

"""To add Flask App version in final response
"""

app.register_blueprint(books_issued_blueprint, url_prefix="/book_issued")

@app.after_request
def add_app_version(response: ResponseValue):

    response_json = response.get_json()
    if response_json:
        logger.info(f"Setting App Version after request: {__VERSION__}")
        response_json["app_version"] = __VERSION__
        return make_response(response_json, response.status_code)
    else:
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
