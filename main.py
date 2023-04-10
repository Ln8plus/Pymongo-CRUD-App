from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient
from hashlib import sha256


app = Flask(__name__)
api = Api(app)



localMongoPort = 27017
localHostName = "localhost"
containerHostName = "172.17.0.2"
client = MongoClient("mongodb://172.17.0.2:27017")



db = client["LocalMongoDBServer"]
collections = db["FlaskAPI"]





class User(Resource):

    #Fetch all users. 
    def get(self, id = None):
        try:
            response = []
            if id:               
                user = collections.find_one({"id":id})
                user_records = {"id":user["id"], "name":user["name"], "email":user["email"], "password":user["password"]}
                response.append(user_records)

            else:
                users = collections.find()
                for user in users:
                    user_records = {"id":user["id"], "name":user["name"], "email":user["email"], "password":user["password"]}
                    response.append(user_records)


        except Exception as e:
            response = f"The following error has occurred: : {str(e)}"
        return jsonify({"response":response})





    #Create one user.
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("id", type = str, required = True)
            parser.add_argument("name", type = str, required = True)
            parser.add_argument("email", type = str, required = True)
            parser.add_argument("password", type = str, required = True)
            args = parser.parse_args()

            id = args["id"]
            name = args["name"]
            email = args["email"]
            password = args["password"]


            hash_obj_1 = sha256()
            hash_obj_1.update(str.encode(password))
            hashed_pwd = hash_obj_1.hexdigest()
            


            payload = {"id":id, 
                       "name":name, 
                       "email":email, 
                       "password":hashed_pwd}

            if collections.find_one({"id":id}) is not None:
                    return jsonify(f"User with {id} can't be created as their id already exists.")
            
        
            collections.insert_one(payload)
            response = f"User with {payload['id']}'s records have been added successfully."

        except Exception as e:
            response = f"The following error has occurred: {str(e)}"
        return jsonify(response)





    #Update user by id with new data.
    def put(self, id = None):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type = str, required = False, location = "json")
            parser.add_argument("email", type = str, required = False, location = "json")
            parser.add_argument("password", type = str, required = False, location = "json")
            args = parser.parse_args()

            if args["name"] is None and args["email"] is None and args["password"] is None:
                return jsonify({"No records for updatation have been provided."})

            filter = {"id":id}

            update = {}
            if args["name"] is not None:
                update["name"] = args["name"]

            if args["email"] is not None:
                update["email"] = args["email"]

            if args["password"] is not None:
                hash_obj_2 = sha256()
                hash_obj_2.update(str.encode(args["password"]))
                new_hashed_pwd = hash_obj_2.hexdigest()
                update["password"] = new_hashed_pwd


            new_records = {"$set":update}
            collections.update_one(filter, new_records)
            response = f"User {id}'s records have been updated successfully."

        except Exception as e:
            response = f"The following error has occurred: {str(e)}"
        return jsonify(response)




    #Delete user by id.
    def delete(self, id = None):
        try:
            id = int(id)
            if id is None:
                return jsonify({"User id can't be none."})
            
            if collections.find_one({"id":id}) is None:
                return jsonify(f"User with {id} not found.")
            
            collections.delete_one({"id":id})
            response = f"User {id}'s records have been deleted successfully."

        except Exception as e:
            response = f"The following error has occurred: {str(e)}"
        return jsonify(response)



api.add_resource(User, "/users", endpoint="users")
api.add_resource(User, "/users/<id>", endpoint="user")



if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = 9000)