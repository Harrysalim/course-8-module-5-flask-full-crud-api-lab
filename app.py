from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([e.to_dict() for e in events]), 200

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400
    
    new_id = max((e.id for e in events), default = 0) + 1
    event = Event(new_id, title.strip())
    events.append(event)
    return jsonify(event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error":"Event not found "}), 404
    
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    event.title = title.strip()
    return jsonify(event.to_dict()), 200 

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    
    events.remove(event)
    return "", 204

def find_event(event_id):
    return next((e for e in events if e.id == event_id), None)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Method not allowed" }), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == "__main__":
    app.run(debug=True)
