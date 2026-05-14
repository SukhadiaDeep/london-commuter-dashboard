from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Replace with your actual key later
TFL_API_KEY = "YOUR_PRIMARY_KEY_HERE"

@app.route('/tube_status', methods=['GET'])
def get_tube_status():
    # 1. Check if the URL works without a key first (TfL allows limited hits)
    url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"
    
    response = requests.get(url)
    
    # 2. Check the status code (200 is good, 401/403 means Key issue)
    print(f"TfL Response Code: {response.status_code}")
    
    if response.status_code != 200:
        return jsonify({"error": f"TfL returned error {response.status_code}"}), response.status_code

    try:
        data = response.json()
        status_list = []
        for line in data:
            status_list.append({
                "name": line['name'],
                "status": line['lineStatuses'][0]['statusSeverityDescription']
            })
        return jsonify(status_list)
    except Exception as e:
        print(f"Data Error: {e}")
        return jsonify({"error": "Failed to parse TfL data"}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5001)