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

def generate_html_table(key, tags):
    html_table = "<table border='1'>\n"  # Rozpoczęcie budowania tabeli HTML
    html_table += "<tr><th>Klucz</th><th>Tagi</th></tr>\n"  # Dodanie nagłówków

    html_table += f"<tr><td>{key}</td>"  # Dodanie klucza w pierwszej kolumnie
    html_table += "<td>"  # Rozpoczęcie drugiej kolumny dla tagów

    for idx, tag in enumerate(tags):
        if idx > 0:
            html_table += "<hr>"  # Dodanie linii poziomej przed każdym tagiem (jeśli nie jest to pierwszy tag)
        html_table += f"<p>{tag}</p>"  # Dodanie tagu w nowym wierszu

    html_table += "</td></tr>\n"  # Zamknięcie drugiej kolumny i wiersza
    html_table += "</table>"  # Zakończenie tabeli HTML

    return html_table


@app.route('/ip-tags/<ip>', methods=['GET'])
def ip_tags(ip):
    tags = get_tags_for_ip(ip)
    return jsonify(tags), 200

@app.route('/ip-tags-report/<ip>', methods=['GET'])
def ip_tags_report(ip):
    tags = get_tags_for_ip(ip)
    key = ip
    return generate_html_table(key, tags), 200

f.close()