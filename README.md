# 🎵 Wolns API

A REST API for Wolns.

## ✨ Features

* **🔐 User Authentication:** Secure user registration and login system.
* **🎧 Music Platform Integration:** Connect accounts from Spotify, Yandex Music, and VK Music.
* **🎶 Real-time Listening Status:** Fetch and display the currently playing track from connected music services.
* **👥 Subscription System:** Follow other users to see their listening activity.
* **💫 Track Sharing:** Share your current listening status with your subscribers.
* **🔌 API Endpoints:** Comprehensive API for managing users, accounts, subscriptions, and tracks.
* **⚡ Asynchronous Tasks:** Utilizes Celery for background tasks like updating user listening status.
* **📊 Monitoring:** Includes Prometheus and Grafana for monitoring application metrics.

## 🚀 Installation

### Prerequisites

🐳 Docker

### Setup

1. **📥 Clone the repository:**

    ```bash
    git clone https://github.com/wolns/wolns-api
    cd wolns-api
    ```

2. **⚙️ Configure environment variables:**

    * Copy the `.env.dist` file to `.env`:

        ```bash
        cp .env.dist .env
        ```

    * Fill in the required values in the `.env` file. This includes database credentials, API keys for music services, and JWT secret.

3. **🏗️ Start the services using Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images and start all the necessary services (API, PostgreSQL, Redis, Celery worker etc.).

## 📖 Usage

Once the application is running, you can access the API endpoints.

### API Endpoints

The API is documented using OpenAPI (Swagger). You can access the interactive documentation at `http://localhost:2000/docs` (replace `2000` with your configured `BACKEND_PORT`).


### Connecting Music Accounts

To connect your music accounts, you need to follow the OAuth2 flow:

1. Navigate to the login endpoint for the desired service (e.g., `/api/v1/spotify/login`). This will return an authorization URL.
2. Open the authorization URL in your browser. You will be prompted to log in to the music service and grant permissions to the Wolns API.
3. After granting permissions, you will be redirected to the callback URL (e.g., `/api/v1/spotify/callback`) with an authorization code.
4. The callback endpoint will exchange the authorization code for access and refresh tokens

## 🛠️ Development

### Contributing

We welcome contributions to the Wolns API project! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes, ensuring that the code follows the project's coding style (PEP 8).
4. Commit your changes and push them to your fork.
5. Submit a pull request to the main repository.

### Code Style

The project uses `ruff` for linting and formatting. Please ensure your code passes the linting checks before submitting a pull request.

## 📈 Monitoring

The application includes integration with Prometheus and Grafana for monitoring:

* **Prometheus:** Collects metrics from the application. Access Prometheus at `http://localhost:9090`.
* **Grafana:** Provides dashboards for visualizing the collected metrics. Access Grafana at `http://localhost:3000`.

## 📝 License

This project is licensed under the [GNU General Public License v3.0
](LICENSE).
