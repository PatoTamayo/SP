from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/sensor_data", methods=["POST"])
def receive_data():
    """
    Esta función maneja las solicitudes POST en '/sensor_data' para procesar datos JSON.
    """
    if request.headers["Content-Type"] == "application/json":
        data = request.json

        humidity = data.get("humidity")
        print("Humidity:", humidity)

        temperature = data.get("temperature")
        print("Temperature:", temperature)     

        date_time = data.get("date_time")
        print("Date and Time:", date_time)

        return "Data received", 200
    else:
        return "Invalid Content-Type", 400

@app.route("/")
def hello_world():
    """
    Esta función muestra una página de inicio simple.
    """
    return render_template("index.html", title="Hello")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
