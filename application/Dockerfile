FROM python:3.7.3-stretch

# Gunicorn binds port 5000 as the output. Expose this port.
EXPOSE 5000

# Set a working directory for the application.
WORKDIR /usr/src/app

# Install the various packages per the frozen pip.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current host contents into the working directory.
COPY . .

# The following environment variable is required to specify the app
ENV FLASK_APP main.py

# Finally, run the container as an executable by running the launch script.
ENTRYPOINT ["./launch.sh"]
