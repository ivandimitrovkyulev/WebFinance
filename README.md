Web Finance
=======
### version v0.1.0

-------
### Installation


This project uses **[Python 3.11](https://www.python.org/downloads/)**, **[Poetry](https://python-poetry.org/docs/#installation)**,
**[Django 5.0.2](https://www.djangoproject.com/download/)**, **[gcloud CLI](https://cloud.google.com/sdk/docs/install)** and
**[cloud-sql-proxy](https://cloud.google.com/sql/docs/mysql/sql-proxy#install)**.

##### 1. Install dependencies

Activate virtual environment and install all third-party project dependencies:
```shell
# Sets Poetry configuration so it creates a virtual environment inside project root folder
poetry config --local virtualenvs.in-project true

# Create a virtual environment
poetry shell

# Install all project dependencies
poetry install
```

##### 2. Update variables
Create an `.env` file with the following content:

```shell
DEBUG=True
DATABASE_URL=postgres://ivankyulev:@//var/run/postgresql/test_db
GS_BUCKET_NAME=PROJECT_ID_MEDIA_BUCKET
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=<email-address>
EMAIL_HOST_PASSWORD=<your-password>
```

##### 3. Run Application

```shell
python3 manage.py runserver
```

-------
### Version

To update project version, run `./update_version.py` and follow instructions.


-------
### Deploy

Google Cloud Deployment: https://cloud.google.com/python/django/appengine

