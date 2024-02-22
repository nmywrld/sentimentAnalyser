FROM python:3.7

WORKDIR /app

# Copy only requirements, to cache them in Docker layer
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Uncomment this if you want to install xformers
# RUN pip install xformers

# Uncomment this if you want to start the service when the container starts
# CMD ["python", "sentimentApp.py"]