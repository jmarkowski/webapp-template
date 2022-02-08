FROM python:3.10.2-bullseye

# Gunicorn binds port 5000 as the output. Expose this port.
EXPOSE 5000

# Create a webapp:webapp user so the application does not run as root
RUN groupadd webapp
RUN useradd --create-home --gid webapp --shell /bin/sh webapp

ARG HOME_DIR=/home/webapp

# Set a working directory for the application
WORKDIR ${HOME_DIR}

# Install the various packages per the frozen pip
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current host contents into the working directory
COPY . .

# Ownership of all the copied files must belong to the webapp user
RUN chown -R webapp:webapp ${HOME_DIR}

# These are the environment variables required for the app
ENV FLASK_APP main.py

# Disable python output buffering. This allows gunicorn output to be real-time.
ENV PYTHONUNBUFFERED true

# Set the python path to the working directory so all modules may be found.
ENV PYTHONPATH=${HOME_DIR}

# Set the user of the running image
USER webapp

# Finally, pass the execution to the command script
CMD ["./docker-cmd-gunicorn.sh"]
