import ipaddress
import json
from flask import Flask, jsonify

# Opening our database from JSON file
f = open('ip_base.json',  encoding="utf-8")
IP_TAGS_DATABASE = json.load(f)

app = Flask(__name__)

def get_tags_for_ip(ip_address):
    """
    Retrieves tags associated with a given IP address from a predefined IP tags database.

    Args:
        ip_address (str): The IP address for which tags are to be retrieved.

    Returns:
        list: A sorted list of unique tags associated with the IP address. If no tags
              are found for the IP address, an empty list is returned.
    """
    ip_address_conv = ipaddress.ip_address(ip_address)
    tags = []

    # Loop through entries in the IP_TAGS_DATABASE
    for entry in IP_TAGS_DATABASE:
        try:
            network = ipaddress.ip_network(entry['ip_network'])
            # Check if the IP address is within the defined network
            if ip_address_conv in network:
                # Check if the tag associated with the network entry is already in the list
                if entry['tag'] in tags:
                    continue  # Skip if the tag is already added

                tags.append(entry['tag'])  # Add the tag to the list
        except ValueError:
            continue  # Skip this entry if there's an invalid network format

    tags.sort()  # Sort the list of tags lexicographically
    return tags


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
    Retrieve and return tags associated with the specified IP address.

    Args:
        ip (str): The IP address for which tags are to be retrieved.

    Returns:
        Response: A JSON response containing a list of tags associated with the IP address.
                  The response status code is 200 (OK) on success.

    Example:
        >>> # Sending a GET request to '/ip-tags/192.168.1.1' will return a JSON response with tags.
    """
    tags = get_tags_for_ip(ip)
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
    tags = get_tags_for_ip(ip)
    key = ip
    return generate_html_table(key, tags), 200

f.close()
