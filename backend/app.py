from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database import db
from models import ApiHit, ApiLog
import datetime

# Load environment variables from .env
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Ensure tables are created
with app.app_context():
    db.create_all()

# Function to log audit entries
def log_audit(operation, endpoint, request_type, user_agent, request_body, response_status):
    log = ApiLog(
        operation=operation,
        endpoint=endpoint,
        request_type=request_type,
        user_agent=user_agent,
        request_body=request_body,
        response_status=response_status,
        timestamp=datetime.datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()

# Middleware to log API hits for all requests
@app.before_request
def log_api_hit():
    if request.method != 'OPTIONS':  # Exclude OPTIONS requests
        user_agent = request.headers.get('User-Agent')
        request_type = request.method
        request_body = request.get_json(silent=True)  # Try to get JSON data from request body
        
        new_hit = ApiHit(
            request_type=request_type,
            endpoint=request.path,
            user_agent=user_agent,
            request_body=str(request_body),  # Convert to string if JSON data exists
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add(new_hit)
        db.session.commit()

# Routes

@app.route('/api/hits/stats', methods=['GET'])
def get_stats():
    hits = ApiHit.query.all()
    data = {
        "pieChartData": {},
        "barChartData": {
            "labels": [],
            "values": []
        },
        "tableData": []
    }

    for hit in hits:
        # Collecting pie chart data
        if hit.user_agent in data["pieChartData"]:
            data["pieChartData"][hit.user_agent] += 1
        else:
            data["pieChartData"][hit.user_agent] = 1

        # Collecting bar chart data
        date_str = hit.timestamp.strftime('%Y-%m-%d')
        if date_str in data["barChartData"]["labels"]:
            idx = data["barChartData"]["labels"].index(date_str)
            data["barChartData"]["values"][idx] += 1
        else:
            data["barChartData"]["labels"].append(date_str)
            data["barChartData"]["values"].append(1)

        # Collecting table data
        data["tableData"].append({
            "id": hit.id,
            "request_type": hit.request_type,
            "endpoint": hit.endpoint,
            "user_agent": hit.user_agent,
            "request_body": hit.request_body,
            "timestamp": hit.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(data)

@app.route('/api/hits', methods=['POST'])
def create_hit():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON data or Content-Type header missing'}), 400

    user_agent = request.headers.get('User-Agent')
    request_type = request.method

    new_hit = ApiHit(
        request_type=request_type,
        endpoint=data.get('endpoint'),
        user_agent=user_agent,
        request_body=data.get('request_body', None),
        timestamp=datetime.datetime.utcnow()
    )
    try:
        db.session.add(new_hit)
        db.session.commit()
        log_audit('CREATE', '/api/hits', request_type, user_agent, data, 201)
        return jsonify(new_hit.as_dict()), 201
    except Exception as e:
        db.session.rollback()
        log_audit('CREATE', '/api/hits', request_type, user_agent, data, 500)
        return jsonify({'error': str(e)}), 500

@app.route('/api/hits', methods=['GET'])
def get_hits():
    hits = ApiHit.query.all()
    log_audit('GET_ALL', '/api/hits', 'GET', request.headers.get('User-Agent'), None, 200)
    return jsonify([hit.as_dict() for hit in hits])

@app.route('/api/hits/<int:id>', methods=['GET'])
def get_hit(id):
    hit = ApiHit.query.get(id)
    if not hit:
        log_audit('GET_SINGLE', f'/api/hits/{id}', 'GET', request.headers.get('User-Agent'), None, 404)
        return jsonify({'error': 'Hit not found'}), 404
    log_audit('GET_SINGLE', f'/api/hits/{id}', 'GET', request.headers.get('User-Agent'), None, 200)
    return jsonify(hit.as_dict())

@app.route('/api/hits/<int:id>', methods=['PUT'])
def update_hit(id):
    hit = ApiHit.query.get(id)
    if not hit:
        log_audit('UPDATE', f'/api/hits/{id}', 'PUT', request.headers.get('User-Agent'), request.json, 404)
        return jsonify({'error': 'Hit not found'}), 404
    data = request.get_json(silent=True)
    hit.request_type = request.method
    hit.endpoint = data.get('endpoint')
    hit.user_agent = request.headers.get('User-Agent')
    hit.request_body = data.get('request_body', None)
    try:
        db.session.commit()
        log_audit('UPDATE', f'/api/hits/{id}', 'PUT', request.headers.get('User-Agent'), data, 200)
        return jsonify(hit.as_dict())
    except Exception as e:
        db.session.rollback()
        log_audit('UPDATE', f'/api/hits/{id}', 'PUT', request.headers.get('User-Agent'), data, 500)
        return jsonify({'error': str(e)}), 500

@app.route('/api/hits/<int:id>', methods=['DELETE'])
def delete_hit(id):
    hit = ApiHit.query.get(id)
    if not hit:
        log_audit('DELETE', f'/api/hits/{id}', 'DELETE', request.headers.get('User-Agent'), None, 404)
        return jsonify({'error': 'Hit not found'}), 404
    try:
        db.session.delete(hit)
        db.session.commit()
        log_audit('DELETE', f'/api/hits/{id}', 'DELETE', request.headers.get('User-Agent'), None, 204)
        return '', 204
    except Exception as e:
        db.session.rollback()
        log_audit('DELETE', f'/api/hits/{id}', 'DELETE', request.headers.get('User-Agent'), None, 500)
        return jsonify({'error': str(e)}), 500

@app.route('/api/audit_logs', methods=['GET'])
def get_audit_logs():
    logs = ApiLog.query.all()
    return jsonify([log.as_dict() for log in logs])

# Run the application
if __name__ == '__main__':
    app.run(debug=True)