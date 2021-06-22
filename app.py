from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time
from bson.json_util import dumps, loads

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['DSMarkets']

# Choose collections
users = db['Users']
products = db['Products']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}
global new_quant
global product_up
propertie = 'yo'






def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    return user_uuid in users_sessions
def createlist():
     global new_list  
     new_list = [] 
     return new_list
     
def costlist():
     global sum_list  
     sum_list = [] 
     return sum_list  
  


@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "password" in data or not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
        
        
        
    if users.find({"email":data["email"]}).count() == 0 :
       user = {"name": data['name'] , "password": data['password'], "email": data['email'], "category": 'A', }
       users.insert_one(user)
       return Response(data['name']+"was added to DS Markets",status=200,mimetype='application/json')
    else:
       return Response("A user with the given email already exists",status=200,mimetype='application/json')
       
       
       
@app.route('/login', methods=['POST'])
def login():
    createlist()
    costlist()
    
    
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    if users.find({"email":data["email"]}).count() > 0 and users.find({"password":data["password"]}).count() > 0:
    	user= users.find_one({"email":data["email"]})
    	global propertie
    	propertie = user.get('category')
    	
    	user_uuid = create_session(data["email"])
    	res = {"uuid": user_uuid, "email": data['email']}
    	return Response(json.dumps(res), status=200, mimetype='application/json')   # ΠΡΟΣΘΗΚΗ STATUS
    	
    
    	
     
    		
    else :
    	return Response("Wrong username or password.", status=400,mimetype='application/json')
    	
    	

@app.route('/getProduct', methods=['GET'])
def get_product():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "epilogh" in data or not "epilekteo" in data or not "uuid" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
        
        
        
        
    
    if is_session_valid(data["uuid"]):
    	if data["epilogh"] == 'name':
    		product = products.find_one({"name":data["epilekteo"]})
    		if product!= None:
    			product = {'name':product["name"],'description':product["description"], 'price':product["price"], 'category':product["category"], 'unique_id':product["unique_id"]}
    			return jsonify(product)
    		else:
    			return Response('No student found with that name '+ data["epilekteo"] +' was found',status=500,mimetype='application/json')	
    	elif data["epilogh"] == 'category':
    		product = products.find_one({"category":data["epilekteo"]})
    		if product!= None:
    			product = {'name':product["name"],'description':product["description"], 'price':product["price"], 'category':product["category"], 'unique_id':product["unique_id"]}
    			return jsonify(product)
    		else:
    			return Response('No student found with that name '+ data["epilekteo"] +' was found',status=500,mimetype='application/json')
    	elif data["epilogh"] == 'unique_id':
    		product = products.find_one({"unique_id":data["epilekteo"]})
    		if product!= None:
    			product = {'name':product["name"],'description':product["description"], 'price':product["price"], 'category':product["category"], 'unique_id':product["unique_id"]}
    			return jsonify(product)
    		else:
    			return Response('No student found with that name '+ data["epilekteo"] +' was found',status=500,mimetype='application/json')
    					
    		
    		
    else:
    	Response("Information incomplete",status=500,mimetype="application/json")
    	
    	
    	
    	
@app.route('/addkalathi', methods=['GET'])
def get_addkalathi():

    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "unique_id" in data  or not "uuid" in data or not "quantity" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
        
        
        
        
    
    if is_session_valid(data["uuid"]):
    	product = None
    	product = products.find_one({"unique_id":data["unique_id"]})
    	apothema = product.get('quantity')
    	new_quant = apothema - int(data["quantity"])
    	
    	if product != None and apothema >= int(data["quantity"]) and apothema != 0:
    		cursor = products.find({"unique_id":data["unique_id"]})
    		list_cur = list(cursor)
    		new_list.append(str(list_cur))
    		
    		
    		cursor2= int(data["quantity"])*product.get('price')
    		
    		sum_list.append(cursor2)
    		total=0
    		ele=0
    		while(ele < len(sum_list)):
    			total = total + sum_list[ele]
    			ele+=1
    		
    		print(total)
    		dedomena = {'new_list': new_list , 'total':total}
    		json_data = dumps(dedomena, indent = 2 )
    		try:
    		     product = products.update_one({"unique_id":data["unique_id"]},
    		     {"$set":
    		         {
    		         
    		               "quantity":new_quant
    		         }      
    		     })
    	
    		
    		except Exception as e:			
    		   return Response({'User could not be updated'},status=500,mimetype='application/json')
    		return Response('Τα προιοντα που εχετε επιλεξει ειναι τα ακολουθα και στο πεδιο quantity φαινεται το αποθεμα του μαγαζιου στο συγκεκριμενο προιον μετα την καθε αγορα σας.Το συνολικο κοστος ειναι '+json_data, status=500,  mimetype='application/json')
    	else:
    		return Response('Error, Do you want to',status=500,mimetype='application/json')			   	
    else:
    	return Response("the user has not been authenticated",status=401,mimetype="application/json")					
 	       
       
       




