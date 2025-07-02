# Python Flask Login API

This project is a simple Python Flask application that provides a user login API with JWT-based authentication and a MySQL backend.

## Folder Structure

The project is organized into the following main folders:

*   **`.github/workflows/`**: Contains GitHub Actions workflows, for example, `docker-publish.yml` which might be for building and publishing Docker images.
*   **`conections/`**: Handles database connection logic.
    *   `mysql.py`: Contains the function `conection_accounts()` to establish a connection to the MySQL database using SQLAlchemy, retrieving credentials from environment variables.
*   **`models/`**: Defines the database schema using SQLAlchemy ORM.
    *   `models.py`: Includes the `User` model with fields like `Id_User`, `Name`, `Lastname`, `User_mail`, `Password`, and `Status`.
*   **`services/`**: Contains the business logic of the application.
    *   `functions.py`: Implements functions like `hash_password` for hashing passwords and `login_user` for authenticating users and generating JWT tokens.
*   **`tests/`**: Includes unit and integration tests for the application.
    *   `test_login.py`: Contains Pytest tests for the `/login` API endpoint, mocking database connections and JWT encoding.

Other important files:

*   **`main.py`**: The entry point of the Flask application. It defines the `/login` route and starts the development server.
*   **`requirements.txt`**: Lists the Python dependencies required for the project (e.g., Flask, SQLAlchemy, PyMySQL, PyJWT, Pytest).
*   **`dockerfile`**: Defines the Docker image for containerizing the application. It sets up a Python 3.9 environment, copies the project files, installs dependencies, and specifies the command to run the application.
*   **`.gitignore`**: Specifies intentionally untracked files that Git should ignore (e.g., `__pycache__/`).

## Backend Pattern Design

The backend follows a **Layered Architecture** pattern. This pattern organizes the code into distinct layers, each with a specific responsibility:

1.  **Presentation Layer (`main.py`)**: Handles incoming HTTP requests, parses request data, and sends back HTTP responses. It uses Flask to define routes and manage request/response cycles.
2.  **Service Layer (`services/functions.py`)**: Contains the core business logic. For example, the `login_user` function orchestrates user authentication, password verification, and token generation. This layer is decoupled from the web framework and database specifics.
3.  **Data Access Layer (`conections/mysql.py`, `models/models.py`)**: Manages interaction with the database.
    *   `models.py` defines the data structures (entities) using SQLAlchemy ORM.
    *   `conections/mysql.py` handles the creation of database sessions.
    SQLAlchemy itself acts as an abstraction layer over the raw SQL, allowing for more Pythonic database interactions.

This separation of concerns makes the application easier to understand, maintain, and test.

## Communication Architecture

*   **Client-Server Communication**: The application exposes a RESTful API for clients to interact with. Currently, it has a `/login` endpoint that accepts POST requests with JSON payloads.
*   **Internal Communication**:
    *   The **Presentation Layer** (`main.py`) calls functions in the **Service Layer** (`services/functions.py`) to perform business operations.
    *   The **Service Layer** interacts with the **Data Access Layer** (`conections/mysql.py` and `models/models.py`) to fetch or persist data. It calls `conection_accounts()` to get a database session and uses SQLAlchemy models to query the database.

## Folder Pattern

The project uses a **Layer-Based Folder Pattern**, where folders are named according to the architectural layer they represent:

*   `conections/` and `models/` for the Data Access Layer.
*   `services/` for the Service Layer.
*   `main.py` (though not in a separate folder) acts as the Presentation Layer entry point.
*   `tests/` groups all test files, which mirrors the structure of the application code it tests.

This pattern helps in quickly locating code related to a specific layer of the application.

## Running the Code

### 1. Local Setup (Without Docker)

**Prerequisites:**

*   Python 3.9 or higher
*   Pip (Python package installer)
*   Access to a MySQL database instance

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory of the project and add the following variables with your database credentials and a secret key for JWT:
    ```env
    DBA_HOSTIP=your_mysql_host
    DBA_PORT=your_mysql_port (e.g., 3306)
    DBA_USER=your_mysql_user
    DBA_PASSWORD=your_mysql_password
    DBA_NAME=your_mysql_database_name
    SECRET_KEY=your_strong_secret_key_for_jwt
    ```
    Replace placeholders with your actual configuration. The `SECRET_KEY` is crucial for signing and verifying JWTs.

