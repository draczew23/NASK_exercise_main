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
            logger (Logger, optional): The logger instance for logging errors. Defaults to None.
        """
        self.filename = filename
        self.logger = logger
        self.load_database()
        
    def load_database(self):
        """
        Load the IP tags database from the specified JSON file.

        Raises:
            FileNotFoundError: If the specified JSON file is not found.
            ValueError: If there is an error decoding JSON data from the file.
        """
        try:
            with open(self.filename, encoding="utf-8") as f:
                self.ip_tags_database = json.load(f)
        except FileNotFoundError as e:
            error_message = f"Error loading database: {str(e)}"
            if self.logger:
                self.logger.critical(error_message)
            raise FileNotFoundError(error_message) from e
        except json.JSONDecodeError as e:
            error_message = f"Error decoding JSON data: {str(e)}"
            if self.logger:
                self.logger.critical(error_message)
            raise ValueError(error_message) from e

    def get_tags_for_ip(self, ip_address):
        """
        Retrieve tags associated with a given IP address from the predefined IP tags database.

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
        if self.logger:
            self.logger.info("Successfully retrieved tags from the database.")
        return tags
