from flask import Flask, jsonify
from flask import request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
import pydantic


from schema import CreateTask, UpdateTask
from models import Session, Tasks

app = Flask('app')

def validate(schema_class, json_data):
    '''Функция валидации данных для методов POST и PUT'''
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)

@app.before_request
def before_request():
    '''Открытие сессии записи данных в БД'''
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    '''Закрытие сессии данных в БД после выполнения запроса'''
    request.session.close()
    return response

class HttpError(Exception):
    '''Класс для вызова ошибок'''
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

    
def add_task(task: Tasks):
    '''Добавление записей в БД, в случае дублирования выдаёт стандартную ошибку'''
    try:
        request.session.add(task)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, "user already exists")
    return task

def get_task_all():
    '''Получение всех записей из БД'''
    all = request.session.query(Tasks).all()
    return [i.json for i in all]

def get_task(task_id: int):
    '''Получение одной записи из БД по id'''
    return request.session.get(Tasks, task_id)

class TasksView(MethodView):
    '''Класс для обработки запросов по url /tasks'''

    def get(self):
        '''Функция предоставления http ответа на запрос всех записей из таблицы Task'''
        return jsonify(get_task_all())

    def post(self):
        '''Функция валидации и добавление даписей в Task от http запроса'''
        json_data = validate(CreateTask, request.json)
        task = Tasks(**json_data)
        add_task(task)
        return jsonify({'id': task.id})

class OneTaskView(MethodView):
    '''Класс для обработки запросов по url /tasks/<int:task_id>'''

    def get(self, task_id):
        '''Функция предоставления http ответа на запрос записи из таблицы Task по id'''
        task = get_task(task_id)
        if task is None:
            return jsonify({'error': 'article is not found'})
        return jsonify(task.json)
    
    def put(self, task_id):
        '''Функция валидации и изменеия записи в таблице Task'''
        task = get_task(task_id)
        json_data = validate(UpdateTask, request.json)
        for field, value in json_data.items():
            setattr(task, field, value)
        add_task(task)
        return jsonify(task.json)

    def delete(self, task_id):
        '''Функция удаления записи в таблице Task'''
        task = get_task(task_id)
        request.session.delete(task)
        request.session.commit()
        return jsonify({'delete':f'id: {task_id}'})

task_view = TasksView.as_view('task_view')
task_one_view = OneTaskView.as_view('task_one_view')

'''доступные url'''
app.add_url_rule('/tasks', view_func=task_view, methods=['GET','POST'])
app.add_url_rule('/tasks/<int:task_id>', view_func=task_one_view, methods=['GET','PUT', 'DELETE'])

app.run()