# url-shortner-poc

## Functional Features

On the functional level, there are two basic categorization - User authentication service, and Short URL Creation service.

## User Authentication Service
- Django application - Handles User CRUD operation. 
- Database - Postgres (Stores User data like ID, Name)
- Authentication - Using JSON Web Tokens.

### USER Endpoints
* /api/token/
   * POST
* /api/register/
   * POST
* /api/user/{id}
   * GET, POST, PUT, DELETE

### User Model
![image](https://user-images.githubusercontent.com/4581090/160870372-731ad5d9-c602-4f6b-be1f-9c7592152ca0.png)

## Short URL Service
- Flask application - Handles two operation - creation of short URL, and redirection using Short URL.
  - Short URL Creation endpoint is only available to authenticated users. 
  - Authentication handled by the `User Authentication Service`
  - Database - MongoDB 
## Features
### Create a Short URL
- Create a short link given any link of arbitrary length 
  -  example, The URL `https://github.com/jahandaniyal` is shortened to `<BASE_URL>/shortly/XvBaW`  
   
