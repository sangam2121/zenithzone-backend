## API Endpoints

### Authentication

- `POST /login/`: Obtain a token pair. Requires the following parameters:
  - `email`: User's email.
  - `password`: User's password.

- `POST /login/refresh/`: Refresh the token. Requires the following parameter:
  - `refresh`: Refresh token.

- `POST /register/`: Register a new user. Requires the following parameters:
  - `email`: User's email.
  - `password`: User's password.
  - `first_name`: User's first name.
  - `last_name`: User's last name.
  - `user_type`: User's type (choices: 'doctor', 'patient', 'admin').

### Users

- `GET /users/`: Returns a list of all users. Requires authentication.

- `PUT /update/`: Updates the details of the authenticated user. Requires authentication and the following parameters:
  - `email`: User's email.
  - `first_name`: User's first name.
  - `last_name`: User's last name.
  - `phone`: User's phone number.
  - `address`: User's address.
  - `bio`: User's bio.
  - `user_type`: User's type (choices: 'doctor', 'patient', 'admin').

## Models

### CustomUser

- `id`: UUID field, primary key.
- `email`: EmailField, unique.
- `first_name`: CharField, max length 30.
- `last_name`: CharField, max length 30.
- `phone`: CharField, max length 100, nullable.
- `address`: CharField, max length 100, nullable.
- `bio`: TextField, nullable.
- `is_active`: BooleanField, default True.
- `is_staff`: BooleanField, default False.
- `is_superuser`: BooleanField, default False.
- `user_type`: CharField, max length 10, choices defined by `user_type`.