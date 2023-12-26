# ZenithZone Backend API

## User
- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`

## Patient
- Get all patients: `GET /api/patient`

## Doctor
- Get all doctors: `GET /api/doctor/lists`
- Update/Get doctor profile: `PUT /api/doctor/update/:id`
- Delete doctor profile: `DELETE /api/doctor/delete/:id`
- Create/Get all clinics: `POST/GET /api/doctor/clinics`
- Create/Get all reviews: `POST/GET /api/doctor/reviews`
- Get/Update/Delete a review: `GET/PUT/DELETE /api/doctor/review/:id`
- Get/Update/Delete a clinic: `GET/PUT/DELETE /api/doctor/clinic/:id`
  **Note:** `:id` is the uuid of the doctor/clinic/review. You can get the uuid by using the `GET` method. 



## Appointment
- Get all appointments: `GET /api/appointment`



## Post
### Posts
- Create/List a post: `POST/GET /api/posts/`
- Update/View Details of a post: `PUT /api/posts/details/:id`
- Delete a post: `DELETE /api/posts/delete/:id`

### Comments
- Create/List a comment: `POST/GET /api/posts/comments/`
- Update/View Details of a comment: `PUT /api/posts/comments/details/:id`
- Delete a comment: `DELETE /api/posts/comments/delete/:id`