@app.route('/viewkalathi', methods=['GET'])
def view_addkalathi():
    ele=0
    total=0
    while(ele < len(sum_list)):
    	total = total + sum_list[ele]
    	ele+=1
    	
    	
    dedomena = {'new_list': new_list , 'total':total}
    json_data = dumps(dedomena, indent = 2 )		
    if json_data != None:
    	return Response('Τα προιοντα που εχετε επιλεξει ειναι τα ακολουθα και στο πεδιο quantity φαινεται το αποθεμα του μαγαζιου στο συγκεκριμενο προιον μετα την καθε αγορα σας.Το συνολικο κοστος ειναι '+json_data, status=500,  mimetype='application/json')
    else:
    	return Response("TO kalathi einai adio")	
    	
    	
    	
@app.route('/delkalathi', methods=['GET'])
def del_kalathi():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "unique_id" in data  or not "uuid" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    if is_session_valid(data["uuid"]):
    	product = products.find_one({"unique_id":data["unique_id"]})
    	if product != None:
    		cursor = products.find_one({"unique_id":data["unique_id"]})
    		list_cur = list(cursor)
    		new_list.remove(str(str(list_cur)))
    		
    		poso = product.get('price')
    		total=0
    		ele=0
    		while(ele < len(sum_list)):
    			total = total + sum_list[ele]
    			ele+=1
    			
    		total=total-poso
    		dedomena = {'new_list': new_list , 'total':total}
    		json_data = dumps(dedomena, indent = 2 )
    		if json_data != None:
    			return Response('Τα προιοντα που εχετε επιλεξει ειναι τα ακολουθα και στο πεδιο quantity φαινεται το αποθεμα του μαγαζιου στο συγκεκριμενο προιον μετα την καθε αγορα σας.Το συνολικο κοστος ειναι '+json_data, status=500,  mimetype='application/json')
    		else:
    			return Response("TO kalathi einai adio")
    	else:
    		return Response("To proion pou zhthtai den vrethike")				
    			
    		
    			    	



@app.route('/buykalathi', methods=['GET'])
def buy_kalathi():
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "card_number" in data  or not "uuid" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    if is_session_valid(data["uuid"]):
    	length = len(data["card_number"])
    	if length > 16:
    		total=0
    		ele=0
    		while(ele < len(sum_list)):
    			total = total + sum_list[ele]
    			ele+=1
    		dedomena = {'Λιστα προιοντων που εχουν προστεθει στο καλαθι': new_list , 'Συνολικο ποσο':total}
    		json_data = dumps(dedomena, indent = 2 )
    		if json_data != None:
    			return Response('*****RECIEPT*****'+json_data+ '*****THANK YOU*****', status=500,  mimetype='application/json')
    		else:
    			return Response("TO kalathi einai adio")
    	else:
    		return Response("Λαθος δομη αριθμου καρτας")			
    	    
	


@app.route('/deleteuser', methods=['DELETE'])
def delete_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "uuid" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
        
    if is_session_valid(data["uuid"]):
    	user = users.find_one({"email":data["email"]})
    	if user!= None:
    		users.delete_one({"email": data["email"]})
    		return Response("User deleted successfuly", status=200, mimetype='application/json')
    	else:
    		return	Response('Error not deleted', status=200, mimetype='application/json')
    			
    		
