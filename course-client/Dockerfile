# In Docker, it is common to base a new image on a previously-created image
# Use an official Python runtime image as a parent image to base this image on
FROM python:3.7-slim

# Set the working directory within the image to /app
WORKDIR /course-client

# the ADD command is how you add files from your local machine into a Docker image
# Copy the current directory contents into the container at /app
ADD . /course-client

# Install any needed packages specified in requirements.txt
# in Python, a requirements.txt file is a way of indicating dependencies in a way that the package manager, pip, can understand
RUN pip3 install -r requirements.txt
COPY . .

# Make port 6001 available to the world outside this container
EXPOSE 7001

# Run app.py when the container launches
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=7001"]
