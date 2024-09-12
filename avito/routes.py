from flask import request, jsonify, Blueprint, make_response
from sqlalchemy.testing.pickleable import User

from .models import *

main = Blueprint('main', __name__)


@main.route('/api/ping', methods=['GET'])
def ping():
    return make_response('OK', 200)


# @main.route('/api/employee/new', methods=['POST'])
# def new_user():
#     user = Employee(
#         username=request.json['username'],
#         first_name=request.json['first_name'],
#         last_name=request.json['last_name'],
#     )
#     db.session.add(user)
#     db.session.commit()
#     return make_response(jsonify(user.to_dict()), 200)
#
#
# @main.route('/api/employee/list', methods=['GET'])
# def list_employees():
#     employees = Employee.query.all()
#     return make_response(jsonify([employee.to_dict() for employee in employees]), 200)
#
#
# @main.route('/api/organisation/new', methods=['POST'])
# def new_organisation():
#     organisation = Organisation(
#         name=request.json['name'],
#         description=request.json['description'],
#         type=request.json['type']
#     )
#     db.session.add(organisation)
#     db.session.commit()
#     return make_response(jsonify(organisation.to_dict()), 200)
#
#
# @main.route('/api/organisationresponsible/add', methods=['POST'])
# def new_organisation_responsible():
#     organisation = Organisation.query.filter_by(name=request.json['organisation']).first()
#     employee = Employee.query.filter_by(username=request.json['employee']).first()
#     organisation_responsible = OrganisationResponsible(
#         organisation_id=organisation.id,
#         user_id=employee.id
#     )
#     db.session.add(organisation_responsible)
#     db.session.commit()
#     return make_response(jsonify(organisation_responsible.to_dict()), 200)


"""
Tender related endpoints
"""


@main.route('/api/tenders', methods=['GET'])
def get_tenders():
    tenders = Tender.query.filter_by(tender_status='Published').all()
    return make_response(jsonify([tender.to_dict() for tender in tenders]), 200)


@main.route('/api/tenders/my', methods=['GET'])
def get_my_tenders():
    username = request.args.get('username')
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    if limit is None:
        limit = 5
    if offset is None:
        offset = 0
    try:
        if limit is not None:
            limit = int(limit)
        if offset is not None:
            offset = int(offset)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    tenders = Tender.query.filter_by(creator_username=username).all()[offset:limit]
    return make_response(jsonify([tender.to_dict() for tender in tenders]), 200)


@main.route('/api/tenders/new', methods=['POST'])
def create_tender():
    tender = Tender(
        name=request.json['name'],
        description=request.json['description'],
        service_type=request.json['service_type'],
        tender_status=request.json['status'],
        organisation_name=request.json['organisation_name'],
        creator_username=request.json['username']
    )
    db.session.add(tender)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)
    return make_response(jsonify(tender.to_dict()), 200)


@main.route('/api/tenders/<int:tender_id>/edit', methods=['PATCH'])
def edit_tender(tender_id):
    required_params = ['username']

    for param in required_params:
        if request.args.get(param) is None:
            return make_response(jsonify({f'Error! Отсутствует обязательный параметр': {param}}), 400)

    tender = Tender.query.get(tender_id)
    # organisation = Organisation.query.filter_by(name=tender.organisation_name).first()
    employee = Employee.query.filter_by(username=request.json['username']).first()
    if OrganisationResponsible.query.filter_by(organisation_id=tender_id).filter_by(user_id=employee.id).get() is None:
        return make_response('Error', 403)
    # if tender.creator_username != username:
    #     return make_response(jsonify({'error': 'You do not have permission to edit this tender'}), 403)

    tender.name = request.json['name']
    tender.description = request.json['description']
    tender.service_type = request.json['service_type']
    tender.version += 1
    db.session.commit()
    return make_response(jsonify(tender.to_dict()), 200)


@main.route('/api/tenders/<string:tender_id>/status', methods=['GET'])
def get_tender_status(tender_id):
    username = request.args.get('username')
    if username is not None:
        if username not in Employee.query.all():
            return make_response(jsonify({'error': 'There is no such user'}), 403)
    tender = Tender.query.get(tender_id)
    employee = Employee.query.filter_by(username=username).first()
    if tender.tender_status == 'Created' or tender.tender_status == 'Closed':
        if OrganisationResponsible.query.filter_by(organisation_id=tender_id).filter_by(
                user_id=employee.id).get() is None:
            return make_response(jsonify({'error': 'You don\'t have permission'}), 403)
    return make_response(jsonify(tender.tender_status.value), 200)


