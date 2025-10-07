# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a Flask-based Slack bot that integrates with external APIs. The bot provides two main capabilities:

1. **Interactive Slack Commands**: Users can query API resources via `/search` slash commands
2. **Kafka-based Notifications**: Async notification system that pushes events to Slack channels via Kafka Connect with a Camel Slack Sink Connector

### Key Components

**Flask Application** ([main.py](main.py)):
- Entry point that creates the Flask app
- Registers Slack listeners and API blueprints during app context initialization
- Slack Bolt app ([slack.py](slack.py)) is initialized with OAuth flow and signing secret

**OAuth Flow** ([oauth/oauth.py](oauth/oauth.py), [oauth/installation_store.py](oauth/installation_store.py)):
- Custom OAuth callback handlers for installation success/failure
- File-based installation store at `./db/.installations`
- Handles both workspace and enterprise installs
- State validation enabled with cookie-based state store

**API Routes** ([api/__init__.py](api/__init__.py)):
- `/slack/events/` - Slack event subscriptions and slash commands endpoint
- `/slack/oauth/redirect` - OAuth redirect URI
- `/slack/install-link` - Installation page

**Listeners** ([listeners/__init__.py](listeners/__init__.py)):
- Event listeners in `listeners/events/` (e.g., `app_home_opened`)
- Command listeners in `listeners/commands/` (e.g., `/search` command handler)
- Registered to the Slack Bolt app during initialization

**API Integration** ([api_client/service.py](api_client/service.py)):
- `APIService` class provides HTTP client facade for external API
- Authentication via `api_client.auth.get_access_token()` (currently uses static token from env)
- Main method: `get_object_by_name_preview(modelled_system, object_name, category)` returns object preview data

**Notifications System**:
- Kafka Connect with Camel Slack Sink Connector consumes from `slack-notifications` topic
- Messages published to Kafka are automatically forwarded to Slack channel
- Configuration in [notifications/config/KafkaSlackCamelSinkConnector.conf](notifications/config/KafkaSlackCamelSinkConnector.conf)

## Development Commands

### Local Development Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt  # for development
   ```

2. **Configure environment** - Create `.env` file:
   ```
   BASE_URL=https://your-ngrok-url.ngrok.io
   SLACK_CLIENT_ID=your_client_id
   SLACK_CLIENT_SECRET=your_client_secret
   SLACK_SIGNING_SECRET=your_signing_secret
   API_TOKEN=your_jwt_token
   API_BASE_URL=https://api.example.com/v2
   ```

3. **Start ngrok tunnel** (for local Slack webhook testing):
   ```bash
   ngrok http 5000
   ```

4. **Run the Flask app**:
   ```bash
   flask --app main run
   ```

### Kafka Notifications Setup

1. **Start Kafka and Connect**:
   ```bash
   docker compose up connect
   ```

2. **Wait for Connect to be ready**:
   ```bash
   curl localhost:8083
   ```

3. **Create Kafka topic**:
   ```bash
   kafka-topics --bootstrap-server localhost:9092 --topic slack-notifications --create
   ```

4. **Deploy Slack Sink Connector** (requires Camel Slack Sink Connector in `/tmp/custom/jars`):
   ```bash
   curl -XPOST -d @notifications/config/KafkaSlackCamelSinkConnector.conf -H "Content-Type: application/json" http://localhost:8083/connectors | jq '.'
   ```

5. **Test notification**:
   ```bash
   kafka-console-producer --bootstrap-server localhost:9092 --topic slack-notifications
   # Then type message and press Enter
   ```

## Configuration Notes

- **Slack App Manifest**: [manifest.yaml](manifest.yaml) contains the Slack app configuration (must be manually updated with ngrok URL for local dev)
- **API Authentication**: Currently uses static JWT token from `.env` (`API_TOKEN`). The `get_access_token(user)` function in `api_client/auth.py` should be enhanced for proper per-user auth
- **Installation Storage**: File-based storage in `./db/.installations` (not suitable for production)
