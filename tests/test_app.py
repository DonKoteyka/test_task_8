import pytest
import json

data_2 = {'title': 'Second Task', 'description': 'This is a Second task'}
data_3 = {'title': 'Third Task', 'description': 'This is a Third task'}

def test_put_create_task(client):
    response = client.post('/tasks', data=json.dumps(data_3), content_type='application/json')
    task_id = response.get_json()['id']
    data_put = {'title': 'Test Put', 'description': 'This is a test task'}
    client.put(f'/tasks/{task_id}', data=json.dumps(data_put), content_type='application/json')
    response_get_new = client.get(f'/tasks/{task_id}')
    assert response_get_new.status_code == 200
    assert response_get_new.get_json()['title'] == data_put['title']

def test_delete_create_task(client):
    response = client.post('/tasks', data=json.dumps(data_2), content_type='application/json')
    task_id = response.get_json()['id']
    response_delete = client.delete(f'/tasks/{task_id}')
    assert response_delete.status_code == 200
    assert response_get_new.get_json()['delete'] == f'id: {task_id}'







