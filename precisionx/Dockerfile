# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . /code/

# Check the contents of the /code directory
RUN ls -a /code

# CMD or ENTRYPOINT to start your application
# CMD ["python", "manage.py", "runserver"]
ENV POSTGRES_HOST_AUTH_METHOD=md5
