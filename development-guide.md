
# Book API for Wookies

REST APIs created using Django Rest Framework

## Features

- New users registration 
- Login to get the JWT token
- GET (List/Detail) books without authentication
- List resource searchable with query parameters
- CRUD operations for this resource
- Endpoint to unpublish a book (DELETE)
- Unit test and API tests
- Schema based validation testing

## Project setup in local env

Clone the Project Repo

```bash
  mkdir <name>
  cd <name>
  git clone http://aidhere-gmbh-rfhzza@git.codesubmit.io/aidhere-gmbh/book-api-for-wookies-gzlaiu
```
Create virtual environment(Ubuntu, Mac)

```bash
  python3 -m venv <name>
```
Activate virtual environment
```bash
  source <name>/bin/activate
```
Install project dependencies
```bash
  pip install -r requirements.txt
```
Migrate
```bash
  cd wookie_books/
  python manage.py migrate
```
Run the application
```bash
  python manage.py runserver
```
To test users app
```bash
  python manage.py test users.tests 
```
To test bookstore app
```bash
  python manage.py test bookstore.tests 
```


## List of APIs

* User registration:
```bash
    Method: POST
    
    URL: http://localhost:8000/users/register/
	
    payload: {
        'username':<username>,
        'password':<password>,
        'author_pseudonym':<pen_name>
    }
```
* User login:
```bash
    Method: POST
    
    URL: http://localhost:8000/users/login/
	
    payload: {
        'username':<username>,
        'password':<password>		
    }

    You will get the token.
```
* List all users:
```bash
    Method: GET
    
    URL: http://localhost:8000/users/list/
	
    Headers: Add a new key-value pair:
    
    Key: "Authorization", Value: "Bearer [your_token]"

```
* List/Detail books without authentication:
```bash
    Method: GET
    
    URL: http://localhost:8000/api/books/
	
```
* Search books:
```bash
    Method: GET
    
    URL: http://127.0.0.1:8000/api/books/?search=your_search_term
	
    Replace "your_search_term" with the term you want to search for.

```
* List my books:
```bash
    Method: GET
    
    URL: http://localhost:8000/api/my_books/
    
    Headers: Add a new key-value pair:
    
    Key: "Authorization", Value: "Bearer [your_token]"

```
* Create a book (my books):
```bash
    Method: POST
    
    URL: http://localhost:8000/api/my_books/
	
    Headers: Add a new key-value pair:
    
    Key: "Authorization", Value: "Bearer [your_token]"
    
    Body: Select "form-data", and add the required key-value pairs (e.g., title, description, cover_image, price).
```
* Retrieve a book (my books):
```bash
    Method: GET
    
    URL: http://localhost:8000/api/my_books/[book_id]/
    
    Headers: Add a new key-value pair:
    
    Key: "Authorization", Value: "Bearer [your_token]"

    Replace "[book_id]" with the ID of the book you want to retrieve.
```
* Update a book (my books)::
```bash
    Method: PUT or PATCH
    
    Url: http://localhost:8000/api/my_books/update/[book_id]/
	
    Replace "[book_id]" with the ID of the book you want to update.
    
    Headers: Add a new key-value pair:

    Key: "Authorization", Value: "Bearer [your_token]"

    Body: Select "form-data", and add the key-value pairs for the fields you want to update (e.g., title, description, cover_image, price).
```
*  Delete a book (unpublish) (my books):
```bash
    Method: DELETE
    
    Url: http://localhost:8000/api/my_books/unpublish/[book_id]/
    
    Headers: Add a new key-value pair:
    
    Key: "Authorization", Value: "Bearer [your_token]"
	
    Replace "[book_id]" with the ID of the book you want to delete.
```
*  List user's unpublished books (my unpublished books):
```bash
    Method: GET
    
    Url: http://localhost:8000/api/my_books/list_unpublish/
	
    Headers: Add a new key-value pair:

    Key: "Authorization", Value: "Bearer [your_token]"
```
*  Bonus:- "Darth Vader" is unable to publish his work on Wookie Books:
```bash
    Method: POST
    
    Url: http://localhost:8000/api/my_books/
	
    Headers: Add a new key-value pair:

    Key: "Authorization", Value: "Bearer [your_token]"
    
    Body: Select "form-data", and add the key-value pairs for the fields you want to update (e.g., title, description, cover_image, price).
```


## Production Setup:

We have organized the project settings into a dedicated folder named "settings" inside the wookie_books directory. This folder contains three separate Python files for base, development, and production environment configurations.

We recommend creating a ".env" file at the project's root level to manage sensitive environment variables.

To set the DEBUG environment variable for development and production, modify it inside the ".env" file.

The "manage.py" file handles the logic for differentiating the development and production environments.

For development, I have utilized the SQLite3 database, and for production, I have used the PostgreSQL database.