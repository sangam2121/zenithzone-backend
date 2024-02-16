## API Endpoints

### Posts

- `GET /`: Returns a list of all posts. Requires authentication.

- `POST /`: Creates a new post. Requires authentication and the following parameters:
  - `title`: Title of the post.
  - `content`: Content of the post.
  - `thumbnail`: Thumbnail image for the post.
  - `author`: ID of the author.
  - `file_upload`: File to be uploaded.
  - `is_anonymous`: Boolean indicating if the post is anonymous.
  - `post_type`: Type of the post.

- `PUT /update/<slug:pk>/`: Updates the details of a specific post identified by the post's ID. Requires authentication and the same parameters as the POST request.

- `DELETE /delete/<slug:pk>/`: Deletes a specific post identified by the post's ID. Requires authentication.

### Comments

- `GET /comments/`: Returns a list of all comments.

- `POST /comments/`: Creates a new comment. Requires the following parameters:
  - `post`: ID of the post.
  - `author`: ID of the author.
  - `content`: Content of the comment.

- `PUT /comments/update/<slug:pk>/`: Updates the details of a specific comment identified by the comment's ID. Requires the same parameters as the POST request.

- `DELETE /comments/delete/<slug:pk>/`: Deletes a specific comment identified by the comment's ID.

## Models

### Post

- `id`: UUID field, primary key.
- `title`: CharField, max length 100, unique.
- `content`: TextField.
- `thumbnail`: ImageField, with a default image.
- `author`: ForeignKey to CustomUser.
- `file_upload`: FileField.
- `is_anonymous`: BooleanField, default False.
- `post_type`: CharField, max length 100, choices defined by `post_type`.
- `created_at`: DateTimeField, auto_now_add=True.
- `updated_at`: DateTimeField, auto_now=True.

### Comment

- `id`: UUID field, primary key.
- `post`: ForeignKey to Post.
- `author`: ForeignKey to CustomUser.
- `content`: TextField.
- `created_at`: DateTimeField, auto_now_add=True.
- `updated_at`: DateTimeField, auto_now=True.