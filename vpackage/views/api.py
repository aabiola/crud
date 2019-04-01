# pylint: disable-msg=C0103
from vpackage import app
from flask import Flask, render_template, request, url_for, abort, redirect,make_response,json, jsonify

from vpackage import db, csrf

from vpackage.model import Product, Category, Message, Customer, Admin, Hostel, Allstates, User

from sqlalchemy import or_
from sqlalchemy import desc

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/hostel/api/v1.0/list', methods=['GET'])
#@auth.login_required
def hostel_list():
    deets = db.session.query(Hostel, Allstates).join(Allstates).filter(Hostel.hostel_state == Allstates.id).all()
    mydict = {}
    if deets:
        for deet in deets:
           
            mydict[deet.Hostel.id] = {
                'name': deet.Hostel.hostel_name,
                'desc': deet.Hostel.hostel_desc,
                'state':deet.Allstates.state_name
            }
        return jsonify(mydict)
    else:
        return 0
    #return render_template('test2.html', deets = mydict)


@app.route('/hostel/api/v1.0/list/<int:hostel_id>', methods=['GET'])
@auth.login_required
def get_hostel(hostel_id):

    deet = db.session.query(Hostel, Allstates).join(Allstates).filter(Hostel.id ==hostel_id).first()
    #json.dumps(deet)
    if deet == None:
        abort(404)
    else:
        mydict = {
                'name': deet.Hostel.hostel_name,
                'desc': deet.Hostel.hostel_desc,
                'state':deet.Allstates.state_name
        }
    return jsonify(mydict)

@csrf.exempt
@app.route('/hostel/api/v1.0/hostel', methods=['POST'])
def add_hostel():
    dict_body = request.get_json() # receive the value as json
    if dict_body is None or 'hostelname' not in dict_body:
        abort(400)
    else:
        #retrieve each value and insert into database
        hostel = Hostel(hostel_name=dict_body['hostelname'],hostel_state=dict_body['hostelstate'],hostel_desc=dict_body['description'])
        db.session.add(hostel)
        db.session.commit()
        return jsonify({'message': 'New hostel successfully created.'}), 200
        #return jsonify(dict_body) #render_template('test2.html', newhostel=dict_body)
   
@csrf.exempt
@app.route('/hostel/api/v1.0/update/<int:hostel_id>', methods=['PUT'])
def update_hostel(hostel_id):
    deets = db.session.query(Hostel).get(hostel_id)
    if deets is not None:
        #retrieve from json request object

        data = request.get_json() 
        hostelname = data['hostelname']
        hostelstate = data['hostelstate']
        description = data['description']

        #update table by setting attributes of obj to new value
        deets.hostel_name = hostelname
        deets.hostel_desc = description
        deets.hostel_state = hostelstate       
        db.session.commit()
        return jsonify({"message":"Update was successful"})
    else:
        return jsonify({"message":"Invalid Data Supplied"})

@auth.get_password
def get_password(username):
    deets = db.session.query(User.password).filter(User.username==username).first()
    if deets:
        return deets.password
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@csrf.exempt
@app.route('/hostel/api/v1.0/delete/<int:hostel_id>', methods=['DELETE'])
def delete_hostel(hostel_id):
    deets = db.session.query(Hostel).get(hostel_id)
    if deets is not None:
        db.session.delete(deets)
        db.session.commit()
        return jsonify({"message":"Hostel Deleted!"})
    else:
        return jsonify({"message":"Invalid Data Supplied"})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)