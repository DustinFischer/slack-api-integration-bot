# Slack API Integration Bot

A Flask-based Slack bot that integrates with external APIs to provide search functionality and real-time notifications through Slack.

## Features

- **Slack Command Integration**: Search and discover API resources using `/search` slash commands
- **OAuth Flow**: Secure workspace installation with custom OAuth callbacks
- **Kafka-based Notifications**: Asynchronous notification system using Kafka Connect with Camel Slack Sink Connector
- **Interactive Home Tab**: Custom app home experience for users
- **Multi-workspace Support**: File-based installation store for multiple workspace installations

## Architecture

This bot demonstrates a production-ready pattern for integrating Slack with external APIs:

- **Flask** web framework with **Slack Bolt** for Slack app development
- **OAuth 2.0** authentication flow for secure app installation
- **Kafka Connect** for scalable, decoupled notification delivery
- Modular architecture separating API client, listeners, and UI composition

## Setup

### Prerequisites

- Python 3.10+
- Kafka (for notifications feature)
- ngrok (for local development)

### Local Development Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt  # for development
   ```

2. **Create a Slack App**:
   - Go to [Slack API Apps](https://api.slack.com/apps)
   - Create a new app using the `manifest.yaml` file
   - Update the ngrok URLs in `manifest.yaml` with your ngrok URL

3. **Configure environment** - Create `.env` file:
   ```env
   BASE_URL=https://your-ngrok-url.ngrok.io

   SLACK_CLIENT_ID=your_client_id
   SLACK_CLIENT_SECRET=your_client_secret
   SLACK_SIGNING_SECRET=your_signing_secret

   API_TOKEN=your_api_jwt_token
   API_BASE_URL=https://api.example.com/v2
   ```

4. **Start ngrok tunnel** (for local Slack webhook testing):
   ```bash
   ngrok http 5000
   ```

5. **Update Slack App URLs**:
   - In Slack App settings, set OAuth redirect URL to: `https://your-ngrok-url.ngrok.io/slack/oauth/redirect`
   - Set Event Subscriptions URL to: `https://your-ngrok-url.ngrok.io/slack/events/`

6. **Run the Flask app**:
   ```bash
   flask --app main run
   ```

7. **Install the app to your workspace**:
   - Navigate to `http://localhost:5000/slack/install-link`
   - Click "Add to Slack" and authorize the app

## Kafka Notifications Setup (Optional)

The notification system allows publishing messages to Kafka that are automatically forwarded to Slack channels.

### Setup Steps

1. **Download Kafka Camel Slack Sink Connector**:
   - Download from [Apache Camel Kafka Connector](https://camel.apache.org/camel-kafka-connector/3.18.x/reference/index.html)
   - Extract and place in `/tmp/custom/jars`

2. **Update webhook URL**:
   - Get webhook URL from your Slack app installation
   - Update `notifications/config/KafkaSlackCamelSinkConnector.conf` with your webhook URL

3. **Start Kafka and Connect**:
   ```bash
   docker compose up connect
   ```

4. **Wait for Connect to be ready**:
   ```bash
   # Poll until you get a response
   curl localhost:8083
   ```

5. **Create Kafka topic**:
   ```bash
   kafka-topics --bootstrap-server localhost:9092 --topic slack-notifications --create
   ```

6. **Deploy Slack Sink Connector**:
   ```bash
   curl -XPOST -d @notifications/config/KafkaSlackCamelSinkConnector.conf \
     -H "Content-Type: application/json" \
     http://localhost:8083/connectors | jq '.'
   ```

7. **Test notification**:
   ```bash
   kafka-console-producer --bootstrap-server localhost:9092 --topic slack-notifications
   # Type a message and press Enter
   > Hello from Kafka!
   ```

The message should appear in your configured Slack channel (`#api-notifications` by default).

## Project Structure

```
.
├── api/                    # Flask API blueprints
│   ├── events/            # Slack event handlers
│   └── oauth/             # OAuth endpoints
├── api_client/            # External API client
│   ├── auth.py           # Authentication logic
│   ├── models.py         # API data models
│   └── service.py        # HTTP client service
├── composition/           # UI components
│   ├── commands/         # Slash command UI
│   └── views/            # App home and modals
├── listeners/            # Slack event listeners
│   ├── commands/        # Command handlers
│   └── events/          # Event handlers
├── notifications/       # Kafka notification config
├── oauth/              # OAuth flow implementation
├── static/             # Static assets (icons, etc.)
├── utils/              # Utility functions
├── config.py           # Application configuration
├── main.py            # Flask app factory
├── slack.py           # Slack Bolt app initialization
└── manifest.yaml      # Slack app manifest
```

## Technologies Used

- **Flask** - Web framework
- **Slack Bolt** - Slack app development framework
- **Kafka** - Message streaming platform
- **Apache Camel Kafka Connector** - Kafka to Slack integration
- **Docker Compose** - Container orchestration for Kafka stack

## Use Cases

This project demonstrates:
- Building Slack bots with custom OAuth flows
- Integrating third-party APIs with Slack
- Implementing scalable notification systems with Kafka
- Multi-workspace Slack app development
- Interactive Slack UI components (home tabs, modals, commands)

## License

MIT

## Author

Portfolio project demonstrating Slack bot development and event-driven architecture.
