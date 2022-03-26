```

# Use the official lightweight Python image.
# https://hub.docker.com/_/python

FROM python:3

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.

RUN pip install dash-html-components==2.0.0
RUN pip install dash-table==5.0.0
RUN pip install dnspython==2.2.1
RUN pip install dominate==2.6.0
RUN pip install email-validator==1.1.3
RUN pip install Flask==2.0.3
RUN pip install Flask-Bootstrap==3.3.7.1
RUN pip install Flask-Compress==1.11
RUN pip install Flask-Login==0.5.0
RUN pip install Flask-Migrate==3.1.0
RUN pip install Flask-SQLAlchemy==2.5.1
RUN pip install Flask-WTF==1.0.0
RUN pip install greenlet==1.1.2
RUN pip install idna==3.3
RUN pip install install==1.3.5
RUN pip install itsdangerous==2.1.2
RUN pip install Jinja2==3.1.1
RUN pip install Mako==1.2.0
RUN pip install MarkupSafe==2.1.1
RUN pip install numpy==1.22.3
RUN pip install pandas==1.4.1
RUN pip install plotly==5.6.0
RUN pip install python-dateutil==2.8.2
RUN pip install pytz==2022.1
RUN pip install six==1.16.0
RUN pip install SQLAlchemy==1.4.32
RUN pip install tenacity==8.0.1
RUN pip install visitor==0.1.3
RUN pip install Werkzeug==2.0.3
RUN pip install WTForms==3.0.1
RUN pip install gunicorn

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
```
