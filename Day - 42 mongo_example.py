from pymongo import MongoClient



mongo_cluster = "mongodb+srv://resumeparse:txAZOJnfDWqUB9ZR@resume.6nnmavs.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
database_name = "test_db"
collection = "people"
client = MongoClient(mongo_cluster) #connect to mongo cluster

database=client[database_name]
people_collection =database[collection]

#******************* Insert One *********************

# insert_one_statement = {"name" : "Manish" , "age" : "25" , "city" : "Hyderabad", "pin_code": 500049}
# insert_one_statement = {"name" : "Manish" , "age" : "25" , "city" : "Hyderabad", "pin_code": 500049,"designation":"agentic ai"}
# insert_one_statement = {"Hello": "world"}
# people_collection.insert_one(insert_one_statement)


#******************Bulk insert / Insert Many ***********

# people_collection.insert_many(
# [
# {"name": "Priyanka","designation": "Agentic AI Developer","Slarty":55000,"doj": "01-01-2025"},
# {"name": "Priyanka","designation": "Agentic AI Developer","Slarty":40000,"doj": "01-01-2025"},
# {"name": "voonna","designation": "Agentic AI Developer","Slarty":30000,"doj": "01-01-2025"}
# ]
# )

#*************Nested insert****************

# people_collection.insert_one(
#     {
#        "name":"Gayatri",
#        "City":"Hyderabad",
#        "Salary": 50000,
#        "Address": {"street":"Hightech city riad","lane": "3rdlane"}

#     }    
#     )


#****************Find all ******************
# for document in people_collection.find():
#     print (document)

#****************Find one ******************
# for document in people_collection.find_one():  #gets first avaliable record
#     print (document)


#*********find one -filter **********
# document= people_collection.find({
#     "name": "Priyanka",
#     "salary": 10000
# })

# for doc in document:
#   print(doc)


# documents= people_collection.find({
#   "Slarty" : {"$gt" : 5000}
# })


# for document in documents:
#     print(documents)


#**************find one -Sort ****************

# documents= people_collection.find().sort("Slarty",-1)

# for document in documents:  #-1 indicates desc   +1 is ascending
#     print (document)

# ####to get highes/lowest #####
# documents= people_collection.find().sort("Slarty",-1).limit(1)

# for document in documents:  #-1 indicates desc   +1 is ascending
#     print (document)

# documents= people_collection.find({},{"_id":1,"name":1,"designation":1}) #_id=0 indicates to ignore id object and 1 gives id object in result
# for document in documents: 
#      print (document)


#***********Find One - Start with *********************


# documents= people_collection.find({
#      "name": {"$regex": "^P" },
     
# })
# for document in documents: 
#     print (document)



#***************delete&**********************

# document= people_collection.delete_one({
#    "name":"Priyanka"

# })

# print (document)
#******************delete many***********
# document= people_collection.delete_many({
#    "Slarty": {"$gt":35000}

# })

# print (document)



document = people_collection.delete_many({
  "Address.lane": "3rdlane"
})
print (document)
