# API Documentation

## Endpoints

### Create Appointment

- **URL:** `/create/`
- **Method:** `POST`
- **Auth required:** Yes
- **Data Params:** 
    - `doctor`: ID of the doctor
    - `date`: Date of the appointment
    - `time_at`: Time of the appointment
- **Success Response:**
    - **Code:** 200
    - **Use the payment id from the response to initiate payment**
    - **Content:** `{ id : 12, doctor : 34, patient : 56, date : "2022-12-31", time_at : "09:00", payment : 78 }`

### List Appointments

- **URL:** `/lists/`
- **Method:** `GET`
- **Auth required:** Yes
- **Success Response:**
    - **Code:** 200
    - **Content:** `{ id : 12, doctor : 34, patient : 56, date : "2022-12-31", time_at : "09:00", payment : 78 }`

### Update Appointment

- **URL:** `/update/<id>/`
- **Method:** `PUT`
- **Auth required:** Yes
- **Data Params:** 
    - `doctor`: ID of the doctor
    - `date`: Date of the appointment
    - `time_at`: Time of the appointment
- **Success Response:**
    - **Code:** 200
    - **Content:** `{ id : 12, doctor : 34, patient : 56, date : "2022-12-31", time_at : "09:00", payment : 78 }`

### Initiate Payment

- **URL:** `/pay/`
- **Method:** `POST`
- **Auth required:** Yes
- **Data Params:** 
    - `payment_id`: ID of the payment
- **Success Response:**
    - **Code:** 302
    - **Content:** Redirects to payment URL

<!-- ### Payment Callback

- **URL:** `/callback/`
- **Method:** `GET`
- **Auth required:** No
- **Data Params:** 
    - `transaction_id`: ID of the transaction
    - `pidx`: Payment index
    - `amount`: Amount of the payment
- **Success Response:**
    - **Code:** 302
    - **Content:** Redirects to create appointment URL -->

### List Appointments for a Doctor

- **URL:** `/doctor/<doctor_id>/`
- **Method:** `GET`
- **Auth required:** Yes
- **Success Response:**
    - **Code:** 200
    - **Content:** `{ id : 12, doctor : 34, patient : 56, date : "2022-12-31", time_at : "09:00", payment : 78 }`