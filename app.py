import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from database import Database

app = Flask(__name__)

# Logger configuration settings
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=1)
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

db = Database('ip_base.json', logger=app.logger)

@app.route('/ip-tags/', methods=['GET'])
def missing_ip_error():
    """
    Handle error when IP address is missing in /ip-tags/ request.

    Returns:
        Response: A JSON response with error details and HTTP status code 400.
    """
    error_message = 'IP address is missing. Please provide a valid IP address.'
    app.logger.error(error_message)
    return jsonify({'error': 'Bad request', 'message': error_message}), 400

def generate_html_table(key, tags):
    """
    Generates an HTML table representing a key with associated tags in a seperate column.

    Args:
        key (str): The key or identifier to be displayed in the table.
        tags (list): A list of strings representing tags associated with the key.

    Returns:
        str: A string containing HTML code for a table with the given key and tags.
             Each tag is displayed in a separate row within the table cell.
    """
    html_table = "<table border='1'>\n"  # Start building the HTML table
    html_table += "<tr><th>Klucz</th><th>Tagi</th></tr>\n"  # Add headers

    html_table += f"<tr><td>{key}</td>"  # Add the key in the first column
    html_table += "<td>"  # Start the second column for tags

    for idx, tag in enumerate(tags):
        if idx > 0:
            html_table += "<hr>"  # Add a horizontal line before each tag (except the first one)
        html_table += f"<p>{tag}</p>"  # Add the tag in a new row

    html_table += "</td></tr>\n"  # Close the second column and the row
    html_table += "</table>"  # End the HTML table

    return html_table


@app.route('/ip-tags/<ip>', methods=['GET'])
def ip_tags(ip):
    """
    Retrieve tags associated with the specified IP address.

    Args:
        ip (str): The IP address to retrieve tags for.

    Returns:
        Response: JSON response containing the tags associated with the IP address.
                  Status code 200 on success, or appropriate error response on failure.
    """
    if not ip:
        return missing_ip_error()
    try:
        tags = db.get_tags_for_ip(ip)
        return jsonify(tags), 200
    except ValueError as e:
        app.logger.error(f"Invalid IP address '{ip}': {str(e)}")
        return jsonify({'error': 'Bad request', 'message': 'Invalid IPv4 address format.'}), 400
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred.'}), 500

@app.route('/ip-tags-report/<ip>', methods=['GET'])
def ip_tags_report(ip):
    """
    Generate an HTML report containing tags associated with the specified IP address.

    Args:
        ip (str): The IP address to generate the report for.

    Returns:
        str: HTML content representing a report table of tags associated with the IP address.
             Status code 200 on success, or appropriate error response on failure.
    """
    if not ip:
        return missing_ip_error()
    try:
        tags = db.get_tags_for_ip(ip)
        key = ip
        html_table = generate_html_table(key, tags)
        return html_table, 200
    except ValueError as e:
        app.logger.error(f"Invalid IP address '{ip}': {str(e)}")
        return jsonify({'error': 'Bad request', 'message': 'Invalid IPv4 address format.'}), 400
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    app.run()
