from flask import Flask, jsonify
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Session, Tasks

app = Flask('app')

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

    
def add_task(task: Tasks):
    try:
        request.session.add(task)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, "user already exists")
    return task

def get_task_all():
    all = request.session.query(Tasks).all()
    return [i.json for i in all]

def get_task(task_id: int):
    return request.session.get(Tasks, task_id)

class TasksView(MethodView):

    def get(self):
        return jsonify(get_task_all())

    def post(self):
        task = Tasks(**request.json)
        add_task(task)
        return jsonify({'id': task.id})

class OneTaskView(MethodView):

    def get(self, task_id):
        task = get_task(task_id)
        if task is None:
            return jsonify({'error': 'article is not found'})
        return jsonify(task.json)
    
    def put(self, task_id):
        task = get_task(task_id)
        json_data = request.json
        for field, value in json_data.items():
            setattr(task, field, value)
        add_task(task)
        return jsonify(task.json)

    def delete(self, task_id):
        task = get_task(task_id)
        request.session.delete(task)
        request.session.commit()
        return jsonify({'delete':f'id: {task_id}'})

task_view = TasksView.as_view('task_view')
task_one_view = OneTaskView.as_view('task_one_view')

app.add_url_rule('/tasks', view_func=task_view, methods=['GET','POST'])
app.add_url_rule('/tasks/<int:task_id>', view_func=task_one_view, methods=['GET','PUT', 'DELETE'])

app.run()