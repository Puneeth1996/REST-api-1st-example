from flask import Flask,jsonify,request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'wedeeye'
app.config['MONGO_URI'] = "mongodb+srv://test:test@wideeye-3ku58.mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)
print("connected i guess")
user = mongo.db.users

#This below function create the home route that shows out all the database plans existing.
@app.route('/', methods=['GET'])
def all_plans():
	output = []
	for val in user.find():
		output.append({'its id': val['id']})
		output.append({'Plan-Name': val['name']})
		for n in val['price']:
			if(n == 'amount'):
				output.append({'Amount':val['price'][n]})
			
			elif(n == 'currency'):
				output.append({'Currency':val['price'][n]})
		
		for m in val['features']:
			output.append({'Feature': m['name']})
			for lim in m['limit']:				
				if(lim == 'unit'):
					output.append({'Unit':m['limit']['unit']})					
				elif(lim == 'Balance'):
					bal = (m['limit']['Balance'])
					output.append({'Balance': bal})
					
	return jsonify({'All Plans Currently Existing' : output})	


#this below route helps in printing out the current existing plans in database
#for this update method is made only to accept the id and print out a new updated id for the plan 
@app.route('/<path:a_plan>')
def new_plan(a_plan):
	out = []
	the_plan = user.find_one({'name': a_plan})
	if (the_plan):
		for n in the_plan['price']:
			if(n == 'amount'):
				out.append({'Amount':the_plan['price'][n]})
		
			elif(n == 'currency'):
				out.append({'Currency':the_plan['price'][n]})
				
		for m in the_plan['features']:
			out.append({'Feature': m['name']})
			for lim in m['limit']:				
				if(lim == 'unit'):
					out.append({'Unit':m['limit']['unit']})					
				elif(lim == 'Balance'):
					bal = (m['limit']['Balance'])
					out.append({'Balance': bal})	
	else:
		out.append("the plan entered"+a_plan+" is incorect")
					
	return jsonify({'The '+a_plan+' has ' : out})

#this below route hepls in creating the add a plan to the connected database
@app.route('/add_a_plan', methods=['POST'])
def add_star():
	the_new_plan = request.json
	print(the_new_plan)
	new_plan = user.find_one({'name': the_new_plan['name']})
	if(new_plan):
		return("the entered plan is existing in database"+the_new_plan['name'])
	else:
		user.insert(the_new_plan)
		return ("Added : "+ the_new_plan['name'])
	


#this below route is made for update
#user enter the plan_id in path and passes the new json value to be updated
@app.route('/<path:plan_id>/update', methods=['POST'])
def update_a_plan(plan_id):
	output = []
	print(plan_id)
	the_plan_updating = user.find_one({'id': plan_id})
	print(the_plan_updating)
	print({'id': plan_id})
	if(the_plan_updating):
		output.append({'the request':(request.json)})
		update_val = request.json
		user.update_many({'id': plan_id}, {"$set":request.json})
		return ("the plan "+plan_id+" was updated.")
	else:
		return ("the "+plan_id+" is not existing in the database...")
	
if __name__ == '__main__':
	app.run(debug=True)
