FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /notebook

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8888 for Jupyter Notebook
EXPOSE 8888

# Command to run the python file
# CMD ["python", "generate_predictions.py"]

CMD ["bash", "-c", "jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token=''"]