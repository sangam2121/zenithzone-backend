# API Documentation

## Endpoints

### Chat

- `GET /<chat_room_id>/messages/`: Returns a list of all messages in the chat room with the given `chat_room_id`. Requires authentication.

- `POST /<chat_room_id>/messages/`: Creates a new message in the chat room with the given `chat_room_id`. Requires authentication and the following parameters:
  - `content`: The content of the message.
  - `chat_room`: The `id` of the chat room where the message is posted.
  - `sender`: The `id` of the user who sends the message.

## Models

### ChatRoom

- `id`: UUIDField, primary key, auto-generated, not editable.
- `participant1`: ForeignKey to the CustomUser model, related name 'user1'.
- `participant2`: ForeignKey to the CustomUser model, related name 'user2'.
- `name`: CharField, can be null or blank.

### Message

- `id`: UUIDField, primary key, auto-generated, not editable.
- `chat_room`: ForeignKey to the ChatRoom model, related name 'messages'.
- `sender`: ForeignKey to the CustomUser model, related name 'messages'.
- `content`: TextField.
- `created_at`: DateTimeField, auto_now_add is True.

## WebSocket

- `ws/chat/<userId>/<otherUserId>/`: Establishes a WebSocket connection between two users with the given `userId` and `otherUserId`. The following actions can be performed:
  - `new_message`: Sends a new message. Requires the following parameters:
    - `action`: Must be 'new_message'.
    - `message`: The content of the message.
    - `sender`: The `id` of the user who sends the message.
    - `chat_room`: The `id` of the chat room where the message is posted.
    - `other_user`: The `id` of the other user in the chat room.
  - `typing`: Indicates that the user is typing. Requires the following parameters:
    - `action`: Must be 'typing'.
    - `chat_room`: The `id` of the chat room where the user is typing.
    - `other_user`: The `id` of the other user in the chat room.

## Permissions

All endpoints and WebSocket connections require authentication. The user must be authenticated to access the endpoints and establish a WebSocket connection. If the user is not authenticated, a 401 Unauthorized response will be returned.