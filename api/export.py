
from flask import Flask, Response
import csv, io

app = Flask(__name__)

@app.route("/", methods=["GET"])
def handler():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["time", "direction", "score", "hit", "profit"])
    return Response(output.getvalue(), content_type="text/csv")

handler = app
