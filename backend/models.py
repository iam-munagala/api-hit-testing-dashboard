from database import db
from datetime import datetime

class ApiHit(db.Model):
    __tablename__ = 'api_hits'
    
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(10), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    request_body = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'request_type': self.request_type,
            'endpoint': self.endpoint,
            'user_agent': self.user_agent,
            'request_body': self.request_body,
            'timestamp': self.timestamp.isoformat()
        }

class ApiLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(10), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
    request_type = db.Column(db.String(10), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    request_body = db.Column(db.Text, nullable=True)
    response_status = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'operation': self.operation,
            'endpoint': self.endpoint,
            'request_type': self.request_type,
            'user_agent': self.user_agent,
            'request_body': self.request_body,
            'response_status': self.response_status,
            'timestamp': self.timestamp.isoformat()
        }