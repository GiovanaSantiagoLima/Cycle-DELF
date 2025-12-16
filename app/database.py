from pymongo import MongoClient

MONGO_URI = MONGO_URI = "mongodb+srv://admin:8B7OWtWdBky2KvOm@cluster0.k9ycyvh.mongodb.net/cycledelf?retryWrites=true&w=majority"


client = MongoClient(MONGO_URI)

db = client["cycledelf"]

users_collection = db["users"]
sessions_collection = db["sessions"]

