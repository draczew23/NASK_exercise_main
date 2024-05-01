from flask import Flask, request
import ipaddress
import json

IP_TAGS_DATABASE = [
    {"tag": "foo", "ip_network": "192.0.2.0/24"},
    {"tag": "just a TAG", "ip_network": "198.51.100.0/24"},
    {"tag": "{$(a-tag)$}", "ip_network": "198.51.100.0/24"},
    {"tag": "zażółć ♥", "ip_network": "198.51.100.0/24"},
    {"tag": "foo", "ip_network": "192.0.2.0/24"},
    {"tag": "bar", "ip_network": "192.0.2.8/29"},
    {"tag": "bar", "ip_network": "10.20.0.0/16"},
    {"tag": "SPAM", "ip_network": "10.20.30.40/32"},
]

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

@app.route('/ip-tags')
def ip_tags():
    ip_address = request.args.get('ip')
    tags = get_tags_for_ip(ip_address)
    return tags, 200