5.  **Ensure the `users` table exists in your database.**
    The table schema is defined in `models/models.py`. You might need to create this table manually or use a migration tool (not included in this project).
    ```sql
    -- Example SQL for creating the users table (adjust types if needed for your MySQL version)
    CREATE TABLE users (
        Id_User INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(100),
        Lastname VARCHAR(100),
        User_mail VARCHAR(100) UNIQUE,
        Password VARCHAR(100), -- Stores hashed passwords
        Status INT,
        CONSTRAINT CK_Status CHECK (Status IN (0, 1))
    );
    ```

6.  **Run the Flask application:**
    ```bash
    python main.py
    ```
    The application will start on `http://0.0.0.0:8080`.

### 2. Running with Docker

**Prerequisites:**

*   Docker installed and running.

**Steps:**

1.  **Clone the repository (if not already done):**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create the `.env` file:**
    As described in the "Local Setup" section, create a `.env` file in the root directory with your database credentials and `SECRET_KEY`. Docker will use this file if you mount it or build it into the image (though the current Dockerfile doesn't explicitly copy `.env`, it's good practice to have it for the application running inside the container to access).

    **Note**: For Docker, `DBA_HOSTIP` should be the IP address or hostname of your MySQL server *accessible from the Docker container*. If MySQL is running on your host machine, this might be `host.docker.internal` or your machine's network IP, not `localhost`.

3.  **Build the Docker image:**
    ```bash
    docker build -t flask-login-api .
    ```

4.  **Run the Docker container:**
    You need to pass the environment variables to the container. You can do this using an environment file or by passing them individually.
    ```bash
    docker run -p 8080:8080 --env-file .env flask-login-api
    ```
    Or, if your MySQL server is also running in Docker and they share a network:
    ```bash
    # Example: Assuming MySQL container is named 'mysql-db' and on 'my-network'
    # docker network create my-network
    # docker run --name mysql-db --network my-network -e MYSQL_ROOT_PASSWORD=... -d mysql:latest
    # Then update DBA_HOSTIP in .env to 'mysql-db'

    docker run --network my-network -p 8080:8080 --env-file .env flask-login-api
    ```
    The application will be accessible at `http://localhost:8080`.

## API Endpoints

### User Login

*   **Endpoint:** `/login`
*   **Method:** `POST`
*   **Description:** Authenticates a user and returns a JWT token upon successful login.
*   **Request Body (JSON):**
    ```json
    {
        "User_mail": "user@example.com",
        "password": "yourpassword"
    }
    ```
*   **Responses:**
    *   **200 OK (Success):**
        ```json
        {
            "token": "your.jwt.token"
        }
        ```
    *   **400 Bad Request (Missing fields):**
        ```json
        {
            "error": "Email and password are required"
        }
        ```
    *   **401 Unauthorized (Invalid credentials):**
        ```json
        {
            "error": "Invalid credentials"
        }
        ```
    *   **403 Forbidden (User inactive):**
        ```json
        {
            "error": "User is inactive"
        }
        ```
    *   **404 Not Found (User not found):**
        ```json
        {
            "error": "User not found"
        }
        ```
    *   **500 Internal Server Error (Other errors):**
        ```json
        {
            "error": "Description of the error"
        }
        ```

## Running Tests

The project uses `pytest` for testing.

1.  **Ensure you have installed development dependencies (including pytest):**
    ```bash
    pip install -r requirements.txt
    ```
    (Pytest is already included in the provided `requirements.txt`)

2.  **Set up environment variables for testing if needed.**
    The tests might require specific environment variables (like `SECRET_KEY`). The `test_login.py` example temporarily sets `os.environ["SECRET_KEY"]`. For database-dependent tests not mocked, ensure your test environment can connect to a test database.

3.  **Run tests from the root directory:**
    ```bash
    pytest
    ```
    Pytest will automatically discover and run tests in the `tests/` directory. You should see output indicating the status of each test.
    ```bash
    ============================= test session starts ==============================
    platform ... -- Python ...
    plugins: ...
    collected 1 item

    tests/test_login.py .                                                    [100%]

    ============================== 1 passed in 0.xxs ===============================
    ```