@main.route('/api/tenders/<string:tender_id>/status', methods=['PUT'])
def update_tender_status(tender_id):
    required_params = ['username', 'status']
    for param in required_params:
        if request.json[param] is None:
            return make_response(jsonify({f'Error! Отсутствует обязательный параметр': {param}}), 400)

    username = request.json['username']
    status = request.json['status']
    tender = Tender.query.get(tender_id)
    employee = Employee.query.filter_by(username=username).first()
    if tender.tender_status == 'Created' or tender.tender_status == 'Closed':
        if OrganisationResponsible.query.filter_by(organisation_id=tender_id).filter_by(
                user_id=employee.id).get() is None:
            return make_response(jsonify({'error': 'You don\'t have permission'}), 403)
    tender.tender_status = status
    db.session.commit()
    return make_response(jsonify(tender.to_dict()), 200)


"""
Bid related endpoints
"""


@main.route('/api/bids/new', methods=['POST'])
def create_bid():
    try:
        bid = Bid(
            name=request.json['name'],
            description=request.json['description'],
            status=request.json['status'],
            tender_id=request.json['tender_id'],
            organisation_name=request.json['organisation_name'],
            author_username=request.json['username']
        )
    except Exception as ex:
        return make_response(jsonify({'error': str(ex)}), 400)
    db.session.add(bid)
    db.session.commit()
    return make_response(jsonify(bid.to_dict()), 200)


@main.route('/api/bids/my', methods=['GET'])
def get_bids():
    username = request.args.get('username')
    if username is None:
        return make_response(jsonify({'Error': 'No requiring param'}), 403)
    if username not in Employee.query.all():
        return make_response(jsonify({'Error': 'There is no such user'}), 403)
    bids = Bid.query.filter_by(author_username=username).all()
    return make_response(jsonify({'bids': [bid.to_dict for bid in bids]}), 200)


@main.route('/api/bids/<string:tender_id>/list', methods=['GET'])
def get_bids_list(tender_id):
    username = request.args.get('username')
    if username is None:
        return make_response(jsonify({'Error': 'No requiring param'}), 403)
    if username not in Employee.query.all():
        return make_response(jsonify({'Error': 'There is no such user'}), 403)
    tender = Tender.query.get(tender_id)
    if tender is None:
        return make_response(jsonify({'Error': 'No such tender'}), 403)
    bids = Bid.query.filter_by(status=BidStatus.Published).filter_by(tender_id=tender_id).all()
    return make_response(jsonify([bid.to_dict() for bid in bids]), 200)


@main.route('/api/bids/<string:bid_id>/edit', methods=['PATCH'])
def update_bid(bid_id):
    required_params = ['name', 'description']
    username = request.json['username']
    if username is None:
        return make_response(jsonify({'Error': 'You don\'t have permission'}), 403)
    for param in required_params:
        if request.json[param] is None:
            return make_response(jsonify({'Error': 'No requiring param'}), 400)
    bid = Bid.query.get(bid_id)
    if bid is None:
        return make_response(jsonify({'Error': 'No such bid'}), 403)
    org = Organisation.query.filter_by(name=bid.organisation_name).first()
    employee = Employee.query.filter_by(username=username).first()
    if OrganisationResponsible.query.filter_by(organisation_id=org.id).filter_by(user_id=employee.id).get() is None:
        return make_response(jsonify({'error': 'You don\'t have permission'}), 403)
    bid.name = request.json['name']
    bid.description = request.json['description']
    db.session.commit()
    return make_response(jsonify(bid.to_dict()), 200)


@main.route('/api/bids/<string:bid_id>/status', methods=['GET'])
def get_bids_status(bid_id):
    username = request.json['username']
    if username is None:
        return make_response(jsonify({'Error': 'No requiring param'}), 403)
    bid = Bid.query.get(bid_id)
    if bid is None:
        return make_response(jsonify({'Error': 'No such bid'}), 403)
    # if bid.status != BidStatus.Published:
    #     return make_response(jsonify({'Error': 'You don\'t have permission'}), 403)
    org = Organisation.query.filter_by(name=bid.organisation_name).first()
    employee = Employee.query.filter_by(username=username).first()
    if OrganisationResponsible.query.filter_by(organisation_id=org.id).filter_by(user_id=employee.id).get() is None:
        return make_response(jsonify({'error': 'You don\'t have permission'}), 403)
    return make_response(jsonify(bid.status), 200)


@main.route('/api/bids/<string:bid_id>/status', methods=['PUT'])
def update_bid_status(bid_id):
    username = request.args.get('username')
    status = request.args.get('status')
    if username is None:
        return make_response(jsonify({'Error': 'No requiring param'}), 403)
    bid = Bid.query.get(bid_id)
    if bid is None:
        return make_response(jsonify({'Error': 'No such bid'}), 403)
    org = Organisation.query.filter_by(name=bid.organisation_name).first()
    employee = Employee.query.filter_by(username=username).first()
    if OrganisationResponsible.query.filter_by(organisation_id=org.id).filter_by(user_id=employee.id).get() is None:
        return make_response(jsonify({'error': 'You don\'t have permission'}), 403)
    bid.status = status
    db.session.commit()
    return make_response(jsonify(bid.to_dict()), 200)
