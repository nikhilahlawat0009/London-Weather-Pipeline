from flask import Flask, render_template, request, jsonify
import requests
import threading
from IPython.display import display, HTML

app = Flask(__name__)

# Flask app logic
API_KEY = "42cb047397fee9639d8da30ed471abe2"  # Replace with your API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

UK_CITIES = [
    "London", "Manchester", "Birmingham", "Leeds", "Liverpool",
    "Glasgow", "Edinburgh", "Belfast", "Cardiff", "Bristol",
    "Sheffield", "Newcastle", "Nottingham", "Leicester", "Coventry"
]

@app.route("/")
def index():
    # Render an HTML form for selecting cities
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>UK Real-Time Weather App</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>UK Real-Time Weather App</h1>
        <label for="city">Select a City:</label>
        <select id="city">
            """ + "".join(f"<option value='{city}'>{city}</option>" for city in UK_CITIES) + """
        </select>
        <button id="getWeather">Get Weather</button>

        <h2>Weather Information</h2>
        <div id="weatherResult">
            <p>Select a city and click "Get Weather" to see the current weather.</p>
        </div>

        <script>
            $(document).ready(function () {
                $("#getWeather").click(function () {
                    const city = $("#city").val();
                    $("#weatherResult").html("<p>Loading...</p>");
                    $.ajax({
                        url: "/get_weather",
                        type: "POST",
                        contentType: "application/json",
                        data: JSON.stringify({ city: city }),
                        success: function (response) {
                            if (response.success) {
                                const weather = response.weather;
                                $("#weatherResult").html(`
                                    <ul>
                                        <li><strong>City:</strong> ${weather.city}</li>
                                        <li><strong>Temperature:</strong> ${weather.temperature}°C</li>
                                        <li><strong>Humidity:</strong> ${weather.humidity}%</li>
                                        <li><strong>Wind Speed:</strong> ${weather.wind_speed} m/s</li>
                                        <li><strong>Description:</strong> ${weather.description}</li>
                                    </ul>
                                `);
                            } else {
                                $("#weatherResult").html(`<p>Error: ${response.message}</p>`);
                            }
                        },
                        error: function () {
                            $("#weatherResult").html("<p>An error occurred while fetching the weather data.</p>");
                        }
                    });
                });
            });
        </script>
    </body>
    </html>
    """

@app.route("/get_weather", methods=["POST"])
def get_weather():
    city = request.json.get("city")
    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        response.raise_for_status()
        data = response.json()
        return jsonify({
            "success": True,
            "weather": {
                "city": data.get("name"),
                "temperature": data.get("main", {}).get("temp"),
                "humidity": data.get("main", {}).get("humidity"),
                "wind_speed": data.get("wind", {}).get("speed"),
                "description": data.get("weather", [{}])[0].get("description"),
            }
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": str(e)})

def run_app():
    app.run(debug=False, use_reloader=False)
