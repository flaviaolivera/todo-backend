from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

# In-memory task list
tasks = [
    {"id": str(uuid.uuid4()), "title": "Task One", "status": "open"},
    {"id": str(uuid.uuid4()), "title": "Task Two", "status": "completed"}
]

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    status = data.get('status', 'open')

    if not title:
        return jsonify({"error": "Title is required"}), 400

    if status not in ['open', 'in_progress', 'completed']:
        status = 'open'

    new_task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "status": status
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Update an existing task
@app.route('/tasks/<task_id>', methods=['PATCH'])
def update_task(task_id):
    data = request.json
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            if data.get("status") in ["open", "in_progress", "completed"]:
                task["status"] = data["status"]
            return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

# Delete a task
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
