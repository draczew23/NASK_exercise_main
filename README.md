# IP Tagging Service

This project implements an HTTP-based service that provides two endpoints for tagging IPv4 addresses and generating tag reports.

## Description
The IP Tagging Service allows clients to query two endpoints:
- **Endpoint 1 (GET /ip-tags/{ip})**:
  - Returns a JSON list of unique and sorted tags for the specified IPv4 address.
  - Handles cases where no tags correspond to the IP address by returning an empty list.

- **Endpoint 2 (GET /ip-tags-report/{ip})**:
  - Generates an HTML table report presenting tags associated with the provided IPv4 address.
  - Tags are displayed in individual cells within the table for readability.

A simple base of ip address is provided to interact with the IP Tagging Service. This base is stored in the **ip_base.json** file. Interaction with the database is conducted through the **database.py** file.

## Usage

To use the service:
1. Extract the archive into desirable directory.
2. Enter the directory `cd NASK_exercise_main`.
3. Start the application container with `docker-compose up`.
4. Access the service endpoints:
   - `GET /ip-tags/{ip}` for JSON response.
   - `GET /ip-tags-report/{ip}` for HTML report.

Access the application at:
```bash
  http://0.0.0.0:8080
```
Example usage of the first endpoint:
```bash
  http://0.0.0.0:8080/ip-tags/198.51.100.227
```

Example usage of the second endpoint:
```bash
  http://0.0.0.0:8080/ip-tags-report/198.51.100.227
```


All important events are stored in the **app.log** file.

## Technologies Used

- **Flask**: Python micro-framework for web development.
- **Gunicorn**: WSGI HTTP server for running Flask applications.
- **Docker**: Containerization platform for packaging and running applications.

## Requirements

Ensure you have the following installed:
- Docker
- Python 3.12
- pip3

## Running Tests

To run tests, run the following command

```bash
  docker-compose run my_app python check_app.py
```

There are four simple unit tests implemented. 
#### TO DO:
- missing database test 
- unexpected errors tests for both endpoints
## Author

Jakub Wiechnik
## License

[MIT](https://choosealicense.com/licenses/mit/)



