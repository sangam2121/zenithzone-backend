# ZenithZone Backend API

## User
- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`


## All endpoints require authentication. The user must be authenticated to access the endpoints. If the user is not authenticated, a 401 Unauthorized response will be returned.

**Note**: 
- `AUTH_USER_MODEL` is the user model used in the application. It is set to `users.CustomUser` by default.
- `slug:pk` is the primary key of the model. It is a unique identifier for the model and is generated automatically so that it can be used to retrieve, update, or delete the model instance.

