# Use an official Python runtime as a parent image
FROM python:3.11.0

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app/

# Install Poetry
RUN pip install poetry

# Copy the Poetry lock and configuration files into the container
COPY pyproject.toml poetry.lock ./

# Install dependencies with Poetry, including virtual environment creation
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the entrypoint script into the container
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy the current directory contents into the container at /app/
COPY . /app

# Run the entrypoint script when the container launches
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]