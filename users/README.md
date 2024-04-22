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


## Change Password

**Endpoint:** `/change/`

**Method:** `POST`

**Permission:** `IsAuthenticated`

**Data Parameters:**

- `old_password`: The user's current password.
- `new_password`: The new password the user wants to set.

**Success Response:**

- **Code:** `200 OK`
- **Content:** `{'message': 'Password changed successfully'}`

**Error Response:**

- **Code:** `400 BAD REQUEST`
- **Content:** `{'error': 'Old password is incorrect'}`

## Reset Password Token

**Endpoint:** `/reset_token/`

**Method:** `POST`

**Permission:** `AllowAny`

**Data Parameters:**

- `email`: The user's email address.

**Success Response:**

- **Code:** `200 OK`
- **Content:** `{'message': 'Password reset link sent to your email'}`

**Error Response:**

- **Code:** `400 BAD REQUEST`
- **Content:** `{'error': 'Error message'}`

**Notes:**

- An email will be sent to the user with a password reset token. This token will expire after 10 minutes.

## Reset Password

**Endpoint:** `/reset/`

**Method:** `POST`

**Permission:** `AllowAny`

**Data Parameters:**

- `email`: The user's email address.
- `token`: The password reset token.
- `password`: The new password the user wants to set.

**Success Response:**

- **Code:** `200 OK`
- **Content:** `{'message': 'Password reset successfully'}`

**Error Response:**

- **Code:** `400 BAD REQUEST`
- **Content:** `{'error': 'Invalid token or expired token.'}` or `{'error': 'Invalid token'}`

**Notes:**

- The token is checked for validity and expiry. If it's invalid or expired, an error response is returned. If it's valid, the user's password is reset.