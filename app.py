from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json

# Connect to our local MongoDB
client = MongoClient(host='mongodb', port=27017)

# Choose InfoSys database
db = client['InfoSys']
students = db['Students']

# Initiate Flask App
app = Flask(__name__)

# Insert Student
# Create Operation
@app.route('/insertstudent/<string:email>/<yearOfBirth>', methods=['POST','GET','PATCH'])
def insert_student(email,yearOfBirth):
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "name" in data or not "yearOfBirth" in data or not "email" in data or not "address" in data:
        return Response("Information incompleted",status=500,mimetype="application/json")
    
    if students.find({"email":data["email"]}, {"address":data["address"]}).count() == 0 :
        student = {"email": data['email'], "name": data['name'],  "yearOfBirth":data['yearOfBirth'], "address":data['address']}
        # Add student to the 'students' collection
        students.insert_one(student)
        return Response("was added to the MongoDB",status=200,mimetype='application/json') 
    else:
        return Response("A user with the given email already exists",status=200,mimetype='application/json')

# Read Operations
# Get all students
@app.route('/getallstudents', methods=['GET'])
def get_all_students():
    iterable = students.find({})
    output = []
    for student in iterable:
        student['_id'] = None 
        output.append(student)
    return jsonify(output)

# Get the number of all the students in the DB 
@app.route('/getstudentcount', methods=['GET'])
def get_students_count():
    number_of_students = students.find({}).count()
    return jsonify({"Number of students": number_of_students})

# Find student by email
@app.route('/getstudent/<string:email>', methods=['GET'])
def get_student_by_email(email):
    if email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    student = students.find_one({"email":email})
    if student !=None:
        student = {'_id':str(student["_id"]),'name':student["name"],'email':student["email"], 'yearOfBirth':student["yearOfBirth"]}
        return jsonify(student)
    return Response('no student found',status=500,mimetype='application/json')

# Find students with valid address
@app.route('/getStudentsWithAddress', methods=['GET'])
def get_students_with_address():

       
        data = json.loads(request.data)
        student= students.find({"address":data["address"]}).count()
     
        return(student)
   
                                                                                                        
   
    

# Find students address by email    
@app.route('/getStudentsAddress/<student_email>', methods=['GET'])
def get_students_address_by_email(student_email):
    if student_email == None:
        return Response("Bad request", status=500, mimetype='application/json')
    student = students.find_one({"email":student_email})
    if student !=None:
        student = {'address':student["address"],'email':student["email"]}
        return jsonify(student)
    return Response('no student found',status=500,mimetype='application/json')

# Find students born in 80s and have a home
@app.route('/getEightsAddress', methods=['GET'])
def get_students_eights_address():
    num_of_students = students.find({'yearOfBirth':{'$gte':1980,'$lte':1990}}, {'address'}).count
   
    return jsonify({"Number of students born in 80s having a valid address": num_of_students})

# Find number of students with 
@app.route('/getcountAddress', methods=['GET'])
def get_students_address():
    cursor = students.find({"address": True})
    
          
    return jsonify(cursor.count())

# Find number of students born in yearOfBirth
@app.route('/countYearOfBirth/<yearOfBirth>', methods=['GET'])
def count_year_of_birth(yearOfBirth):
    if yearOfBirth == None:
        return Response("Bad request", status=500, mimetype='application/json')
    student = students.find({'yearOfBirth':{'$gte':int(yearOfBirth)}}).count()
    if student !=None:
       return jsonify({"Students borned at the selected year": student})
    return Response('no student found',status=500,mimetype='application/json')

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)