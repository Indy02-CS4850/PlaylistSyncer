from flask import Flask, request, jsonify
from flask_cors import CORS
import applemusicpy

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def hello_world():
    data = {'message': 'Hello from Python backend!'}
    secret_key = '''CONTACT NIKITA FOR ACCESS'''
    key_id = 'Q6TGY5D7M2'
    team_id = '6BTDC7TLBV'

    am = applemusicpy.AppleMusic(secret_key, key_id, team_id)
    results = am.search('sea power', types=['albums'], limit=5)

    for item in results['results']['albums']['data']:
        print(item['attributes']['name'])
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
