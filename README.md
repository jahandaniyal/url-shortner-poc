# url-shortner-poc

# Proposed Architecture

![asd drawio (2)](https://user-images.githubusercontent.com/4581090/160974118-0b572c8a-0906-4520-bc20-33199f218704.png)


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
* /api/shortenurl/
   * POST

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

### Short URL Redirection
- If a user visits a short url, this service will fetch the long URL from mongoDB and redirect the user to this long URL
- Endpoint:
  -  `<BASE_URL>/shortly/{id}`
  -  This endpoint is directly accessible by the User (no need to go through Authservice)
  -  Publicly accessible.

### Reusing short URL ID/keys
- We want to re-use the keys/ids which have expired. One way to find out is by pooling the DB occasionally and checking for expired links.
- Another approach would be to check anytime someone tries use a Short URL. If it has expired then we inform the User and recover the URL key for future use.
  - This POC uses the later approach.

### Key Generation
- Key consist of fixed length of ASCII-letter combinations (For example, 52 ASCII char [a-z,A-z] of length 5: aaaaa-ZZZZZ)
- DB is pre-populated with a sub-set of all possible combinations using a utility script.
  - Pre-poluation is randomised so `aaa` and `aab` are not consecutive entries.
  - Batch pre-population also helps when we want to scale our system. If we run out of keys, then we just create another cluster with a different sub-set of ASCII chars.
- Randomization of keys ensure that the generated short URLs are not guessable.
  
   
### Model
![image](https://user-images.githubusercontent.com/4581090/160886547-65011216-2224-4c01-9488-25375aba4a7d.png)

## Monitoring Services
- Using Prometheus and Grafana
- Can be deployed on the Kubernetes cluster or use cloud managed Kubernetes services like Google Kubernetes Engine. 
- Monitor resource consumption and load metrics of each node in the cluster.
