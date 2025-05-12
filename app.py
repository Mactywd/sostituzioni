from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/get_sostituzioni", methods=["POST"])
def get_sostituzioni():
    data = request.get_json()
    print(data)

    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
