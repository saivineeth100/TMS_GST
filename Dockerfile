# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.2-slim-buster

# Warning: A port below 1024 has been exposed. This requires the image to run as a root user which is not a best practice.
# For more information, please refer to https://aka.ms/vscode-docker-python-user-rights`
EXPOSE 80

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY backend/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder: 'TMS_GST'. Please enter the Python path to wsgi file.
#CMD ["gunicorn", "--bind", "0.0.0.0:80", "pythonPath.to.wsgi"]
CMD ["python3", "backend/manage.py","runserver", "0.0.0.0:80"]