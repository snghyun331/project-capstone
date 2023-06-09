from flask import Flask, jsonify, request

from .apis import elastic_api

app = Flask(__name__)
app.register_blueprint(elastic_api)

if __name__ == '__main__':
    app.run(debug=False, port=8000)
