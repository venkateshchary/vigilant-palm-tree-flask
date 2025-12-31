# Flask Learning App

A simple Flask application containerized with Docker and PostgreSQL.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Python 3.12](https://www.python.org/) (optional, for local development)
- [Pipenv](https://pipenv.pypa.io/en/latest/) (optional, for local development)

## Running with Docker (Recommended)

The easiest way to run the application is using Docker Compose. This will set up both the Flask application and the PostgreSQL database.

1.  **Build and start the containers:**

    ```bash
    docker-compose up -d --build
    ```

2.  **Access the application:**

    Open your browser and navigate to [http://localhost:5000](http://localhost:5000).

    You should see a "Hello, World!" message along with the PostgreSQL version, confirming the database connection.

3.  **Stop the containers:**

    ```bash
    docker-compose down
    ```

## Running Locally

If you want to run the application locally (outside of Docker), you will need a running PostgreSQL instance.

1.  **Install dependencies:**

    ```bash
    pipenv install
    ```

2.  **Set environment variables:**

    You need to configure the application to connect to your local database.

    ```powershell
    $env:POSTGRES_HOST="localhost"
    $env:POSTGRES_DB="flaskdb"
    $env:POSTGRES_USER="user"
    $env:POSTGRES_PASSWORD="password"
    ```

3.  **Run the application:**

    ```bash
    pipenv run python app.py
    ```
