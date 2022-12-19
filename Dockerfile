FROM python:3.8-slim

# Install the necessary libraries
RUN pip install opencv-python numpy Flask
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
# Copy the code into the container
COPY . /app
WORKDIR /app

# Run the app when the container starts
CMD ["python", "app.py"]
