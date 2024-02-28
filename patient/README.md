Here is the API documentation for the Django application:

## API Endpoints

### Patients

- `GET /lists/`: Returns a list of all patients. Optional query parameters:
  - `name`: Filters patients by first or last name starting with the provided string.
  <!-- - `user`: Filters patients by the `id` of the associated user. -->

- `PUT /update/<slug:pk>/`: Updates the details of the patient with the given `pk`. Requires authentication and the following parameters:
  - `user`: The `id` of the user associated with the patient.
  - `image`: The image of the patient.

- `DELETE /delete/<slug:pk>/`: Deletes the patient with the given `pk`. Requires authentication.

## Models

### Patient

- `user`: OneToOneField to the AUTH_USER_MODEL.
- `image`: ImageField, default image provided.

## Permissions

All endpoints require authentication. The user must be authenticated to access the endpoints. If the user is not authenticated, a 401 Unauthorized response will be returned.