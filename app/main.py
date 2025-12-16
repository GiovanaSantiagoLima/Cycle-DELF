from fastapi import FastAPI
from app.functions.user_functions import (
    create_user,
    get_users,
    update_user,
    delete_user)
from app.functions.session_functions import (
    create_session,
    get_sessions,
    update_session,
    delete_session)
from app.funcionalidade import(
    start_session, 
    get_cycle_status,
    finish_session)

app = FastAPI(title="Cycle DELF API")

# ---------- USERS ----------
@app.post("/users")
def create_user_route(user: dict):
    return create_user(user)

@app.get("/users")
def get_users_route():
    return get_users()

@app.put("/users/{user_id}")
def update_user_route(user_id: str, data: dict):
    return update_user(user_id, data)

@app.delete("/users/{user_id}")
def delete_user_route(user_id: str):
    return delete_user(user_id)


# ---------- SESSIONS ----------
@app.post("/sessions/{user_id}")
def create_session_route(user_id: str):
    return create_session(user_id)

@app.get("/sessions/{user_id}")
def get_sessions_route(user_id: str):
    return get_sessions(user_id)

@app.put("/sessions/{session_id}")
def update_session_route(session_id: str, data: dict):
    return update_session(session_id, data)

@app.delete("/sessions/{session_id}")
def delete_session_route(session_id: str):
    return delete_session(session_id)

# ---------- FUNCIONALIDADE ----------
@app.post("/sessions/start/{user_id}")
def start_session_route(user_id: str):
    return start_session(user_id)

@app.get("/cycle/status/{user_id}")
def cycle_status_route(user_id: str):
    return get_cycle_status(user_id)

@app.put("/sessions/finish/{session_id}")
def finish_session_route(session_id: str):
    return finish_session(session_id)


