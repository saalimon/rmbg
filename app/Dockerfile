FROM python:3

# Set the working directory to /app
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y


# Run app.py when the container launches
CMD ["python", "app.py"]

