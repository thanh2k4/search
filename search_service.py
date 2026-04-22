from flask import Flask, request
from search_engine import search_many_fields
import scheduler
from flask_cors import CORS

app = Flask(__name__)
CORS(app, 
        origins =
            "http://192.168.10.101:3000"
)

@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    res = search_many_fields("news", keyword ,page=page , size=10)
    return res["hits"]

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
