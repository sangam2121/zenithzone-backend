## WebSocket API Documentation

### WebSocket Connection

To establish a WebSocket connection from frontend, we can use the native WebSocket API or libraries like `socket.io-client`.

The WebSocket URL should be in the following format:

```
ws://<your-server-url>/ws/chat/<userId>/<otherUserId>/
```

Replace `<your-server-url>`, `<userId>`, and `<otherUserId>` with your actual server URL and the IDs of the users participating in the chat.

### Sending Messages

To send a message, you need to send a JSON string through the WebSocket connection. The JSON string should have the following structure:

```json
{
    "action": "new_message",
    "chat_room": "<chat_room_id>",
    "other_user": "<other_user_id>",
    "message": "<message_content>",
    "sender": "<sender_id>"
}
```

Replace `<chat_room_id>`, `<other_user_id>`, `<message_content>`, and `<sender_id>` with your actual values.

### Receiving Messages

When a new message is sent, the server will send a JSON string through the WebSocket connection. The JSON string will have the following structure:

```json
{
    "action": "new_message",
    "id": "<message_id>",
    "chat_room": "<chat_room_id>",
    "sender": "<sender_id>",
    "content": "<message_content>",
    "created_at": "<message_creation_time>"
}
```

You can listen for incoming messages and handle them in your React frontend.

### Typing Indicator

To indicate that a user is typing, you can send a JSON string through the WebSocket connection with the following structure:

```json
{
    "action": "typing",
    "chat_room": "<chat_room_id>",
    "other_user": "<other_user_id>",
    "sender": "<sender_id>"
}
```

The server will forward this message to the other user in the chat room.

Please note that this is a basic documentation based on your provided code. You might need to adjust it according to your actual implementation and requirements.