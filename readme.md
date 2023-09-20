# A few step to setup the project in your local machine.

**Clone the project:**

`git@github.com:MySecondLanguage/stretch.git`

**Write .env file in base directory**
`.env` content are given below
```
DEBUG=1
DATABASE_URL=postgres://dbuser:dbpassword@dbhost:5432/dbname
SECRET_KEY=f$%5rw(n!g5y96jwp0(#zfuc)l%a*mi32i4qt2mz0jdt7^rs_h
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=


FACEBOOK_CLIENT_ID=
FACEBOOK_SECRET_KEY=


DEVELOPMENT_SERVER=True

```

## Install dependency with pipenv
I assume you have installed `pipenv` in your machine

**Activate the enviroment**

`pipenv shell`

`pipenv install`

`python3 manage.py runserver`


# Setup with Docker

I assume you have install docker and docker-compose in your machine.

**Put .env file in base directory**

the `.env` file will be

```
DEBUG=1
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
SECRET_KEY=f$%5rw(n!g5y96jwp0(#zfuc)l%a*mi32i4qt2mz0jdt7^rs_h
```

and the run

`sudo docker-compose up`

