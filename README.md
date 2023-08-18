# gdsc-demo

This project is a sample API prepared for the purposes of the evaluating project for GDSC evaluation and interview.

## Documentation

### 1. Technologies used

The project employs the following technologies:

1. **FastAPI**: An API framework created in Python. This particular framework was used for its robustness, the in-built validation it achieves with the `Pydantic` package, the ease of use, and speed.

2. **SQLAlchemy**: It is an ORM framework in Python. This was used for its general compatibility with several relational databases and its vast documentation and stability.

3. **sqlite3**: An SQLite database was used as the database for storing data for the API to use. The database file present is named `setup.db`.

4. **Poetry**: Poetry is a dependency management and package operations tool for Python. This particular tool was used for its features of dependency management and its central one command does all system.

### 2. File structure
gdsc-demo/
1. main.py - Main entry point for the API, contains endpoints.
2. models.py - Contains database models for creating database objects.
3. schemas.py - Contains JSON schema objects for data validation.
4. setup.db - SQLite database file.


### 3. Data Modelling

The main entity dealt with in this API is a simple `Product`. The attributes used for it are:

1. **id**: The id of the product; it is an auto-incremented integer primary key.

2. **name**: The name of the product; in SQLite, it is a VARCHAR with no size allocated.

3. **price**: The price of the product; it is a float.

4. **description**: The description of the product; it is a TEXT field.

### 4. API endpoints

The API provides the following endpoints for the product object:

1. **Root**: GET request to the root URL returns a simple message.
   
2. **Token**: POST request to `/token` endpoint returns an access token for authentication.

3. **Get All Products**: GET request to `/products` endpoint returns a list of all products.

4. **Get Product by ID**: GET request to `/products/{product_id}` endpoint returns a single product based on the provided product ID.

5. **Get Current User Information**: GET request to `/me` endpoint returns information about the current user.

6. **Get All Users**: GET request to `/users` endpoint returns a list of all users.

7. **Create User**: POST request to `/users` endpoint allows creating a new user.

The code handles user authentication using OAuth2 and token-based authentication with JWT.
