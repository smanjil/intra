
from fastapi import FastAPI
from typing import Dict


app = FastAPI()

users = dict()


@app.get('/')
async def list_all():
    return users
    
    
@app.post('/create')
async def create_user(user: Dict):
    users[len(users) + 1] = user
    
    return users


@app.put('/update/{user_id}')
async def update_user(user_id: int, value: Dict):
    try:
        users[user_id].update(value)
    except:
        raise KeyError(f"User {user_id} not available.")

    return users


@app.delete('/delete/{user_id}')
async def delete_user(user_id: int):
    try:
        del users[user_id]
    except:
        raise KeyError(f"User {user_id} not available.")

    return users
