# cargopulse-api

This is a proof-of-concept (POC) project for demonstrating cloud monitoring of application metrics and secrets management using Google Cloud Platform (GCP) services.

## Overview

The CargoPulse POC aims to showcase how to monitor application metrics and manage secrets effectively using GCP services. It provides a simple API for managing logistics-related tasks such as shipment tracking and user management.

## Features

- User authentication with JWT
- API key management
- Shipment management
- Cloud monitoring for application metrics visualization
- Secrets management with GCP Secrets Manager

## Technologies Used

- Flask: Web framework for building the API endpoints
- Google Cloud Platform (GCP) services:
  - Cloud Datastore: For storing user and shipment data
  - Cloud Monitoring: For monitoring application metrics
  - Secrets Manager: For managing secrets securely
- Pydantic: For data validation and configuration
- RESTX: For API documentation and validation
- JWT: For user authentication
- Docker and Docker Compose: For containerization and orchestration

## Usage

- Authentication: Use JWT tokens for authenticating API requests.
- Shipment Management: Create and update shipments.
- User Management: Manage users and API keys for accessing the API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
