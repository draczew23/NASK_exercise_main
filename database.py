import ipaddress
import json

class Database:
    """
    Represents a database of IP tags loaded from a JSON file.

    Attributes:
        filename (str): The path to the JSON file containing IP tags data.
        ip_tags_database (list): A list of dictionaries representing IP tags entries.

    Methods:
        load_database(): Load the IP tags database from the specified JSON file.
        get_tags_for_ip(ip_address): Retrieve tags associated with a given IP address.

    Example:
        >>> db = Database('ip_tags_data.json')
        >>> tags = db.get_tags_for_ip('192.168.1.1')
    """
    def __init__(self, filename, logger=None):
        """
        Initialize a Database instance.

        Args:
            filename (str): The path to the JSON file containing IP tags data.
        """
        self.filename = filename
        self.logger = logger
        self.load_database()
        
    def load_database(self):
        """
        Load the IP tags database from the specified JSON file.
        """
        try:
            with open(self.filename, encoding="utf-8") as f:
                self.ip_tags_database = json.load(f)
        except FileNotFoundError as e:
            self.logger.critical(f"Error loading database: {str(e)}")
            raise FileNotFoundError(f"Error loading database: {str(e)}") from e
        except json.JSONDecodeError as e:
            self.logger.critical(f"Error decoding JSON data: {str(e)}")
            raise ValueError(f"Error decoding JSON data: {str(e)}") from e

    def get_tags_for_ip(self, ip_address):
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

        for entry in self.ip_tags_database:
            try:
                network = ipaddress.ip_network(entry['ip_network'])
                if ip_address_conv in network:
                    if entry['tag'] not in tags:
                        tags.append(entry['tag'])
            except ValueError:
                continue

        tags.sort()
        self.logger.info("Managed to successfully read the data from the database and acquire tags")
        return tags
