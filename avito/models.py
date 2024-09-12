from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import uuid

db = SQLAlchemy()


class OrganisationType(Enum):
    IE = 'IE'
    LLC = 'LLC'
    JSC = 'JSC'


class ServiceType(Enum):
    Construction = 'Construction'
    Delivery = 'Delivery'
    Manufacture = 'Manufacture'


class TenderStatus(Enum):
    Created = 'Created'
    Published = 'Published'
    Closed = 'Closed'


class BidStatus(Enum):
    Created = 'Created'
    Published = 'Published'
    Canceled = 'Canceled'
    Approved = 'Approved'
    Rejected = 'Rejected'


class AuthorType(Enum):
    User = 'User'
    Organisation = 'Organisation'


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Organisation(db.Model):
    __tablename__ = 'organisation'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    type = db.Column(db.Enum(OrganisationType), name='organisation_type')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class OrganisationResponsible(db.Model):
    __tablename__ = 'organisation_responsible'

    id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('organisation.id'), nullable=False)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('employee.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'organisation_id': self.organisation_id,
            'user_id': self.user_id
        }


"""
Tender related models
"""


class Tender(db.Model):
    __tablename__ = 'tender'

    id = db.Column(db.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    service_type = db.Column(db.Enum(ServiceType), nullable=False, name='service_type')
    tender_status = db.Column(db.Enum(TenderStatus), nullable=False, name='tender_status')
    organisation_name = db.Column(db.String(100), db.ForeignKey('organisation.name'), nullable=False)
    version = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    creator_username = db.Column(db.String(50), db.ForeignKey('employee.username'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'service_type': self.service_type.value,
            'tender_status': self.tender_status.value,
            'organisation_name': self.organisation_name,
            'version': self.version,
            'created_at': self.created_at,
            'creator_username': self.creator_username
        }

    def __repr__(self):
        return (f'<Tender id:{self.id},\nname:{self.name},\ndescription:{self.description},'
                f'\norganisation_name:{self.organisation_name},\nversion:{self.version}>')


"""
Bid related models
"""


class Bid(db.Model):
    __tablename__ = 'bid'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.Enum(BidStatus), nullable=False, name='bid_status')
    tender_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('tender.id'), nullable=False)
    author_type = db.Column(db.Enum(AuthorType), nullable=False, name='author_type')
    organisation_name = db.Column(db.String(100), db.ForeignKey('organisation.name'), nullable=False)
    author_username = db.Column(db.String(50), db.ForeignKey('employee.username'), nullable=False)
    version = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'tender_id': self.tender_id,
            'author_type': self.author_type.value,
            'author_username': self.author_username,
            'organisation_name': self.organisation_name,
            'version': self.version,
            'created_at': self.created_at
        }
