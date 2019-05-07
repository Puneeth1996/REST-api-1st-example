import pymongo
# the above module is being put just for understanding from the w3chools page basics
from flask import Flask,jsonify,request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'wedeeye'
app.config['MONGO_URI'] = "mongodb+srv://test:test@wideeye-3ku58.mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)
print("connected i guess")
user = mongo.db.users



# make sure this below route was used just on start test process
# @app.route('/add')
# def add():
# 	user.insert({'name':'puneeth'})
# 	return "added user!"

@app.route('/add_plans')
def all_plans():
	user.insert({"id" : "1", "name" : "Plan1", "price" : { "amount" : 10, "currency" : "kwd" }, "features" : [ { "id" : "1.1", "name" : "Calls", "limit" : { "amount" : 100, "unit" : "Minutes", "Balance" : 100, "extraCharge" : { "amount" : "0.100", "currency" : "kwd", "unit" : "minute" } } }, { "id" : "1.2", "name" : "SMS", "limit" : { "amount" : 250, "unit" : "Messages", "Balance" : 250, "extraCharge" : { "amount" : "0.025", "currency" : "kwd", "unit" : "message" } } } ] })
	user.insert({"id" : "2", "name" : "Plan2", "price" : { "amount" : 25, "currency" : "kwd" }, "features" : [ { "id" : "2.1", "name" : "Calls", "limit" : { "amount" : 500, "unit" : "Minutes", "Balance" : 500, "extraCharge" : { "amount" : "0.200", "currency" : "kwd", "unit" : "minute" } } }, { "id" : "2.2", "name" : "SMS", "limit" : { "amount" : 500, "unit" : "Messages", "Balance" : 500, "extraCharge" : { "amount" : "0.05", "currency" : "kwd", "unit" : "message" } } } ] })
	user.insert({"id" : "3", "name" : "Plan3", "price" : { "amount" : 25, "currency" : "kwd" }, "features" : [ { "id" : "2.1", "name" : "Calls", "limit" : { "amount" : 500, "unit" : "Minutes", "Balance" : 500, "extraCharge" : { "amount" : "0.200", "currency" : "kwd", "unit" : "minute" } } }, { "id" : "2.2", "name" : "SMS", "limit" : { "amount" : 500, "unit" : "Messages", "Balance" : 500, "extraCharge" : { "amount" : "0.05", "currency" : "kwd", "unit" : "message" } } } ] })
	return "added 3 intial plans!"


@app.route('/plan', methods=['GET'])
def base_plans():
	output = []
	output1 = []
	for val in user.find():
		print(val)
		output.append({'Plan': val['name']})
		print(output)
		for n in val["price"]:
			# print(n)
			# print(val["price"][n])
			output1.append({'Amount':val["price"][n]})
			print(output1)
		output.append(output1)		
	return jsonify({'result' : output})


@app.route('/plan/<path:filename>')
def particular_plan(filename):
	search = filename
	print(search)
	out = []
	out1 = []
	s = user.find_one({'name' : search})
	print(s)
	if s:
		out = {'Plan' : s['name']}
		print(out)
		for n in s["price"]:
			# print(s["price"][n])
			out1.append({'Amount':s["price"][n]})
		print(out1)
	return jsonify({'result' : [out,out1]})	



@app.route('/add_one_plan', methods=['POST'])
def add_one():
	star = user
	print(star)
	print(70*'=')
	name = request.json['name']
	print(name)
	star_id = star.insert({'name': name})
	new_star = star.find_one({'_id': star_id })
	output = {'name' : new_star['name']}
	return jsonify({'result' : output})


if __name__ == '__main__':
	app.run(debug=True)





# print(50*'=')
# myclient = pymongo.MongoClient("mongodb+srv://test:test@wideeye-3ku58.mongodb.net/test?retryWrites=true")
# print(myclient)
# dblist = myclient.list_database_names()
# print(dblist)
# mydb = myclient["wedeeye"]
# collist = mydb.list_collection_names()
# print(collist)
# mycol = mydb["plans"]
# x = mycol.find_one()
# print(x)

# @app.route('/', methods=['GET'])
# def entry_plans():
# 	return jsonify('All plans')



