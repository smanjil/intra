
import pytest

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_create():
    users = len(client.get('/').json())
    response = client.post("/create", json={"fname": "Manjil", "lname": "Shrestha", 
                                            "email": "shresthamanjil21@gmail.com"})
    
    assert response.status_code == 200
    assert response.json() == {f"{users + 1}": {"fname": "Manjil", "lname": "Shrestha", 
                                            "email": "shresthamanjil21@gmail.com"}}
    
    
def test_get():
    response = client.get("/")
    
    assert len(response.json()) == 1
    
    
def test_update():
    response = client.put("/update/1", json={"email": "test@gmail.com"})
    
    assert response.json()['1']['email'] == 'test@gmail.com'
    

def test_delete():
    response = client.delete("/delete/1")
    
    assert len(response.json()) == 0
