# IP Tagging Service

This project implements an HTTP-based service that provides two endpoints for tagging IPv4 addresses and generating tag reports.

## Description

The IP Tagging Service allows clients to query two endpoints:
1. **GET /ip-tags/{ip}**: Retrieves a list of unique and sorted tags associated with a specific IPv4 address in JSON format.
2. **GET /ip-tags-report/{ip}**: Generates an HTML report containing a table displaying tags associated with a given IPv4 address.

## Key Features

- **Endpoint 1 (GET /ip-tags/{ip})**:
  - Returns a JSON list of unique and sorted tags for the specified IPv4 address.
  - Handles cases where no tags correspond to the IP address by returning an empty list.

- **Endpoint 2 (GET /ip-tags-report/{ip})**:
  - Generates an HTML table report presenting tags associated with the provided IPv4 address.
  - Tags are displayed in individual cells within the table for readability.

## Usage

To use the service:
1. Clone the repository to your local environment.
2. Build the Docker image using `docker-compose build`.
3. Start the application container with `docker-compose up`.
4. Access the service endpoints:
   - `GET /ip-tags/{ip}` for JSON response.
   - `GET /ip-tags-report/{ip}` for HTML report.

Access the application

## Technologies Used

- Flask: Python micro-framework for web development.
- Gunicorn: WSGI HTTP server for running Flask applications.
- Docker: Containerization platform for packaging and running applications.

## Requirements

Ensure you have the following installed:
- Docker
- Python 3.12
- pip3

## Author

Jakub Wiechnik