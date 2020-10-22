from flask import Flask, url_for,session,make_response,render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from functools import wraps
from pymongo import MongoClient
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key="secretkey"
app.config['MONGO_URI']="mongodb+srv://Nemo:1234567a@finalproject.8jxp2.mongodb.net/Store?retryWrites=true&w=majority"
mongo = PyMongo(app)

#adds an ADMIN
@app.route('/ADMIN/add',methods=['POST'])
def add_ADMIN():
    _json=request.json
    _username=_json['username']
    _password=_json['password']
    if _username and _password and request.method=='POST':
        _hashed_password=generate_password_hash(_password)
        id = mongo.db.ADMIN.insert({'username':_username,'password':_hashed_password})
        resp=jsonify("ADMIN added successfully")
        resp.status_code=200
        return resp
    else:
        return not_found()
#ADMIN login
@app.route('/ADMIN/login',methods=['POST'])
def ADMIN_login():
    _json=request.json
    _username=_json['username']
    _password=_json['password']
    check_password=mongo.db.ADMIN.find_one({'username':_username},{"password":1})
    if mongo.db.ADMIN.count_documents({'username':_username},limit=1)!=0 and check_password_hash(check_password["password"],_password) and request.method=='POST':
        return jsonify("ADMIN Authenticated")
    else:
        return jsonify("ADMIN Not Authenticated")
#User login
@app.route('/Users/login',methods=['POST'])
def Users_login():
    _json=request.json
    _username=_json['username']
    _password=_json['password']
    check_password=mongo.db.Users.find_one({'username':_username},{"password":1})
    if mongo.db.Users.count_documents({'username':_username},limit=1)!=0 and check_password_hash(check_password["password"],_password) and request.method=='POST':
        return jsonify("User Authenticated")
    else:
        return jsonify("User Not Authenticated")
#adds a user
@app.route('/Users/add',methods=['POST'])
def add_Users():
    _json=request.json
    _username=_json['username']
    _password=_json['password']

    if _username and _password and request.method=='POST':
        _hashed_password=generate_password_hash(_password)
        id = mongo.db.Users.insert({'username':_username,'password':_hashed_password})
        resp=jsonify("User added successfully")
        resp.status_code=200
        return resp
    else:
        return not_found()
#show all users
@app.route('/Users')
def Users():
    Users = mongo.db.Users.find()
    resp = dumps(Users)
    return resp
#find one user
@app.route('/Users/<id>')
def User(id):
    Users = mongo.db.Users.find_one({'_id':ObjectId(id)})
    resp=dumps(Users)
    return resp
#delete a user
@app.route('/Users/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.Users.delete_one({'_id':ObjectId(id)})
    resp=jsonify("User deleted successfully")
    resp.status_code=200
    return resp
#update a user
@app.route('/Users/update/<id>',methods=['PUT'])
def update_user(id):
    _id=id
    _json=request.json
    _username=_json['username']
    _password=_json['password']
    if _username and _password and _id and request.method=='PUT':
        _hashed_password=generate_password_hash(_password)
        mongo.db.Users.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'username':_username,'password':_hashed_password}})
        resp = jsonify("User updated successfuly")
        resp.status_code=200
        return resp
    else:
        return not_found()

#ITEMS
#adds an item
@app.route('/Items/add',methods=['POST'])
def add_Items():
    _json=request.json
    _name=_json['Item_Name']
    _price=_json['Price']
    _description=_json['Description']
    if _name and _price and _description and request.method=='POST':
        id = mongo.db.Items.insert({'Item_Name':_name,'Price':_price,'Description':_description})
        resp=jsonify("Item added successfully")
        resp.status_code=200
        return resp
    else:
        return not_found()
#deletes an item
@app.route('/Items/delete/<id>',methods=['DELETE'])
def delete_Items(id):
    mongo.db.Items.delete_one({'_id':ObjectId(id)})
    resp=jsonify("Item deleted successfully")
    resp.status_code=200
    return resp
#show all Items
@app.route('/Items')
def Items():
    Items = mongo.db.Items.find()
    resp = dumps(Items)
    return resp
#updates an Item
@app.route('/Items/update/<id>',methods=['PUT'])
def update_Item(id):
    _id=id
    _json=request.json
    _name=_json['Item_Name']
    _price=_json['Price']
    _description=_json['Description']
    if _name and _price and _description and request.method=='PUT':
        mongo.db.Items.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'Item_Name':_name,'Price':_price,'Description':_description}})
        resp = jsonify("Item updated successfuly")
        resp.status_code=200
        return resp
    else:
        return not_found()


#error message
@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message':'Not Found'+request.url
    }
    resp.status_code=404
    return resp

if __name__=='__main__':
    app.run(debug=True)


'''
def check_for_token(func):
    @wraps(func)
    def wrapped(*args,**kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}),403
        try: 
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except: 
            return jsonify({'message':'Invalid Token'}),403
        return func(*args,**kwargs)
    return wrapped
@app.route('/auth')
@check_for_token
def authorized():
    return 'This is only viewable with a token'
@app.route('/login',methods=['POST'])
def login():
    if request.form['username'] and request.form['password']=='password':
        session['logged_in']=True
        token =jwt.encode({
            'User':request.form['username'],
            'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=300)
        },app.config['SECRET_KEY'])
        return jsonify({'token':token.decode(utf-8)})
    else:
        return make_response('Unable to verify',403,{'WWW-Authenticate':'Basic realm:"login'})
'''