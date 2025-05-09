from flask import Blueprint, request, jsonify
from app import db
from app.models import Project, Task

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Project name is required'}), 400
    project = Project(name=name)
    db.session.add(project)
    db.session.commit()
    return jsonify({'id': project.id, 'name': project.name}), 201

@projects_bp.route('/', methods=['GET'])
def list_projects():
    projects = Project.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in projects])

@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({'id': project.id, 'name': project.name})

@projects_bp.route('/<int:project_id>/tasks', methods=['GET'])
def list_project_tasks(project_id):
    tasks = Task.query.filter_by(project_id=project_id).all()
    return jsonify([{'id': t.id, 'title': t.title, 'status': t.status.value} for t in tasks])