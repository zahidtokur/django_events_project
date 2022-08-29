## What is it?

This is an "events" web application where users can log in, create events and sign up for an
event and withdraw from an event. 

Any logged in user can:

- View upcoming events
- Create events
- Delete/edit the events they created
- Join and unjoin events
  
## Requirements

Having Python3 installed.

## Installation

After cloning the repository, create a virtual environment:

```
python3 -m venv <env-name>
```

Activate virtual enviroment:

```
source <env-name>/bin/activate
```

or

```
<env-name>/Scripts/activate
```

Install requirements:

```
pip install -r requirements.txt
```

Migrate:
```
python manage.py migrate
```

Load initial data:
```
python manage.py loaddata users
python manage.py loaddata events
```

NOTE: Order in which data is loaded is important since "events" table has relationships to "users" table.

## Usage

After installation is done, you can run your server like so:

```
python manage.py runserver
```

At the home page you will see some events listed but you will not be able to much with them since you are not a logged in user.

Go to `/account/register/` endpoint to create an account. After registration is complete you will be redirected to login page. After logging in, you will be able join/unjoin events, create your own events, update or delete the events you created. Here is the full list of endpoints and what they are for:

| URL | Description |
|---|---|
|  account/register/ |  create an account |
|  account/login/ |  login to your account |
|  account/logout/ |  logout of your account |
|  / |  home page, you will be able to see all the upcoming events |
|  event/create/ |  create an event (must be logged in) |
|  event/created/ |  list all the upcoming events logged in user created |
|  event/joined/ |  list all the upcoming events logged in user joined |
|  event/{event-id}/update/ |  update an event that logged in user created |
|  event/{event-id}/delete/ |  delete an event that logged in user created |
|  event/{event-id}/join/ |  add logged in user to the guests list of an event |
|  event/{event-id}/unjoin/ |  remove logged in user from the guests list of an event |

## Structure overview

```
django_events_project
│
└───events_project
│   
└───account
│   
└───core
│   
└───templates
|   │   account
|   │   core
│   
└───static
|   │   css
|   │   js
```

`account` directory is the directory of the app `account`. A custom user model is used where username field is email. 
`core` directory is the directory of the app `core`. `Event` model is created in this app and related views are located in `views.py`
`templates` directory is made up of two directories within. `account` and `event` directories, named after the apps.