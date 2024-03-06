# API Documentation

This API is built using Django and Django Rest Framework. It provides endpoints for managing Doctors, Reviews, Clinics, Education, Experience, and Locations.

## Endpoints

### Education, Experience, Location

These endpoints use Django Rest Framework's `ModelViewSet`, which provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.

- `GET /education/` - List all education entries
- `POST /education/` - Create a new education entry
- `GET /education/{id}/` - Retrieve a specific education entry
- `PUT /education/{id}/` - Update a specific education entry
- `DELETE /education/{id}/` - Delete a specific education entry

The same pattern applies to `experience` and `location`.

### Doctors

- `GET /lists/` - List all doctors. Query parameters:
  - `name` - Filter by doctor's first or last name
  - `speciality` - Filter by doctor's speciality
  - `clinic_name` - Filter by clinic's name
- `PUT /update/{user_id}/` - Update a specific doctor
- `DELETE /delete/{user_id}/` - Delete a specific doctor

### Reviews

- `GET /reviews/` - List all reviews. Query parameters:
  - `doctor` - Filter by doctor's id
  - `keyword` - Filter by keyword in review content
- `POST /reviews/` - Create a new review
- `GET /review/{id}/` - Retrieve a specific review
- `PUT /review/{id}/` - Update a specific review
- `DELETE /review/{id}/` - Delete a specific review

### Clinics

- `GET /clinics/` - List all clinics. Query parameters:
  - `name` - Filter by clinic's name
- `POST /clinics/` - Create a new clinic
- `GET /clinic/{id}/` - Retrieve a specific clinic
- `PUT /clinic/{id}/` - Update a specific clinic
- `DELETE /clinic/{id}/` - Delete a specific clinic

## Status Codes

The API returns the following status codes:

- `200 OK` - The request was successful
- `201 CREATED` - The request was successful and a resource was created
- `400 BAD REQUEST` - The request could not be understood or was missing required parameters
- `404 NOT FOUND` - The requested resource could not be found
- `405 METHOD NOT ALLOWED` - The method used is not allowed for the requested resource
- `500 INTERNAL SERVER ERROR` - There was an error processing the request