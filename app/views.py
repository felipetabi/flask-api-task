from flask import Blueprint
from flask import request
from .models.task import Task

from .responses import response, not_found, bad_request

from .schemas import task_schema, tasks_schema, params_task_schema

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

def set_task(function):
    def wrap(*args, **kwargs):
        print("Entramos al decorador!!!")
        id = kwargs.get('id', 0)
        task = Task.query.filter_by(id=id).first()

        if task is None:
            return not_found()
        
        return function(task)

    wrap.__name__ = function.__name__
    return wrap    
@api_v1.route('/tasks', methods=['GET'])
def get_tasks():
    page = int(request.args.get('page', 1)) #Dic
    order = request.args.get('order', 'desc')
    #print(page)
    tasks = Task.get_by_page(order, page)

    return response(tasks_schema.dump(tasks))

@api_v1.route('/tasks/<id>', methods=['GET'])
@set_task
def get_task(task):
    return response(task_schema.dump(task))

@api_v1.route('/tasks', methods=['POST'])
def create_task():
    json = request.get_json(force=True)

    error = params_task_schema.validate(json)
    if error:
        print(error)
        return bad_request()
    
    task = Task.new(json['title'], json['description'], json['deadline'])
    if task.save():
        return response(task_schema.dump(task))
    
    return bad_request()

@api_v1.route('/tasks/<id>', methods=['PUT'])
@set_task
def update_task(task):
    
    json = request.get_json(force=True)

    task.title = json.get('title', task.title)
    task.description = json.get('description', task.description)
    task.deadline = json.get('deadline', task.deadline)

    if task.save():
        return response(task_schema.dump(task))
    
    return bad_request()


@api_v1.route('/tasks/<id>', methods=['DELETE'])
@set_task
def delete_task(task):
    
    if task.delete():
        return response(task_schema.dump(task))
    
    return bad_request()