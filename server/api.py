from flask import Flask, current_app, jsonify

app = Flask(__name__)

@app.route('/start-recording', methods=['POST'])
def start_recording():
    queue = current_app.config.get('shared_queue')
    json_obj = {
        "data": "start_recording",
        "command": "update_recording_status"
    }
    queue.put(json_obj)
    return jsonify(json_obj), 200

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    queue = current_app.config.get('shared_queue')
    json_obj = {
        "data": "stop_recording",
        "command": "update_recording_status"
    }
    queue.put(json_obj)
    return jsonify(json_obj), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)