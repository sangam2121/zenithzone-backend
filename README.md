# ZenithZone Backend API

## User
- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`

## Patient
- Get all patients: `GET /api/patient`

## Doctor
- Get all doctors: `GET /api/doctor`

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