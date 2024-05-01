from flask import Flask, jsonify
import ipaddress
import json

# Opening our database from JSON file
f = open('ip_base.json')
IP_TAGS_DATABASE = json.load(f)

app = Flask(__name__)

def get_tags_for_ip(ip_address):
    ip_address_conv = ipaddress.ip_address(ip_address)
    tags = []
    for entry in IP_TAGS_DATABASE:
        try:
            network = ipaddress.ip_network(entry['ip_network'])
            if ip_address_conv in network:
                if entry['tag'] in tags:
                    continue
                else:
                    tags.append(entry['tag'])
        except ValueError:
            continue
    tags.sort()
    return tags

@app.route('/ip-tags/<ip>', methods=['GET'])
def ip_tags(ip):
    tags = get_tags_for_ip(ip)
    return jsonify(tags), 200

f.close()