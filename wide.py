from flask import Flask,jsonify,request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = "mongodb+srv://test:test@wideeye-3ku58.mongodb.net/test?retryWrites=true"

mongo = PyMongo(app)
print("connected i guess")
user = mongo.db.users
user_plan = mongo.db.user_plan


"""

1 create a plan (api/plan/create)
2 update a plan (api/plan/$plan_id/update)
3 retrieve all plans (api/plan/list_all)
4 plan associated with a user(api/$user_id/plan)
5 return the limits/usages for each feature(api/$user_id/plan/feature1/limit)
6 update the the same for above limits (api/$user_id/plan/feature1/limit/update)
 """

# 1 create a plan (api/plan/create)
@app.route('/api/plan/create', methods=['POST'])
def create_plan():
    print(request.json)
    the_new_plan = request.json
    new_plan = user.find_one({'name': the_new_plan['name']})
    if(new_plan):
        return("Entered plan is existing in database"+the_new_plan['name'])
    else:
        user.insert(the_new_plan)
        return ("Added : " + the_new_plan['name'] + " Has just been created!")


# 2 update a plan (api/plan/$plan_id/update)
@app.route('/api/plan/<path:plan_id>/update', methods=['POST'])
def update_a_plan(plan_id):
	the_plan_updating = user.find_one({'id': plan_id})
	print(the_plan_updating)
	print({'id': plan_id})
	if(the_plan_updating):
		user.update_one({'id': plan_id}, {"$set":request.json})
		return ("the plan "+plan_id+" was updated.")
	else:
		return ("the "+plan_id+" is not existing in the database...")

# 3 retrieve all plans (api/plan/list_all) 
@app.route('/api/plan/list_all', methods=['GET'])
def all_planss():
	output = []
	for val in user.find():
		o = {}
		for v in val:			
			if(v != '_id'):
				o[v] = val[v]
		print(o)
		output.append(o)

	return jsonify({"All the plans : " : output })







# 4 plan associated with a user(api/$user_id/plan)
@app.route('/api/<path:user_id>/plan', methods=['POST'])
def user_plans(user_id):
    output = []
    user_existing = user_plan.find_one({'user_id': user_id})
    if(user_existing):
        for val in user_existing['plans']:
            o = {}
            for v in val:
                if(v != '_id'):
                    o[v] = val[v]
                print(o)
            output.append(o)
    
    return jsonify({"Plans associated with: " + user_id: output })


# 5 return the limits/usages for each feature(api/$user_id/plan/feature1/limit)
@app.route('/api/<path:user_id>/plan/feature1/limit', methods=['POST'])
def user_plans_feature1(user_id):
    output = []
    user_existing = user_plan.find_one({'user_id': user_id})
    if(user_existing):
        for val in user_existing['plans']:
            o = {}
            for v in val:
                if(v != '_id'):
                    o[v] = val[v]
                print(o)
            output.append(o)
    
    else:
        print("Nothing")
        output.append({Plans:"None At the moment..."})
        
    return jsonify({"Plans associated with: " + user_id: output })



# 6 update the the same for above limits (api/$user_id/plan/feature1/limit/update)

@app.route('/api/<path:user_id>/plan/feature1/limit/update', methods=['POST'])
def user_plans_update_feature1(user_id):
    output = []
    user_existing = user_plan.find_one({'user_id': user_id})
    if(user_existing):
        features = user_existing['plans']
        for val in features['features']:
            o = {}
            for v in val:
                print
                if(v != '_id'):
                    o[v] = val[v]
                print(o)
            output.append(o)
    
    else:
        print("Nothing")
        output.append({Plans:"None At the moment..."})
        
    return jsonify({"Plans associated with: " + user_id: output })


if __name__ == '__main__':
	app.run(debug=True)