import ipaddress
from flask import Flask, jsonify
from database import Database

# Opening our database from JSON file
db = Database('ip_base.json')
# App initialization
app = Flask(__name__)

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

class InvalidIPAddress(Exception):
    pass

@app.errorhandler(InvalidIPAddress)
def handle_invalid_ip_address(error):
    response = jsonify({'error': 'Invalid IP address format'})
    response.status_code = 400
    return response


@app.route('/ip-tags/<ip>', methods=['GET'])
def ip_tags(ip):
    """
    Retrieve and return tags associated with the specified IP address.

    Args:
        ip (str): The IP address for which tags are to be retrieved.

    Returns:
        Response: A JSON response containing a list of tags associated with the IP address.
                  The response status code is 200 (OK) on success.

    Example:
        >>> # Sending a GET request to '/ip-tags/192.168.1.1' will return a JSON response with tags.
    """
    try:
        ipaddress.ip_address(ip)
    except ValueError as e:
        raise InvalidIPAddress from e
    
    tags = db.get_tags_for_ip(ip)
    return jsonify(tags), 200

@app.route('/ip-tags-report/<ip>', methods=['GET'])
def ip_tags_report(ip):
    """
    Generate an HTML report containing tags associated with the specified IP address.

    Args:
        ip (str): The IP address for which tags are to be included in the HTML report.

    Returns:
        Response: An HTML response containing a table with the specified IP address as the key
                  and associated tags in separate rows. The response status code is 200 (OK) on success.

    Example:
        >>> # Sending a GET request to '/ip-tags-report/192.168.1.1' will return an HTML report.
    """
    tags = db.get_tags_for_ip(ip)
    key = ip
    return generate_html_table(key, tags), 200

if __name__ == '__main__':
    app.run(debug=True)
