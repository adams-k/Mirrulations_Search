"""
Flask app for the Mirrsearch API
"""

import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from mirrsearch.api.query_manager import MongoQueryManager
from mirrsearch.api.database_manager import MongoManager
from mirrsearch.api.mock_database_manager import MockMongoDatabase
from mirrsearch.api.mock_query_manager import MockMongoQueries

def create_app(query_manager):
    """
    Create the application instance and define the routes
    """
    app = Flask(__name__)
    CORS(app)

    @app.route('/data')
    def get_data():
        data = {"message": "hello world", "status": 200}
        return jsonify(data)

    @app.route('/zip_data')
    def zip_data():
        data = {"message": "The email to download your data will be sent shortly", "status": 200}
        return jsonify(data)

    @app.route('/search_dockets')
    def search_dockets():
        # Obtains the search term
        search_term = request.args.get('term')

        # If a search term is not provided, the server will return this JSON and a 400 status code
        if not search_term:
            response = {}
            response['error'] = {'code': 400,
                                 'message': 'Error: You must provide a term to be searched'}
            return jsonify(response), 400


        # If the search term is valid, data will be ingested into the JSON response
        response = query_manager.search_dockets(search_term)

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
        # Obtains the search term and docket id from a prior request
        search_term = request.args.get('term')
        docket_id = request.args.get('docket_id')

        # If a search term is not provided, the server will return this JSON and a 400 status code
        if not search_term:
            response = {}
            response['error'] = {'code': 400,
                                 'message': 'Error: You must provide a term to be searched'}
            return jsonify(response), 400
        if not docket_id:
            response = {}
            response['error'] = {'code': 400,
                                 'message': 'Error: You must provide a docket_id to be searched'}
            return jsonify(response), 400

        response = query_manager.search_comments(search_term, docket_id)

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
            dockets = requests.get(url, auth=(username, password),
                             headers=headers, data=json.dumps(query), timeout=60)
            dockets.raise_for_status()
        except requests.exceptions.RequestException as e:
            return e

        dockets = dockets.json()
        response['data'] = {
                'dockets': []
            }
        for docket in dockets["hits"]["hits"]:
            response['data']['dockets'].append({
                'title': docket["_source"]["data"]["attributes"]["title"],
                'id': docket["_source"]["data"]["id"],
                'link': docket["_source"]["data"]["links"]["self"],
                'docket_type': docket["_source"]["data"]["attributes"]["docketType"],
                'documents_containing': 0,
                'total_documents': 0,
                'date_range': 'null',
                'comment_date_range': "null",
                'comments_containing': 0,
                'total_comments': 0,
            })

        return jsonify(response)

    return app

def launch(database):
    """
    Launch the Flask app
    """
    if database == 'mongo':
        database_manager = MongoManager()
        query_manager = MongoQueryManager(database_manager)
        return create_app(query_manager)
    if database == 'mockMongo':
        database_manager = MockMongoDatabase()
        query_manager = MockMongoQueries(database_manager)
        return create_app(query_manager)
    raise ValueError('Invalid database type')

if __name__ == '__main__':
    flask_app = launch('mongo')
    flask_app.run(debug=True, port=8000, host='0.0.0.0')
