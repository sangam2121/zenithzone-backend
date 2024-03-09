# Chat Application API Documentation

## Endpoints

### 1. Chat Rooms

#### 1.1 Create/List Chat Rooms

- **URL:** `/chatrooms/`
- **Method:** `GET` | `POST`
- **Required Parameters:** None
- **Optional Parameters:** None
- **Data Parameters (POST):** 
  - `participant1`: UUID of the first participant (required)
  - `participant2`: UUID of the second participant (required)

#### 1.2 Update/Delete a Chat Room

- **URL:** `/chatrooms/<UUID:id>/`
- **Method:** `PUT` | `PATCH` | `DELETE`
- **Required Parameters:** `id` - UUID of the chat room
- **Optional Parameters:** None
- **Data Parameters (PUT/PATCH):** 
  - `participant1`: UUID of the first participant (optional)
  - `participant2`: UUID of the second participant (optional)

### 2. Messages

#### 2.1 Create/List Messages

- **URL:** `/messages/`
- **Method:** `GET` | `POST`
- **Required Parameters:** None
- **Optional Parameters:** `chat_room` - UUID of the chat room to filter messages
- **Data Parameters (POST):** 
  - `chat_room`: UUID of the chat room (required)
  - `content`: Text content of the message (required)

#### 2.2 Update/Delete a Message

- **URL:** `/messages/<UUID:id>/`
- **Method:** `PUT` | `PATCH` | `DELETE`
- **Required Parameters:** `id` - UUID of the message
- **Optional Parameters:** None
- **Data Parameters (PUT/PATCH):** 
  - `content`: Text content of the message (optional)

## Notes

- All endpoints require authentication. The user must be logged in.
- For creating a chat room or a message, the authenticated user must be one of the participants.
- For updating or deleting a chat room or a message, the authenticated user must be a participant in the chat room or the author of the message, respectively.