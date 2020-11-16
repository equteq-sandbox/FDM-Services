from flask import Flask, Response, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_endpoint():
	data = {"msg": "Hello World"}
	return jsonify(data)

if __name__ == "__main__":
	# while running locally use: app.run(debug=True)
	app.run()