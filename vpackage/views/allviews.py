# pylint: disable-msg=C0103
from vpackage import app
from flask import render_template, request, url_for,abort, flash, redirect,make_response,session, json,send_from_directory
from vpackage.forms import ContactForm, UploadForm, SignupForm, LoginForm
from vpackage import db, csrf
from werkzeug import secure_filename

from vpackage.model import Product, Category, Message, Customer, Admin

from vpackage import mail, Message
from flask import jsonify
from sqlalchemy import or_
from sqlalchemy import desc

from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/payment')
def makepayment():
    return render_template('paystack.html')

@app.route('/testdelete')
def testdelete():
    x = db.session.query(Category).get(2)
    db.session.delete(x)
    db.session.commit()
    return 'yes'

@app.route('/prod')
def prod():
    deetsx = db.session.query(Category.category_name, Category.id,Product).outerjoin(Product).order_by(desc(Category.id))
    deets = db.session.query(Category, Product).outerjoin(Product).order_by(desc(Category.id)).all()
    
    
    # deetsx = db.session.query(Category, Product, Product.prod_id==Category.id)
    # deets =db.session.query(Category,Product, Product.prod_id==Category.id).all()
    

    #query.join(Invoice, id == Address.custid)
    #products = deets.products

    return render_template('test.html', deets=deets,gg=deetsx)

@app.route('/checkuser', methods=['POST','GET'])
def checkuser():
    
    form = LoginForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        deets = db.session.query(Admin).filter(Admin.admin_email == email).first()
        
        
        if deets and check_password_hash(deets.admin_pass, password):           
            return 'Logged in successful'
        else:
            return email + password + 'wrong'
    else:
        return render_template('loginform.html', form=form)

@app.route('/hostels')
def gethostel():
    import requests, json
    from flask import jsonify
    
    # headers = {
    # 'Content-Type': 'application/json',
    # }

    response = requests.get('http://127.0.0.1:5000/hostel/api/v1.0/list')
    #response = requests.get('http://127.0.0.1:5000/hostel/api/v1.0/list', headers=headers)
    res = json.loads(response.text) #res is a dict object
    return jsonify(res)

@app.route('/signup')
def adminsignup():
    form = SignupForm()
    return render_template('signup.html', form=form)

@app.route('/login', methods=['POST'])
def login():
    admin_name = request.form['name']
    admin_email = request.form['email']
    admintype = request.form['usertype']
    adminpass = request.form['password']
    formated = generate_password_hash(adminpass)

    user = Admin(admin_name=admin_name,admin_email=admin_email,admin_user=admintype, admin_pass=formated)
    db.session.add(user)
    db.session.commit()

    if user.id:
        flash('Successfully registered')
    else:
        flash('Error Occured, you were not registered')
    return redirect('/signup')

#from flask_mail import Message
@app.route('/')
def userlogin():
    # msg = Message("Subject", recipients=["abiolailupeju@gmail.com","oyebolailupeju@gmail.com"])
    # msg.html = "<h2>Email Heading</h2>\n<p>Email Body</p>"
    # with app.open_resource("image_list.jpg") as fp:
    #     msg.attach("image_list.jpg", "image/jpg", fp.read())
    # mail.send(msg)

    cust = Customer(cust_name='Adebisi Alao',cust_email='bisi@y.com',cust_phone='09056362666')
    prod = Product(product_name='Tea',product_price='50000', product_category=1)
    db.session.add(cust)
    db.session.add(prod)
    db.session.commit()
    return 'This route sends out mail but the mail sending functionality has been commented out..'



@app.route('/welcome')
def welcome():
    form = ContactForm()
    return render_template('login.html', form=form)  # render a template

@app.route('/contact')
def contactus():
    title = request.args.get('key')
    return render_template('contact.html',title=title)  # render a template


@app.route('/test/', methods=['POST', 'GET'])
#@csrf.exempt
def test():
    from flask import jsonify
    # name =  request.form['name']
    # email =  request.form['email']
    # message = request.form['message']
    name = request.args.get('name','abi')
    #return json.dumps({'status':'OK','user':name,'email':email});
    #return json.jsonify(1,2,3,4,5)
    return name

@app.route('/search/<searchword>')
def searchlist(searchword):
    from flask import jsonify
    deets = db.session.query(Customer).filter(Customer.cust_name.ilike('%Abiol%')).all()
    st = ""
    for i in deets:
        st = st + "<option value='"+ i.cust_name +"'"+'>'
    return jsonify(st)

# @app.after_request
# def after_request(response):
#     if str(request.path).startswith('/download/'):
#         response.headers['Content-Disposition'] = 'attachment'
#         return response

@app.route('/download/myfile')
def myfile():
    return send_from_directory('uploads',filename='web-application-creation-process.png')

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

@app.route('/fileupload', methods=['POST', 'GET'])
def fileupload():
    form = UploadForm()

    if request.method == 'POST' and form.validate_on_submit():
        file_filenames = []
        for i in request.files['files']:
            file_filenames.append(i)

        gifts = request.form.getlist('gifts')
        f = request.files['upload']
        fullpath = app.config['UPLOAD_FOLDER']+ secure_filename(f.filename)
        f.save(fullpath)
        return file_filenames[1]
    else:
        return render_template('uplo.html', form=form)

