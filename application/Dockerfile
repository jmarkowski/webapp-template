FROM python:3.7.3-stretch

# Gunicorn binds port 5000 as the output. Expose this port.
EXPOSE 5000

# Create a webapp:webapp user so the application does not run as root
RUN groupadd webapp
RUN useradd --create-home --gid webapp --shell /bin/sh webapp

# Set a working directory for the application
WORKDIR /home/webapp

# Install the various packages per the frozen pip
COPY requirements.txt ./

# Create the virtual environment and install the required libraries
RUN python -m venv pyenv
RUN pyenv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the current host contents into the working directory
COPY . .

# These are the environment variables required for the app
ENV FLASK_APP main.py

# Ownership of all the copied files must belong to the webapp user
RUN chown -R webapp:webapp /home/webapp

# Set the user of the running image
USER webapp

# Finally, run the container as an executable by running the launch script
ENTRYPOINT ["./launch.sh"]
