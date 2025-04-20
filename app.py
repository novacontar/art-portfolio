from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# Simple in-memory database for demo purposes
# In a real app, you would use a proper database
projects = [
    {
        "id": 1,
        "title": "Ocean Dreams",
        "description": "A series of paintings exploring the depths of the ocean.",
        "category": "Painting",
        "date_created": "2025-01-15",
        "featured": True,
        "images": ["ocean1.jpg", "ocean2.jpg"]
    },
    {
        "id": 2,
        "title": "Urban Landscapes",
        "description": "Photography project capturing city life.",
        "category": "Photography",
        "date_created": "2024-11-20",
        "featured": False,
        "images": ["urban1.jpg"]
    }
]

# Root route - API info
@app.route('/')
def home():
    return jsonify({
        "message": "Artist Portfolio API",
        "version": "1.0",
        "endpoints": [
            "/api/projects",
            "/api/projects/<id>"
        ]
    })

# Get all projects
@app.route('/api/projects', methods=['GET'])
def get_projects():
    # Filter by category if provided
    category = request.args.get('category')
    if category:
        filtered_projects = [p for p in projects if p['category'].lower() == category.lower()]
        return jsonify(filtered_projects)
    
    # Return all projects
    return jsonify(projects)

# Get a specific project
@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = next((p for p in projects if p['id'] == project_id), None)
    if project:
        return jsonify(project)
    return jsonify({"error": "Project not found"}), 404

# Create a new project
@app.route('/api/projects', methods=['POST'])
def create_project():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Invalid project data"}), 400
    
    new_project = {
        "id": max(p['id'] for p in projects) + 1 if projects else 1,
        "title": request.json['title'],
        "description": request.json.get('description', ''),
        "category": request.json.get('category', 'Other'),
        "date_created": request.json.get('date_created', datetime.now().strftime('%Y-%m-%d')),
        "featured": request.json.get('featured', False),
        "images": request.json.get('images', [])
    }
    
    projects.append(new_project)
    return jsonify(new_project), 201

# Update a project
@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    if not request.json:
        return jsonify({"error": "Invalid project data"}), 400
    
    project['title'] = request.json.get('title', project['title'])
    project['description'] = request.json.get('description', project['description'])
    project['category'] = request.json.get('category', project['category'])
    project['featured'] = request.json.get('featured', project['featured'])
    project['images'] = request.json.get('images', project['images'])
    
    return jsonify(project)

# Delete a project
@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    global projects
    project = next((p for p in projects if p['id'] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    projects = [p for p in projects if p['id'] != project_id]
    return jsonify({"message": "Project deleted"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
