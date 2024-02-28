# API Documentation

## Endpoints

### Doctors

- `GET /lists/`: Returns a list of all doctors. Requires authentication. Optional query parameters:
  - `name`: Filters doctors by first or last name starting with the provided string.
  - `speciality`: Filters doctors by speciality containing the provided string.
  - `clinic_name`: Filters doctors by the `id` of the associated clinic.

- `PUT /update/<slug:pk>/`: Updates the details of the doctor with the given `pk`. Requires authentication and the following parameters:
  - `user`: The `id` of the user associated with the doctor.
  - `speciality`: The speciality of the doctor.
  - `image`: The image of the doctor.
  - `clinic`: The `id` of the clinic associated with the doctor.
  - `appointment_fee`: The appointment fee of the doctor.

- `DELETE /delete/<slug:pk>/`: Deletes the doctor with the given `pk`. Requires authentication.

### Reviews

- `GET /reviews/`: Returns a list of all reviews. Requires authentication. Optional query parameters:
  - `doctor`: Filters reviews by the `id` of the associated doctor.
  - `keyword`: Filters reviews by content containing the provided keyword.

- `POST /reviews/`: Creates a new review. Requires authentication and the following parameters:
  - `doctor`: The `id` of the doctor associated with the review.
  - `patient`: The `id` of the patient associated with the review.
  - `comment`: The comment of the review.
  - `rating`: The rating of the review (1-5).

- `GET /review/<slug:pk>/`: Retrieves the details of the review with the given `pk`. Requires authentication.

- `PUT /review/<slug:pk>/`: Updates the details of the review with the given `pk`. Requires authentication and the same parameters as `POST /reviews/`.

- `DELETE /review/<slug:pk>/`: Deletes the review with the given `pk`. Requires authentication.

### Clinics

- `GET /clinics/`: Returns a list of all clinics. Requires authentication. Optional query parameters:
  - `name`: Filters clinics by name starting with the provided string.

- `POST /clinics/`: Creates a new clinic. Requires authentication and the following parameters:
  - `name`: The name of the clinic.
  - `address`: The `id` of the location associated with the clinic.
  - `phone`: The phone number of the clinic.

- `GET /clinic/<slug:pk>/`: Retrieves the details of the clinic with the given `pk`. Requires authentication.

- `PUT /clinic/<slug:pk>/`: Updates the details of the clinic with the given `pk`. Requires authentication and the same parameters as `POST /clinics/`.

- `DELETE /clinic/<slug:pk>/`: Deletes the clinic with the given `pk`. Requires authentication.

## Models

### Doctor

- `user`: OneToOneField to the AUTH_USER_MODEL.
- `speciality`: CharField, can be null.
- `image`: ImageField, default image provided.
- `clinic`: ForeignKey to the Clinic model, can be null.
- `appointment_fee`: IntegerField, default is 0.

### Review

- `doctor`: ForeignKey to the Doctor model.
- `patient`: ForeignKey to the Patient model.
- `comment`: TextField.
- `rating`: IntegerField, choices from 1 to 5, default is 0.

### Clinic

- `name`: CharField.
- `address`: OneToOneField to the Location model, can be null.
- `phone`: CharField.

## Permissions

All endpoints require authentication. The user must be authenticated to access the endpoints. If the user is not authenticated, a 401 Unauthorized response will be returned.