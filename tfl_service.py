from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

TFL_API_KEY = "YOUR_PRIMARY_KEY_HERE"

@app.route('/tube_status', methods=['GET'])
def get_tube_status():
    url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"
    response = requests.get(url)
    print(f"TfL Status Code: {response.status_code}")
    
    if response.status_code != 200:
        return jsonify({"error": "TfL Error"}), response.status_code

    try:
        data = response.json()
        return jsonify([{"name": l['name'], "status": l['lineStatuses'][0]['statusSeverityDescription']} for l in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/arrivals/<station_id>', methods=['GET'])
def get_arrivals(station_id):
    url = f"https://api.tfl.gov.uk/StopPoint/{station_id}/Arrivals"
    response = requests.get(url)
    data = response.json()
    
    # Sorting and formatting
    arrivals = sorted(data, key=lambda x: x['timeToStation'])[:5]
    results = [{
        "line": t['lineName'],
        "destination": t['destinationName'],
        "minutes": round(t['timeToStation'] / 60)
    } for t in arrivals]
        
    return jsonify(results)

# Ensure there are NO spaces before the lines below
if __name__ == '__main__':
    app.run(debug=True, port=5001)