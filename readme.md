# Pymongo CRUD App
## Setup
### Running this code:
Note: The following steps require Python & Docker to be already installed on your system.

1. Firstly you'll need to clone this repo or download the code and extract it in a local folder.
```
git clone https://github.com/Ln8plus/Pymongo-CRUD-App
```

2. Next we'll be building our docker images. Open a terminal in the cloned folder then to get MongoDB running inside a container use this command:
```
docker run -d -p 27018:27017 --name mongoserver -v ./LocalDataStore/db:/data/db mongo:latest
```

Alternatively if you've already got MongoDB's image in your Docker. You can use the derived container instead.

3. For our web app we'll need to manually build an image and then run it. Building the image is done by:
```
docker build -t pymongo .
```
The above command builds a docker image using the files of the current folder and names it "pymongo".

4. Next run the web app using:
```
docker run -it -p 9000:9000 pymongo
```
This command runs the image in interactive mode and binds port 9000 of the container to our local machine.

5. Optional
If you get an error such as connection refused you'll need to find out the IP address of the MongoDB container and
update the connection string in the client variable in main.py.
To find the IP address of the container you can use docker inspect along with grep:
```
docker inspect <containerName/containerId> | grep IPAddress
```

## API endpoints

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