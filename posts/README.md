# API Documentation

## Library

### `GET /library/`

List all libraries.

#### Parameters

- `author` (optional): Filter libraries by author's username (case-insensitive startswith match).
- `title` (optional): Filter libraries by title (case-insensitive startswith match).
- `author_id` (optional): Filter libraries by author's id.

### `POST /library/`

Create a new library.

#### Body

- `title`: The title of the library.
- `description`: The description of the library.

### `PUT /library/{id}/`

Update a library.

#### Body

- `title`: The new title of the library.
- `description`: The new description of the library.

### `DELETE /library/{id}/`

Delete a library.

## Posts

### `GET /lists`

List all posts.

#### Parameters

- `author` (optional): Filter posts by author's username (case-insensitive startswith match).
- `title` (optional): Filter posts by title (case-insensitive startswith match).
- `post_type` (optional): Filter posts by post type (case-insensitive startswith match).

### `POST /lists`

Create a new post.

#### Body

- `title`: The title of the post.
- `content`: The content of the post.
- `post_type`: The type of the post.

### `PUT /update/{id}/`

Update a post.

#### Body

- `title`: The new title of the post.
- `content`: The new content of the post.
- `post_type`: The new type of the post.

### `DELETE /delete/{id}/`

Delete a post.

## Comments

### `GET /comments/`

List all comments.

#### Parameters

- `post` (optional): Filter comments by post id.

### `POST /comments/`

Create a new comment.

#### Body

- `content`: The content of the comment.
- `post`: The id of the post the comment is for.

### `PUT /comments/update/{id}/`

Update a comment.

#### Body

- `content`: The new content of the comment.

### `DELETE /comments/delete/{id}/`

Delete a comment.