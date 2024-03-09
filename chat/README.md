# Chat API Documentation

## Endpoints

### 1. Create Chat Room

- **URL:** `/chatrooms/create`
- **Method:** `POST`
- **Data Params:**
    - `participant1`: User ID of the first participant
    - `participant2`: User ID of the second participant

### 2. List Chat Rooms

- **URL:** `/chatrooms/`
- **Method:** `GET`
- **Query Params:**
    - `participant`: User ID of the participant to filter chat rooms

### 3. Create Message

- **URL:** `/messages/create`
- **Method:** `POST`
- **Data Params:**
    - `chat_room`: Chat Room ID where the message will be sent
    - `content`: Content of the message

### 4. List Messages

- **URL:** `/messages/`
- **Method:** `GET`
- **Query Params:**
    - `chat_room`: Chat Room ID to filter messages

## Success Response

- **Code:** `200 OK`
- **Content:** 
    - `message`: Success message
    - `chat_room` or `message`: Created or retrieved object data

## Error Response

- **Code:** `400 BAD REQUEST`
- **Content:** 
    - `error`: Error message
    - `status`: HTTP status code

- **Code:** `403 FORBIDDEN`
- **Content:** 
    - `error`: Error message
    - `status`: HTTP status code
  - Apologies for the oversight. Here are the missing endpoints:

### 5. Update Chat Room

- **URL:** `/chatrooms/<id>/`
- **Method:** `PUT`
- **URL Params:**
    - `id`: ID of the chat room to be updated
- **Data Params:**
    - `participant1`: User ID of the first participant
    - `participant2`: User ID of the second participant

### 6. Delete Chat Room

- **URL:** `/chatrooms/<id>/`
- **Method:** `DELETE`
- **URL Params:**
    - `id`: ID of the chat room to be deleted

### 7. Update Message

- **URL:** `/messages/<id>/`
- **Method:** `PUT`
- **URL Params:**
    - `id`: ID of the message to be updated
- **Data Params:**
    - `chat_room`: Chat Room ID where the message will be sent
    - `content`: Content of the message

### 8. Delete Message

- **URL:** `/messages/<id>/`
- **Method:** `DELETE`
- **URL Params:**
    - `id`: ID of the message to be deleted

For the update and delete endpoints, the user must be a participant in the chat room or the author of the message. Otherwise, a `403 FORBIDDEN` response will be returned.

## Notes

- All endpoints require authentication.
- All data parameters and query parameters are optional unless stated otherwise.
- All endpoints return JSON data.