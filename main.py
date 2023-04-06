from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from hashlib import sha256

'''
Local Connections
app = Flask(__name__)
client = MongoClient()
db = client.LocalMongoDBServer
collections = db.FlaskAPI
'''


app = Flask(__name__)
client = MongoClient(host = 'mongodb', port = 27017)
db = client["SampleDB"]
collections = db.SampleCollection




#Fetch all users. 
@app.route('/users', methods = ['GET'])
def fetchAllUsers():
    try:
        response = list()
        user_records = collections.find({},{"_id":0,"name":1})

        for user in user_records:
            response.append(user)
        response = dumps(response, indent = 1)

    except Exception as e:
        response = jsonify({"The following error has occurred: ": str(e)})
    return response



#Get records of user by id.
@app.route('/users/<id>', methods = ['GET'])
def fetchUserRecords(id=None):
    try:
        if id is None:
            return jsonify({"User id can't be none."})
        
        response = list()
        user_records = collections.find_one({"id":id})

        if user_records is None:
            return jsonify(f"User with {id} doesn't exist.")
        
        response.append(user_records)
        response = dumps(response, indent = 1)

    except Exception as e:
        response = jsonify({"The following error has occurred: ": str(e)})
    return response







#Create one user.
@app.route('/users', methods = ['POST'])
def createUser():
    try:
        user = request.json

        if collections.find_one({"id":user['id']}) is not None:
                return jsonify(f"User with {user['id']} can't be created as their id already exists.")
        
        hash_obj_1 = sha256()
        hash_obj_1.update(str.encode(user['password']))
        hashed_pwd = hash_obj_1.hexdigest()

        payload = {
            "id":user['id'],
            "name":user['name'],
            "email":user['email'],
            "password":hashed_pwd
        }
    
        collections.insert_one(payload)
        response = f"User with {user['id']}'s records have been added successfully."

    except Exception as e:
        response = f"The following error has occurred: {str(e)}"
    return jsonify(response)






#Update user by id with new data.
@app.route('/users/<id>', methods = ['PUT'])
def updateUserRecords(id=''):
    try:
        if id == '':
            return jsonify({"User id can't be none."})
        
        if collections.find_one({"id":id}) is None:
                return jsonify(f"User with {id} can't be deleted as they don't exist.")

        filter = {"id":id}
        new_info = request.json
        

        update = {}
        if 'name' in new_info and new_info['name'] is not None:
            update['name'] = new_info['name']

        if 'email' in new_info and new_info['email'] is not None:
            update['email'] = new_info['email']

        if 'password' in new_info and new_info['password'] is not None:
            hash_obj_2 = sha256()
            hash_obj_2.update(str.encode(new_info['password']))
            new_hashed_pwd = hash_obj_2.hexdigest()
            update['password'] = new_hashed_pwd


        new_records = {"$set":update}
        collections.update_one(filter, new_records)
        response = f"User {id}'s records have been updated successfully."

    except Exception as e:
        response = f"The following error has occurred: {str(e)}"
    return jsonify(response)






#Delete user by id.
@app.route('/users/<id>', methods = ['DELETE'])
def deleteUserId(id=''):
    try:
        if id == '':
            return jsonify({"User id can't be none."})
        
        if collections.find_one({"id":id}) is None:
            return jsonify(f"User with {id} not found.")
        
        collections.delete_one({"id":id})
        response = f"User {id}'s records have been deleted successfully."

    except Exception as e:
        response = f"The following error has occurred: {str(e)}"
    return jsonify(response)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=9000)