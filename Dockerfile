# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

ADD requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
ADD ./run.py /app
ADD ./config.py /app
COPY ../app app/

# Make port 8443 available to the world outside this container
#EXPOSE 8443

# Run app.py when the container launches
CMD ["python3", "run.py"]