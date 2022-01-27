# **CMS** 

## Clinic Management System

<!--Banner Start-->


<!--Banner End-->


CMS is an online clinic record system that can be used to book appointments and manage patient records, especially for small clinics. Patient history is stored in the database and can be accessed by the user through their dashboard.

Developed an OTP veriﬁcation method using a mail module to send an OTP to the registered email id and Twilio module to send an OTP to the registered mobile number.

## Contents
 
 * [Technologies](#technologies)

   * [Frontend](#frontend)
   * [Backend](#backend)
   * [Database](#database)
   * [Storage](#storage)
   * [Hosting](#hosting)

 * [Features](#features)
   
   * [For Patient](#for-patient)  
   * [For Clinic](#for-clinic)  
 
 * [Links](#links)
 * [API Reference](#api-reference)

   * [Login](#login)
   * [Register](#register)
   * [Patient Information](#patient-information)
   * [Doctors](#doctors)
   * [Past-bookings](#past-bookings)
   * [Bookings](#bookings)

     * [Active Appointments](#get-active-appointments)
     * [Book Appointment](#post-book-appointment)
     * [Cancel Appointment](#delete-cancel-appointments)

   * [GET Report](#get-report)
   * [Send OTP](#send-otp)

 * [Usage](#usage) 
 * [License](#license) 

## Technologies 

* ### Frontend
    
    * HTML
    * CSS
    * Javascript
    * Bootsrtap4
    * jqurey

* ### Backend
    
    * django
    * django-rest-framework

* ### Database
    
    * postgresql

* ### Storage
    
    * AWS S3

* ### Hosting
    * Heroku 

## Features

* #### For Patient
        
      * View or update profile information.
      * Add or update profile picture.
      * Access many features from patient dashboard such as:
            
        - View past consultations and download the prescription.
        - Book or cancel appointments anytime.
        - keep track of your active appointments.
        - View your past appointment details.
        - View and download lab reports.

* #### For Clinic

      * Manage patient records easily.
      * Reduces overhead on the staff.
      * Manage everything using the admin panel of CMS.

## Links

##### CMS website can be accessed using the link below.
> [CMS](https://cms-wa.herokuapp.com/)

##### CMS Admin panel can be accessed using the link below.
> [CMS Admin](https://cms-wa.herokuapp.com/admin/)

#### API Endpoint list

> [CMS API](https://cms-wa.herokuapp.com/cms-api/)

You can use the CMS API to communicate with the server, but to do so, you must first acquire an auth token by logging in.

>*Note:- For login and registration, the auth token is not required.*

## API reference

#### login

##### Allowed Requests

| Request Method | Endpoint                                    |
| -------------- | ------------------------------------------- |
| POST           | https://cms-wa.herokuapp.com/cms-api/login/ |

To communicate with the server, you will need an auth token, which will be generated if it does not exist by sending the username and password in JSON format.

```JSON
{
    "username":"example_username",
    "password":"example_password"
}   
```

>*Note:- ALL the fields are required! but the order need not be the same.*

Sending a JSON file of the same structure will fetch you your auth token like this.

```JSON
{
    "token": "<your_auth_token>"
}
```
An auth token is only generated once.

#### register

##### Allowed Requests

| Request Method | Endpoint                                     |
| -------------- | -------------------------------------------- |
| POST           | https://cms-wa.herokuapp.com/cms-api/signup/ |

To log in and obtain an auth token, you must first be registered to the site. In order to do so, write a JSON file of the same structure.

```JSON
{
    "user": {
        "username": "example_username",
        "password": "example_password",
        "first_name": "example_firstname",
        "last_name": "example_lastname",
        "email": "example_email"
    },
    "gender": "gender", 
    "dob": "date",
    "address": "example_address",
    "phone": "xxxxxxxxxx"
}
```

>*Note:- ALL the fields are required except last_name can be "", Date must be of the format 'YYYY-MM-DD', phone-number must be of 10 digits, and gender must be one of the three Male, Female or Other.*

By Sending the above request, you will get the following response if there is no error in the JSON file. 

```JSON
{
    "MSG": "DATA SAVED",
    "DATA": {
        "id": 173,
        "user": {
            "id": 223,
            "username": "system_generate_unique_username",
            "password": "example_password_hashed",
            "first_name": "example_firstname",
            "last_name": "example_lastname",
            "email": "example_email"
        },
        "gender": "gender",
        "dob": "date",
        "address": "example_address",
        "phone": "xxxxxxxxxx",
        "profile_pic": "image-url"
    }
}

```

> *Note:- The auth token assigned to you must be included in the header of all the JSON files given in the below examples.          
>  - The header must in key: value format i.e*                                 
     **"Authorization":"token <your_auth_token>"**


#### Patient information

##### Allowed Requests

| Request Method | Endpoint                                      |
| -------------- | --------------------------------------------- |
| GET            | https://cms-wa.herokuapp.com/cms-api/patient/ |

To get the Patient profile information you must send the same JSON file as given below.

```JSON
{

}
```

By Sending the above request you will get the following response if there is no error in the JSON file. 

```JSON
{
    "id": 173,
    "user": {
        "id": 223,
        "username": "system_generate_unique_username",
        "password": "example_password_hashed",
        "first_name": "example_firstname",
        "last_name": "example_lastname",
        "email": "example_email"
    },
    "gender": "gender",
    "dob": "date",
    "address": "example_address",
    "phone": "xxxxxxxxxx",
    "profile_pic": "image-url"
}
```

#### doctors

##### Allowed Requests

| Request Method | Endpoint                                     |
| -------------- | -------------------------------------------- |
| GET            | https://cms-wa.herokuapp.com/cms-api/doctor/ |

To get a list of all the doctor's information send the same JSON file as sent for 'GET Patient information', and to get individual doctor's information send a JSON file of the same type as below.


###### For list of doctors

```JSON
{

}
```

###### For individual doctor information

```JSON
{
    "doctor_id":12 
}
```

>*Note:- doctor_id must be a valid integer id!*

By Sending the above request you will get the following response if there is no error in the JSON file.

###### For list of doctors

```JSON
[
    {
        "id": 11,
        "name": "Dr. xxx",
        "age": "xx",
        "gender": "gender",
        "experience": "xx",
        "domain": "xxxxxxx",
        "office_number": "xxxxxxxxxxx",
        "profile_pic": "doctor_profile_pic_url"
    },
    {
        "id": 12,
        "name": "Dr. xxx",
        "age": "xx",
        "gender": "gender",
        "experience": "xx",
        "domain": "xxxxxxx",
        "office_number": "xxxxxxxxxxx",
        "profile_pic": "doctor_profile_pic_url"
    },
]
```

###### For individual doctor information

```JSON
[
    {
        "id": 12,
        "name": "Dr. xxx",
        "age": "xx",
        "gender": "gender",
        "experience": "xx",
        "domain": "xxxxxxx",
        "office_number": "xxxxxxxxxxx",
        "profile_pic": "doctor_profile_pic_url"
    }
]
```

#### Past bookings

##### Allowed Requests

| Request Method | Endpoint                                      |
| -------------- | --------------------------------------------- |
| GET            | https://cms-wa.herokuapp.com/cms-api/history/ |

To get the list of all past appointments you must send the same JSON file as given below.

```JSON
{

}
```

By Sending the above request you will get the following response if there is no error in the JSON file and the user had past appointments. 

```JSON

[
    {
        "id": 220,
        "book_no": "5",
        "patient_name": "xxxxxxxxxx",
        "doctor_name": "Dr. xxxxx",
        "patient_id": "223",
        "doctor_id": "12",
        "book_date": "2021-06-25",
        "book_slot": "09:30 AM",
        "reason": "--------"
    },
    {
        "id": 221,
        "book_no": "8",
        "patient_name": "xxxxxxxxxxx",
        "doctor_name": "Dr. xxxxx",
        "patient_id": "223",
        "doctor_id": "11",
        "book_date": "2021-07-03",
        "book_slot": "11:00 AM",
        "reason": "Canceled"
    }
]
```

#### bookings

##### Allowed Requests

| Request Method | Endpoint                                      |
| -------------- | --------------------------------------------- |
| GET            | https://cms-wa.herokuapp.com/cms-api/booking/ |
| POST           | https://cms-wa.herokuapp.com/cms-api/booking/ |
| DELETE         | https://cms-wa.herokuapp.com/cms-api/booking/ |

##### GET active appointments

To get the list of all active appointments you must send the same JSON file as given below.

```JSON
{

}
```

By Sending the above request you will get the following response if there is no error in the JSON file. 

```JSON
[
    {
        "Booking_id": 14,
        "patient": {
            "id": 223,
            "name": "xxxxx",
            "username": "xxxxxxxxx",
            "gender": "xxxxx"
        },
        "doctor": {
            "doctor_id": 13,
            "name": "Dr. xxxxxx",
            "gender": "xxxxx",
            "domain": "xxxxxx",
            "ofiice_number": "xxxxxxxxxx"
        },
        "booking_date": "2021-06-30",
        "time_slot": "09:30 AM"
    },
    {
        "Booking_id": 15,
        "patient": {
            "id": 223,
            "name": "xxxxx",
            "username": "xxxxxxxxxx",
            "gender": "xxxxxx"
        },
        "doctor": {
            "doctor_id": 14,
            "name": "Dr. xxxxxxx",
            "gender": "xxxxxx",
            "domain": "xxxxxxxxx",
            "ofiice_number": "xxxxxxxxxx"
        },
        "booking_date": "2021-06-30",
        "time_slot": "10:30 AM"
    }
]
```

##### POST book appointment 

To book an appointment you must send the same JSON file as given below.

```JSON
{
    "date":"2021-07-6",
    "slot":"10:30 AM",
    "doc_id":12
}
```

> *Note:- ALL the fields are required!*

By Sending the above request you will get the following response if there is no error in the JSON file. 

```JSON
{
    "MSG": " Slot Booked!",
    "data": {
        "Booking_id": 35,
        "patient": {
            "id": 223,
            "name": "xxxxxx",
            "username": "xxxxxxxxxxx",
            "gender": "xxxxxx"
        },
        "doctor": {
            "doctor_id": 12,
            "name": "Dr. xxxxx",
            "gender": "xxxx",
            "domain": "xxxxxxxxxx",
            "ofiice_number": "xxxxxxxxxx"
        },
        "booking_date": "2021-06-30",
        "time_slot": "09:30 AM"
    }
}
```

##### DELETE cancel appointments

To cancel appointments you must send the same JSON file as given below.

```JSON
{
    "booking-ids":[
        39
    ]
}
```

> *Note:- ALL the fields are required!*

By Sending the above request you will get the following response if there is no error in the JSON file. 

```JSON
{
    "MSG": " Appointment Canceled"
}
```

#### GET report

##### Allowed Requests

| Request Method | Endpoint                                      |
| -------------- | --------------------------------------------- |
| GET            | https://cms-wa.herokuapp.com/cms-api/reports/ |

To get the patient's lab reports if any exists, you must send the same JSON file as given below.

```JSON
{

}
```

By Sending the above request you will get the following response if there is no error in the JSON file. 

```JSON
[
    {
        "id": 1,
        "contact": {
            "id": 223,
            "name": "xxxxx",
            "username": "xxxxxxxxxxx",
            "gender": "xxxx"
        },
        "doctor": {
            "doctor_id": 12,
            "name": "Dr. xxxxx",
            "gender": "xxxx",
            "domain": "xxxxxx",
            "ofiice_number": "xxxxxxxx"
        },
        "lab": "MRI",
        "date_of_report": "2021-07-05",
        "report_genrated": false
    },
    {
        "id": 2,
        "contact": {
            "id": 223,
            "name": "xxxxx",
            "username": "xxxxxxxxx",
            "gender": "xxxxx"
        },
        "doctor": {
            "doctor_id": 12,
            "name": "Dr. xxxxxx",
            "gender": "xxxxx",
            "domain": "xxxxxxx",
            "ofiice_number": "xxxxxxxxx"
        },
        "lab": "MRI",
        "date_of_report": "2021-07-05",
        "report_genrated": true,
        "report": "lab_report_image_name",
        "report-image": "lab_report_image_url"
    }
]
```

#### Send OTP

##### Allowed Requests

| Request Method | Endpoint                                          |
| -------------- | ------------------------------------------------- |
| GET            | https://cms-wa.herokuapp.com/cms-api/api-get-otp/ |
| POST           | https://cms-wa.herokuapp.com/cms-api/api-get-otp/ |

To get OTP you must send the same JSON file as given below.

```JSON
{
    "email":"xxxxxxxxxx",
    "sms":"xxxxxxxxxx"
}
```

By Sending the above request you will get the following response if there is no error in the JSON file. 

If only the phone number is provided

```JSON
{
    "MSG": "OTP Sent To The Registered Mobile Number.",
    "OTP": "782415"
}
```

If either email id is provided or both email id and phone number are provided

```JSON
{
    "MSG": "OTP Sent To The Registered Email.",
    "OTP": "532558"
}
```

## Usage

Download the zip file, extract it at the required location, and then navigate to where the requirements.txt file is located and run the command below.

```bash
    pip install -r requirements.txt
```

Then navigate to the CMS/settings.py file and append '0.0.0.0' to the ALLOWED_HOSTS list, it should look something like this

```python
 ALLOWED_HOSTS = [
    'cms-wa.herokuapp.com',
 ]
```
Then you will have to create a few environment variables for mail and sms modules in the cmsUtils directory, for the PostgreSQL database 
connection and settings.py file.

After everything is done, run any one of the following commands from the same location

```python
    python3 manage.py runserver 0.0.0.0:8000
```

### OR

```bash
    gunicorn CMS.wsgi:application 
```

In order to run anyone of the above commands, you must be in the directory as the manage.py file.


#### Top
[TOP](#cms)# CMS-master
 
