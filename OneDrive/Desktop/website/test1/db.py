from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import variable
print(variable.password)
uri = variable.password
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["user_database"]
medecine_collection= db["medicines"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
for medicine in medecine_collection.find():
    print("Name:", medicine.get("med_name"))
    print("Time:", medicine.get("time"))
    print("Rest of the data:", {k: v for k, v in medicine.items() if k not in ["name", "time"]})