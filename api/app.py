from flask import Flask, request, jsonify, make_response
from bson.objectid import ObjectId
from db import db
import config
import jwt
import hashlib

app = Flask(__name__)

# TODO : All requests inputs are going to validate

# Public main route
@app.route('/', methods=['GET'])
def index():
	return 'welcome to mizrapp'

@app.route('/login', methods=['POST'])
def login():
	# Convert request to json format
	json = request.get_json()

	# Get user from db
	user = db.users.find_one({'email' :	json.get('email')})

	if user:
		# Check password
		if user['password'] == hashlib.sha256(json.get('password').encode('utf-8')).hexdigest():

			user['_id'] = str(user['_id'])

			token = {
				"_id" : user['_id']
			}

			# Generate token
			user['token'] = jwt.encode(token, config.jwt_secret, algorithm='HS256').decode("utf-8")
			return jsonify(user)
		else :
			return jsonify({'message' : 'Wrong password'}), 400
	else :
		return jsonify({'message' : 'User not found'}), 404


@app.route('/register', methods=['POST'])
def register():
	# Convert request to json format
	json = request.get_json()

	# Get user from db
	user = db.users.find_one({'email' : json.get('email')})

	if user:
		return jsonify({'message' : 'Email exists'}), 409

	# Hash password
	password = hashlib.sha256(json.get('password').encode('utf-8')).hexdigest()

	user = {
		'name' : json.get('name'),
		'email' : json.get('email'),
		'password' : password
	}

	# Save user
	userId = db.users.insert(user)

	token = {
		'_id' : str(userId)
	}

	user['_id'] = str(userId)
	del user['password']

	# Generate token
	user['token'] = jwt.encode(token, config.jwt_secret, algorithm='HS256').decode("utf-8")

	return jsonify(user)


@app.route('/api/user/info', methods=['POST'])
def api():

		json = request.get_json()

		info = {
				"user" : ObjectId(json.get('user')),
				"age" : json.get('age'),
				"profession" : json.get('profession'),
				"gender" : json.get('gender'),
				"city" : json.get('city'),
		}

		infoId = db.user_info.insert(info)
		info['_id'] = str(infoId)
		info['user'] = json.get('user')
		return jsonify(info)

@app.route('/api/users/<string:userId>', methods=['GET'])
def getUser(userId):

	# Fetch all categories in db as list
	categories = list(db.categories.find({}))

	# Get all subCategory id of all categories
	subCategoryIds = []
	for category in categories:
		category['_id'] = str(category['_id'])
		subCategoryIds += category['subCategories']

	# Fetch all subCategories as list
	subCategories = list(db.subCategories.find({"_id" : {"$in" : subCategoryIds}}))

	# Match categories with their subCategories
	for category in categories:
		listOfSubCategories = []
		for subCategory in subCategories:
			if subCategory['_id'] in category['subCategories']:
				subCategory['_id'] = str(subCategory['_id'])
				listOfSubCategories.append(subCategory)

		# Assign matched subCategories list to category
		category['subCategories'] = listOfSubCategories

	# Fetch all reviews belong to user
	reviews = list(db.reviews.find({'user' : ObjectId(userId)}))

	# Convert objectId to string
	for review in reviews:
		review['_id'] = str(review['_id'])

	# Return response data
	response = {
		'categories' : categories,
		'reviews' : reviews
	}

	return jsonify(response)


@app.route('/api/products/<string:subCategoryId>', methods=['GET'])
def getProducts(subCategoryId):

	# Fetch products
	products = list(db.products.find({'subCategory' : ObjectId(subCategoryId)}))

	# Store companyIds and subCategoryIds
	companyIds = []
	subCategoryIds = []
	for product in products:
		companyIds.append(product['company'])
		subCategoryIds.append(product['subCategory'])

	# Fetch all company and subcategory details with ids
	companies = list(db.companies.find({'_id' : {'$in':companyIds}}))
	subCategories = list(db.subCategories.find({'_id' : {'$in' : subCategoryIds}}))

	# Map product with company and subcategory details
	for product in products:

		product['_id'] = str(product['_id'])

		for company in companies:
			if str(company['_id']) == str(product['company']):
				company['_id'] = str(company['_id'])
				product['company'] = company

		for subCategory in subCategories:
			if str(subCategory['_id']) == str(product['subCategory']):
				subCategory['_id'] = str(subCategory['_id'])
				product['subCategory'] = subCategory

	response = {
		'products' : products
	}

	return jsonify(response)

@app.route('/api/products/review', methods=['POST'])
def review():
	json = request.get_json()

	review= {
		"product" : ObjectId(json.get('product')),
		"isUsed" : json.get('isUsed'),
		"rank" : json.get('rank'),
		"offer" : json.get('offer'),
		"user" : ObjectId(json.get('user')),
	}

	db.reviews.insert(review)

@app.route('/api/images/<string:image>')
def getImage(image):
	fullpath = "./images/" + image

	with open(fullpath, 'rb') as f:
		contents = f.read()

	response = make_response(contents)
	response.content_type = "image/jpeg"

	response.headers.set('Content-Type', 'image/jpeg')
	response.headers.set(
			'Content-Disposition', 'attachment', filename='%s' % image)
	return response

@app.before_request
def check_auth_token():
	# Dont check token for login and register endpoints
	if request.path not in ('/login', '/register', '/'):
			return

	# Get token from request header
	token = request.headers.get('AUTHORIZATION')
	if token is None:
		return jsonify({'message' : 'Invalid Token'})

	token = token.encode('utf-8')

	# Decode and verify token
	try:
		user = jwt.decode(token.decode('utf-8'), config.jwt_secret, algorithms=['HS256'])
		if user:
			return
		else:
			return jsonify({'message' : 'Invalid Token'})
	except:
		return jsonify({'message' : 'Invalid Token'})


if __name__ == '__main__':
	# host : localhost
	# port : 5000 (default)
	app.run(debug=True)