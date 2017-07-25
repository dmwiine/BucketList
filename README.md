# BucketList API in Flask microframework.


[![Build Status](https://travis-ci.org/dmwiine/BucketList.svg?branch=develop)](https://travis-ci.org/dmwiine/BucketList)
[![Coverage Status](https://coveralls.io/repos/github/dmwiine/BucketList/badge.svg?branch=develop)](https://coveralls.io/github/dmwiine/BucketList?branch=develop)

API Documentation:

https://donna-bucketlist.herokuapp.com/

## What is a Bucketlist?

A bucketlist is a list of things one wishes to accomplish before they die.

## The Bucketlist API

In this project, I set out to create a RESTful API that will create, update, delete and edit bucketlists.
The API is developed using the Flask framework.


## Installation and Setup.


1. Clone the repository.

    ``` $ git clone https://github.com/dmwiine/BucketList ```

2. cd into the newly created file folder.

    ``` $ cd Bucketlist ```

3. Create a ***virtual environment*** and activate it.

    ``` 
    $ virtualenv <virtual environment name> 
    $ source <virtual environment name>/bin/activate
    ```

4. Install the API dependencies.

    ``` $ pip install -r requirements.txt``` 



**Setup a Database:**

Install postgres 

``` $ brew install postgresql```

You can skip the above step if you already have postgresql installed.

1. In your terminal, run: 

    ``` $ psql postgres```

2. Create the database:

    ``` # CREATE DATABASE flask_api;```

    ```note: the above command is case sensitive.```

3. Exit the postgres.
    
    ``` # \q```


**Run the Migrations**:

```$ python manage.py db init```

```$ python manage.py db migrate```

```$ python manage.py db upgrade```

Don't fret. One more step and we are done.

To run the application, run:

```$ flask run```

> The command above runs the application on:[http://127.0.0.1:5000] 

## Supported Endpoints

|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `/api/v1/auth/register/` |  Registering a user. |
|POST| `/api/v1/auth/login/` | Logging in a user.|
|POST| `/api/v1/bucketlists/` | Creates a new bucketlist. |
|POST| `/api/v1/bucketlists/<int:id>/items/` | Adds a new item to the bucketlist with the give id. |
|GET| `/api/v1/bucketlists/` | Retrieves all bucketlists created by a given user. |
|GET| `/api/v1/bucketlists/<int:id>` | Retrieves a single bucketlist of the given ID. |
|GET| `/api/v1/bucketlists?limit=20` | Supports pagination. Specify the number of results you would like to have via a GET parameter **limit**.|
|GET| `/api/v1/bucketlists?q=` | Supports search by name. Search for bucket lists based on the name using a GET parameter **q**.
|PUT| `/api/v1/bucketlists/<int:id>` | Updates a single bucketlist of the given ID. |
|DELETE|`/api/v1/bucketlists/<int:id>` | Deletes a single bucketlist of the give ID. |
