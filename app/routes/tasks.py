from flask import Blueprint, request, jsonify
from app import db
from app.models import Task, Project, User, StatusEnum

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    project_id = data.get('project_id')
    user_id = data.get('user_id')
    dependency_ids = data.get('dependencies', [])

    if not title or not project_id:
        return jsonify({'error': 'Title and project_id are required'}), 400

    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    if user_id and not User.query.get(user_id):
        return jsonify({'error': 'Assigned user not found'}), 404

    task = Task(title=title, description=description, project_id=project_id, user_id=user_id)

    # Add dependencies if valid
    for dep_id in dependency_ids:
        dep_task = Task.query.get(dep_id)
        if not dep_task:
            return jsonify({'error': f'Dependency task {dep_id} not found'}), 404
        if dep_task.id == task.id:
            return jsonify({'error': 'Task cannot depend on itself'}), 400
        task.dependencies.append(dep_task)

    db.session.add(task)
    db.session.commit()

    return jsonify({'id': task.id, 'title': task.title, 'status': task.status.value}), 201

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status.value,
        'project_id': task.project_id,
        'user_id': task.user_id,
        'dependencies': [d.id for d in task.dependencies]
    })

@tasks_bp.route('/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in StatusEnum.__members__:
        return jsonify({'error': 'Invalid status'}), 400

    # Check dependencies before marking completed
    if new_status == 'COMPLETED':
        for dep in task.dependencies:
            if dep.status != StatusEnum.COMPLETED:
                return jsonify({'error': f'Task depends on task {dep.id} which is not completed'}), 400

    task.status = StatusEnum[new_status]
    db.session.commit()

    return jsonify({'id': task.id, 'status': task.status.value})

@tasks_bp.route('/user/<int:user_id>', methods=['GET'])
def list_user_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': t.id, 'title': t.title, 'status': t.status.value} for t in tasks])

@tasks_bp.route('/status/<status>', methods=['GET'])
def list_tasks_by_status(status):
    try:
        status_enum = StatusEnum[status.upper()]
    except KeyError:
        return jsonify({'error': 'Invalid status'}), 400

    tasks = Task.query.filter_by(status=status_enum).all()
    return jsonify([{'id': t.id, 'title': t.title, 'status': t.status.value} for t in tasks])