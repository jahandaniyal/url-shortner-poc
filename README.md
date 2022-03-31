# url-shortner-poc

# Proposed Architecture

![asd drawio (2)](https://user-images.githubusercontent.com/4581090/160974118-0b572c8a-0906-4520-bc20-33199f218704.png)


# Features

- On the functional level, there are two basic categorization - User authentication service, and Short URL Creation service.
- JWT Token based authentication
- User Management API to create new users
- A default Admin `{'name': 'admin', 'password': '12345'}` is created automatically during build (only for local testing purposes).
- Targets in Makefile to ease local development - more details in the Local Development Setup section.

## API Definitions
- This project uses REST APIs to create short URLs and redirect short URL to original URL.

### Create Short URL
- Allowed methods - [POST]
- A valid request must contain the following parameters in the request body.
  -  _**URL [String]:**_ Original URL we want to shorten. 
  -  _**alias [String]:**_ Custom Link for the shortened URL. Must be unique and between 3 to 10 characters in length. Example - `danny`
  -  _**expiration_date [ISO 8601 Format datetime object]:**_ Date of expiry of the Shortened URL.  Default is current time + 30 days (if no expiration date is provided).
- Returns:
  - _**shortened-url [String]:**_ Short URL for redirection to original URL
  - _**created_at [ISO 8601 Format datetime object]:**_ The time of creation of this shortened URL
  - _**expiration_date [ISO 8601 Format datetime object]:**_ The time of expiry of this shortened URL

### Redirection URL (Shortened URL)
- Allowed methods [GET]
- Parameters:
  - _**shortened URL key/ID [String]:**_ Example, `<BASE_URL>/shortly/XvBaW` here the Key is `XvBaW`. 
- Returns:
  - _**HTTPResponse:**_ Redirects to the original Link mapped to this shortened URL key/id.

## User Authentication Service
- Django application - Handles User CRUD operation. 
- Database - Postgres (Stores User data like ID, Name)
- Authentication - Using JSON Web Tokens.

### USER Endpoints
* **/api/token/**
   * POST
* **/api/register/**
   * POST
* **/api/user/{id}**
   * GET, POST, PUT, DELETE
* **/api/shortenurl/**
   * POST

### User Model
![image](https://user-images.githubusercontent.com/4581090/160870372-731ad5d9-c602-4f6b-be1f-9c7592152ca0.png)

## Short URL Service
- Flask application - Handles two operation - creation of short URL, and redirection using Short URL.
  - Short URL Creation endpoint is only available to authenticated users. 
  - Authentication handled by the `User Authentication Service`
  - Database - MongoDB 
### Features
#### Create a Short URL
- Create a short link given any link of arbitrary length 
  -  example, The URL `https://github.com/jahandaniyal` is shortened to `<BASE_URL>/shortly/XvBaW`  
  -  If the same long URL is provided again (perhaps by another User) then the service will return existing short URL. 
  -  Expiration Time:
  -  Users can specify expiration time (default is 30 Days, if it is not provided by the user)
- Custom short link
  -  Must be Unique and length limitation of 3 to 10 characters
  -  If custom short link is already used by, then the User needs to select another one
  -  Successful creation if Unique : example, `<BASE_URL>/shortly/danny` (Here, the custom short link is 'danny')
  -  Same expiration, and url reuse rules apply to custom short links as well
- Endpoint
  -  `<AUTH_SERVICE_BASE_URL>/api/shortenurl/{id}`
  -  This endpoint is only accessible through User Authentication Service
  -  Can only be accessed by Authenticated Users

#### Short URL Redirection
- If a user visits a short url, this service will fetch the long URL from mongoDB and redirect the user to this long URL
- Endpoint:
  -  `<BASE_URL>/shortly/{id}`
  -  This endpoint is directly accessible by the User (no need to go through Authservice)
  -  Publicly accessible.

#### Reusing short URL ID/keys
- We want to re-use the keys/ids which have expired. One way to find out is by pooling the DB occasionally and checking for expired links.
- Another approach would be to check anytime someone tries use a Short URL. If it has expired then we inform the User and recover the URL key for future use.
  - This POC uses the later approach.

### Key Generation
- Key consist of fixed length of ASCII-letter combinations (For example, 52 ASCII char [a-z,A-z] of length 5: aaaaa-ZZZZZ)
- DB is pre-populated with a sub-set of all possible combinations using a utility script.
  - Pre-populuation process is randomised so `aaa` and `aab` are not consecutive entries.
  - Batch pre-population also helps when we want to scale our system. If we run out of keys, then we just create another cluster with a different sub-set of ASCII chars.
- Randomization of keys ensure that the generated short URLs are not guessable.
  
   
### Short URL Model
![image](https://user-images.githubusercontent.com/4581090/160886547-65011216-2224-4c01-9488-25375aba4a7d.png)

## Monitoring Services
- Using Prometheus and Grafana
- Can be deployed on the Kubernetes cluster or use cloud managed Kubernetes services like Google Kubernetes Engine. 
- Monitor resource consumption and load metrics of each node in the cluster.


## Local Development Setup
- Uses Docker for building and running the applications.
- Use Make to build, run, stop, and clean the local development environment (assumes a linux-like environment - Tested on ubuntu).
- build - This target will build the docker containers, install all dependencies in requirements.txt and make the initial migrations to the DB. 
   - `make build` or `sudo make build` depending on how docker, docker-compose was installed on the OS.
- run - Run the server for testing locally.
   - `make run`
- stop - Stops all running docker containers related to this project.
   - `make stop`
- clean - Removes virtualenv and temporary files.
   - `make clean`

## Running Locally

### Endpoints
* **/api/token/**
   * POST
* **/api/register/**
   * POST
* **/api/user/{id}**
   * GET, POST, PUT, DELETE
* **/api/shortenurl/**
   * POST
* **/shortly/{id}**
  * GET
   
### Create an Admin
* Ideally, you would want to create a SuperUser/Admin for your application. This is already done in `build` step.
   * A default Admin `{'name': 'admin', 'password': '12345'}` with these credentials is created for testing.
   
### Create new users:
* Use API endpoint `AUTH_SERVICE_BASE_URL/api/register/` to create a new user. Where `AUTH_SERVICE_BASE_URL` could be for example - `http://127.0.0.1:8000/`
   * Body structure is similar to - `{"name": "user1", "password": "123abc#$%"}`. Remember your password obviously! 

### Get a Web Token
* Use API endpoint `AUTH_SERVICE_BASE_URL/api/token/` to get 'access' and 'refresh' token. 
   * Body - `{"name": "user1", "password": "123abc#$%"}`.

### Get User Info
*  Use API endpoint `AUTH_SERVICE_BASE_URL/user/{id}/` to fetch information about the User. You will need 'access' token from the previous step.   
   * Headers - Authorization: Bearer <ACCESS_TOKEN>

### Create short URL
* Use API endpoint `AUTH_SERVICE_BASE_URL/api/shortenurl/` to create a short URL given a Long URL. Optionally provide - Custom Link and expiration date in the request body.
* User Authorization header is required for this operation.
  * Body -  Example `{
      "url": "https://github.com/jahandaniyal/url-shortner-poc/",
      "alias": "danny",
      "expiration_date": "2022-04-30T04:58:34Z"
  } `
  * Headers - Authorization: Bearer <ACCESS_TOKEN>
* Returns:
  * _**shortened-url [String]:**_ Short URL for redirection to original URL
  * _**created_at [ISO 8601 Format datetime object]:**_ The time of creation of this shortened URL
  * _**expiration_date [ISO 8601 Format datetime object]:**_ The time of expiry of this shortened URL
  

### Short URL redirection
* Use API endpoint `BASE_URL/shortly/{id}`. No access token required.
* Returns:
  * _**HTTPResponse:**_ Redirection to the original link.
 
