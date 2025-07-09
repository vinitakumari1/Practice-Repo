from pymongo import MongoClient

mongo_cluster = "mongodb+srv://resumeparse:txAZOJnfDWqUB9ZR@resume.6nnmavs.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
database_name = "test_db"
collection = "users"

#db and collection configuration
client = MongoClient(mongo_cluster) #connect to mongo cluster
database=client[database_name] #get access to database
users=database[collection]


# # users.drop()  # dropping the database
#*************************insert one and insert many*******
# insert_statement = {
#     "user_id":"U1005",
#     "name": {"first":"Manish","last":"reddy"},
#     "dob": "01-01-2020",
#     "contact":{
#         "email":"manish@gmail.com",
#         "phone":["9876536377","837363337389"],
#         "address":{
#             "line1": "A102,Silver Springs",
#             "line2": "Near shivaji park",
#             "city": "Nagpur",
#             "state":"Mharashtra",
#             "zip":"440011"
#         }
#     },
#     "membership":{
#         "type":"Gold",
#         "start_date":"07-08-2024",
#         "expiry_date":"07-08-2026",
#         "benefits":["free-shipping","priority-support","birthday-gift"]
#     },
#     "orders":[{

#         "order_id":"ORD1001",
#         "amount":499.99,
#         "items":[{

#             "product_id":"P01",
#             "quantity":2
#         }]
#     }]
# }


# # users.insert_one(insert_statement)


# insert_many_statement= [
#     {
#         "user_id":"U002",
#         "name":{"first":"ameyyaan","last":"Parse"},
#         "dob":"01-01-2020",
#         "contact":{"email": "smartcoder#gmail.com","address":{"city":"Hyderabad","pin":5009988}},
#         "membership":{"type":"Standard","benefits":["free-shipping"]},
#         "orders":[]
#     },
#     {
#        "user_id":"U001",
#         "name":{"first":"vinita","last":"kumari"},
#         "dob":"01-01-20550",
#         "contact":{"email": "smartcoder#gmail.com","address":{"city":"Hyderabad"}},
#         "membership":{"type":"Standard","benefits":["free-shipping"]},
#         "orders":[
#             {"order_id":"0002", "amount":12009,"quantity":2}]
#     }
# ]

# users.insert_many(insert_many_statement)


###########Find operations ###########

# for user in users.find():
#     print(user)


# find users with city ="hyderabad"

# found_users= users.find(
#   {"contact.address.city":"Hyderbad"}
# )

# for user in found_users:
#     print (user)

# find users with membership =premium


# found_users =users.find(
#     {"membership.type":"Premium"}
# )

# for user in found_users:
#     print (user)


# found_users=users.find({"membership.type":"Standard"},
#                        {"_id":0,"user_id":1,"name.first":1}
#                        )
# for user in found_users:
#     print (user)


#*******Find all the users whose membership -benefits contains the word shipping

# found_users= users.find(
#    {"membership.benefits":{"$regex":"shipping"}}
# )
# for user in found_users:
#     print (user)



