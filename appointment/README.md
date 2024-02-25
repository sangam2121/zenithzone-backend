# API Documentation

## Endpoints

### 1. Create Appointment

**URL**: `/create/`

**Method**: `POST`

**Auth required**: Yes

**Data constraints**

```json
{
    "doctor": "[valid doctor id]",
    "patient": "[valid patient id]",
    "date": "[date in YYYY-MM-DD format]",
    "time": "[time in HH:MM format]",
    "purchase_order_id": "[valid purchase order id]"
}
```

**Data example**

```json
{
    "doctor": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "patient": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "date": "2022-12-31",
    "time": "15:30",
    "purchase_order_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

### 2. List Appointments

**URL**: `/lists/`

**Method**: `GET`

**Auth required**: Yes

### 3. Update Appointment

**URL**: `/update/<slug:id>/`

**Method**: `PUT` or `PATCH`

**Auth required**: Yes

**Data constraints**

```json
{
    "doctor": "[valid doctor id]",
    "patient": "[valid patient id]",
    "date": "[date in YYYY-MM-DD format]",
    "time": "[time in HH:MM format]"
}
```

**Data example**

```json
{
    "doctor": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "patient": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "date": "2022-12-31",
    "time": "15:30"
}
```

### 4. Initiate Payment

**URL**: `/pay/`

**Method**: `POST`

**Auth required**: Yes

**Data constraints**

```json
{
    "doctor": "[valid doctor id]"
}
```

**Data example**

```json
{
    "doctor": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

### 5. Payment Callback

**URL**: `/callback/`

**Method**: `GET`

**Auth required**: No

**Data constraints**

```json


{


    "transaction_id": "[valid transaction id]",
    "pidx": "[valid pidx]",
    "amount": "[valid amount]"
}
```

**Data example**

```json
{
    "transaction_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "pidx": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "amount": "500.00"
}
```

## Models

### Appointment

Field | Type | Description
--- | --- | ---
id | UUID | The unique identifier for the appointment.
doctor | ForeignKey (Doctor) | The doctor for the appointment.
patient | ForeignKey (Patient) | The patient for the appointment.
date | Date | The date of the appointment.
time | Time | The time of the appointment.
payment_status | Boolean | The payment status of the appointment.
created_at | DateTime | The date and time the appointment was created.

### Payment

Field | Type | Description
--- | --- | ---
id | UUID | The unique identifier for the payment.
user | ForeignKey (CustomUser) | The user who made the payment.
appointment | ForeignKey (Appointment) | The appointment the payment is for.
amount | Decimal | The amount of the payment.
status | Char | The status of the payment.
pidx | Char | The pidx of the payment.
transaction_id | Char | The transaction id of the payment.
purchase_order_id | Char | The purchase order id of the payment.