@app.route('/createProduct', methods=['POST'])
def create_product():
    # Request JSON data
    data = None
    global propertie
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "category" in data or not "quantity" in data or not "description" in data or not "price" in data or not "uuid" in data or not "unique_id" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    if is_session_valid(data["uuid"]) and propertie == 'D' :
    	if products.find({"name":data["name"]}).count() == 0 and products.find({"unique_id":data["unique_id"]}).count() == 0:
    		product = {"name": data['name'] , "category": data['category'], "quantity": data['quantity'], "description": data['description'], "price":data['price'], "unique_id":data['unique_id'] }
    		products.insert_one(product)
    		return Response(data['name']+"was added to DS Markets",status=200,mimetype='application/json')		
    	else:
    		return Response("A product with the given name or unique id already exists",status=200,mimetype='application/json')
    else:
    	return Response('Den exete Dikaiwmata Diaxeiristh')			
    	 
    	    
        
    
@app.route('/deleteProduct', methods=['DELETE'])
def delete_product():
    # Request JSON data
    global propertie
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "unique_id" in data or not "uuid" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
        
    if is_session_valid(data["uuid"]) and propertie == 'D':
    	product = products.find_one({"unique_id":data["unique_id"]})
    	if product != None:
    		products.delete_one({"unique_id": data["unique_id"]})
    		return Response("Product deleted successfuly", status=200, mimetype='application/json')
    	else:
    		return	Response('Error not deleted', status=200, mimetype='application/json')
    else:
    	return Response('Den exete Dikaiwmata Diaxeiristh')
    	
    	
    	
    	
    	
@app.route('/updateProduct', methods=['GET'])
def update_product():
    # Request JSON data
    global propertie
   
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "epilogh" in data or not "epilekteo" in data or not "uuid" in data or not "unique_id" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
        
        
    if is_session_valid(data["uuid"]) and propertie == 'D' :
    	if data["epilogh"] == 'price':
    		product = products.find_one({"unique_id":data["unique_id"]})
    		if product!= None:
    			try:
    			    product = products.update_one({"unique_id":data["unique_id"]},
    			    {"$set":
    			        {
    		         
    		               "price":data["epilekteo"]
    		         	}
    		            })
    		           
    			except Exception as e:
    			   return Response("Information incomplete",status=500,mimetype="application/json")	     
    		else:
    			return Response('No student found with that name '+ data["epilekteo"] +' was found',status=500,mimetype='application/json')	
    	elif data["epilogh"] == 'description':
    		product = products.find_one({"unique_id":data["unique_id"]})
    		if product!= None:
    			product = {'name':product["name"],'description':product["description"], 'price':product["price"], 'category':product["category"], 'unique_id':product["unique_id"]}
    			return jsonify(product)
    		else:
    			return Response('No student found with that name '+ data["epilekteo"] +' was found',status=500,mimetype='application/json')
    	elif data["epilogh"] == 'quantity':
    		product = products.find_one({"unique_id":data["unique_id"]})
    		if product!= None:
    			try:
    			    product = products.update_one({"unique_id":data["unique_id"]},
    			    {"$set":
    			        {
    		         
    		               "quantity":data["epilekteo"]
    		         	}
    		            })
    		           
    			except Exception as e:
    			   return Response("Information incomplete",status=500,mimetype="application/json")
    			return Response("H allagh sas oloklirwthike",status=500,mimetype="application/json")		   	   
    		else:
    			return Response('No student found with that name '+ data["epilekteo"] +' was found',status=500,mimetype='application/json')
    	elif data["epilogh"] == 'name':
    		product = products.find_one({"unique_id":data["unique_id"]})
    		if product!= None:
    			try:
    			    product = products.update_one({"unique_id":data["unique_id"]},
    			    {"$set":
    			        {
    		         
    		               "name":data["epilekteo"]
    		         	}
    		            })
    			except Exception as e:
    			   return Response("Information incomplete",status=500,mimetype="application/json")	   
    		else:
    			return Response('No student found with that name '+ data["epilekteo"] +' was found',status=500,mimetype='application/json')				
    	else:
    		return Response('Mh diathesimh epilogh')  	
    		
    else:
    	return Response("Information incomplete",status=500,mimetype="application/json")    
        
    
    
		  
	  
	
		
		
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)              
    
