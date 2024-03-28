# cargopulse-api

This is a proof-of-concept (POC) project for demonstrating cloud monitoring of application metrics and secrets management using Google Cloud Platform (GCP) services.

## Overview

The CargoPulse POC aims to showcase how to monitor application metrics and manage secrets effectively using GCP services. It provides a simple API for managing logistics-related tasks such as shipment tracking and user management.

## Features

- User authentication with JWT
- API key management
- Shipment management
- Webhook integration for shipment state notifications
- Cloud monitoring for application metrics visualization
- Secrets management with GCP Secrets Manager

## Technologies Used

- Flask: Web framework for building the API endpoints
- Google Cloud Platform (GCP) services:
  - Cloud Datastore: For storing user and shipment data
  - Cloud Tasks: For webhook integration
  - Cloud Monitoring: For monitoring application metrics
  - Secrets Manager: For managing secrets securely
- Pydantic: For data validation and configuration
- RESTX: For API documentation and validation
- JWT: For user authentication
- Docker and Docker Compose: For containerization and orchestration

## Getting Started

1. Clone the repository.
2. Set up a GCP project and enable the necessary services.
3. Configure secrets in GCP Secrets Manager.
4. Set up environment variables or secrets for authentication credentials.
5. Deploy the application to GCP using Cloud Run or another suitable service.
6. Access the API endpoints to manage shipments and users.
7. Monitor application metrics using GCP Cloud Monitoring dashboards.

## Usage

- Authentication: Use JWT tokens for authenticating API requests.
- Shipment Management: Create, update, and delete shipments.
- User Management: Manage users and API keys for accessing the API.
- Webhook Integration: Set up webhook URLs for receiving shipment state notifications.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
