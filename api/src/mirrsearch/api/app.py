"""
Create barebones Flask app
Run with: python kickoff_app.py
"""

import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests

def create_app():
    """
    Create the application instance and define the routes
    """
    app = Flask(__name__)
    CORS(app)

    @app.route('/data')
    def get_data():
        data = {"message": "hello world", "status": 200}
        return jsonify(data)

    @app.route('/search_dockets')
    def search_dockets():
        response = {}

        # Obtains the search term
        search_term = request.args.get('term')

        # If a search term is not provided, the server will return this JSON and a 400 status code
        if not search_term:
            response['error'] = {'code': 400,
                                 'message': 'Error: You must provide a term to be searched'}
            return jsonify(response), 400

        # If the search term is valid, data will be ingested into the JSON response
        response['data'] = {
            'search_term': search_term,
            'dockets': []
        }
        response['data']['dockets'].append({
           'title': 'Designation as a Preexisting Subscription Service',
           'id': "COLC-2006-0014",
           'link': 'https://www.regulations.gov/docket/COLC-2006-0014',
           'number_of_comments': 0,
           'number_of_documents': 1
           })
        return jsonify(response)

    @app.route('/search_documents')
    def search_documents():
        response = {}

        # Obtains the search term and document id from a prior request
        search_term = request.args.get('term')
        document_id = request.args.get('document_id')

        # If a search term is not provided, the server will return this JSON and a 400 status code
        if not search_term:
            response['error'] = {'code': 400,
                                 'message': 'Error: You must provide a term to be searched'}
            return jsonify(response), 400

        # If the search term is valid, data will be ingested into the JSON response
        response['data'] = {
            'search_term': search_term,
            'comments': []
        }
        response['data']['comments'].append({
            "author": "Environmental Protection Agency",
            "date_posted": "Dec 22, 2003",
            "link": "https://www.regulations.gov/document/EPA-HQ-OAR-2003-0083-0794",
            "document_id": document_id
           })
        return jsonify(response)

    @app.route('/search_comments')
    def search_comments():
        response = {}

        # Obtains the search term and docket id from a prior request
        search_term = request.args.get('term')
        docket_id = request.args.get('docket_id')

        # If a search term is not provided, the server will return this JSON and a 400 status code
        if not search_term:
            response['error'] = {'code': 400,
                                 'message': 'Error: You must provide a term to be searched'}
            return jsonify(response), 400
        if not docket_id:
            response['error'] = {'code': 400,
                                 'message': 'Error: You must provide a docket_id to be searched'}
            return jsonify(response), 400

        # If the search term is valid, data will be ingested into the JSON response
        response['data'] = {
            'search_term': search_term,
            'comments': []
        }

        response['data']['comments'].append({
            "author": "Department of Health and Human Services",
            "date_posted": "Apr 14, 2011",
            "link": "https://www.regulations.gov/comment/HHS-OS-2010-0014-0032",
            "docket_id": docket_id
           })
        return jsonify(response)

    @app.route('/opensearch')
    def opensearch():
        response = {}

        load_dotenv()

        username = os.getenv("OPENSEARCH_USERNAME")
        password = os.getenv("OPENSEARCH_PASSWORD")

        # Obtains the search term
        search_term = request.args.get('term')

        # If a search term is not provided, the server will return this JSON and a 400 status code
        if not search_term:
            response['error'] = {'code': 400,
                                 'message': 'Error: You must provide a term to be searched'}
            return jsonify(response), 400

        # If the search term is valid, data will be ingested into the JSON response
        host = 'https://search-opensearch334-n6exkzbydhrfh64hs4jw4bo4h4.aos.us-east-1.on.aws'
        index = "dockets"
        url = f"{host}/{index}/_search"
        query = {
            "size": 25,
            "query": {
                "match": {
                    "data.attributes.title": {
                        "query": search_term,
                        "fuzziness": "AUTO"
                    }
                }
            }
        }

        headers = {"Content-Type": "application/json"}

        try:
            r = requests.get(url, auth=(username, password),
                             headers=headers, data=json.dumps(query))
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return e

        return r.json()

        # response['data']['dockets'].append({
        #    'title': 'Designation as a Preexisting Subscription Service',
        #    'id': "COLC-2006-0014",
        #    'link': 'https://www.regulations.gov/docket/COLC-2006-0014',
        #    'number_of_comments': 0,
        #    'number_of_documents': 1
        #    })
        # return jsonify(response)

    return app

def launch():
    """
    Launch the Flask app
    """
    return create_app()

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(debug=True, port=8000, host='0.0.0.0')
