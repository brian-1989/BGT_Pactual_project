from app.config import Settings
from pymongo import mongo_client

client = mongo_client.MongoClient(Settings.DATABASE_URL)
db = client[Settings.MONGO_INITDB_DATABASE]

Users = db.Users
Funds = db.Funds
Transactions = db.Transactions
