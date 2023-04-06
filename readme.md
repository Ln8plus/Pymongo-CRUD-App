## Pymongo CRUD App
- This is a web app made using flask for performing CRUD operations on a mongoDB instance.


### Setup
#### Running Locally:
1. Firstly you'll need to clone this repo or download the code and extract it in a local folder.

```
git clone https://github.com/Ln8plus/Pymongo-CRUD-App
```


2. Create a venv for storing project dependencies:

```
virtualenv -p /usr/bin/python3.10 venv
```

Activate the venv on Linux by using:
```
source venv/bin/activate
```

Alternatively on Windows you might use:

```
venv\Scripts\activate
```


3. Next install required dependencies from the requirements.txt

```
pip install -r requirements.txt
```

4. Next install mongoDB and setup a database for using the app. Installation steps can be found in the link below.

```
https://www.mongodb.com/docs/manual/administration/install-community/
```

After setting up the mongoDB instance on your machine be sure to add their names to the main.py file.

```
db = client.<MongoDB-databasename>
collections = db.<CollectionName>
```
Be sure to uncomment the code in the main.py file and comment/remove the code below it if you're going to run everything locally.


5. Finally to run locally you'll need to use waitress on Windows or gunicorn if you're on Linux as the initiation command. 

Waitress command (Windows):

```
waitress-serve --host 127.0.0.1 main:app
```
Be sure to remember the port as you might need it while using the app, then you will need to add it at the end of your localhost address such as 127.0.0.1:8080


Gunicorn command (Linux):

```
gunicorn -w 4 -b "127.0.0.1:9000" main:app
```

You can us either a browser or a testing tool such as Postman to interact with the app.


#### Running with Docker:
You can either build a image with:

```
docker compose up
```

This command will build an image with a mongoDB instance and the repo code running simultaneously. 

Or pull my image and run it instead of building your own: 
```
https://hub.docker.com/r/ln8plus/pymongoapp-app
```

You will need to run these commands to pull the image and then run it as a container.
```
docker pull ln8plus/pymongapp-app
docker run -it pymongoapp
```


### API endpoints

- GET Return names of all users.
```
http://127.0.0.1:9000/users
```
![image](https://drive.google.com/uc?export=view&id=1GoM8LstqGKh9UdUKkF4QiOMvMY7bXDWx)

- GET Records of a single user by id.
```
http://127.0.0.1:9000/users/<id>
```
![image](https://drive.google.com/uc?export=view&id=1WJ4k0aHGQMEy9uk3PYo7yR-cU575BXea)

- POST Add new user's records to the database.
```
http://127.0.0.1:9000/users
```
User data will have to be supplied as a json file in the body of the POST request.

eg.
```
{
    "id": "001",
    "name": "ABC",
    "email": "abc@abc.com",
    "password": "password1234"
}
```
![image](https://drive.google.com/uc?export=view&id=1adClhqVzX2BPXb9whdIe8p8TUdzACMQx)

- PUT Update user records by id.
```
http://127.0.0.1:9000/users/<id>
```
New records will have to be supplied as a json file in the body of the PUT request.

eg.
```
{
    "password": "331463StrongerpassworD->"
}
```
![image](https://drive.google.com/uc?export=view&id=1YY5Vp-uJ0_FS5Xce5sLU3wc8--yok-xv)

- DELETE Delete user records by id.
```
http://127.0.0.1:9000/users/<id>
```
![image](https://drive.google.com/uc?export=view&id=1kYomGLJSH6eDvFhC5V1nmvRBhQwZeuPs)