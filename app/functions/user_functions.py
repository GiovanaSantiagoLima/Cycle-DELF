from datetime import datetime
from bson import ObjectId
from app.database import users_collection

# CREATE USER
def create_user(user: dict):
    user["created_at"] = datetime.now()
    user["level"] = user.get("level", "A1")  # nível padrão
    users_collection.insert_one(user)
    return {"message": "Usuário criado com sucesso"}

# READ USERS
def get_users():
    return list(users_collection.find({}, {"_id": 0}))

# UPDATE USER
def update_user(user_id: str, data: dict):
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": data}
    )

    if result.modified_count == 1:
        return {"message": "Usuário atualizado com sucesso"}

    return {"message": "Nenhum usuário atualizado"}

# DELETE USER
def delete_user(user_id: str):
    result = users_collection.delete_one(
        {"_id": ObjectId(user_id)}
    )

    if result.deleted_count == 1:
        return {"message": "Usuário deletado com sucesso"}

    return {"message": "Usuário não encontrado"}
