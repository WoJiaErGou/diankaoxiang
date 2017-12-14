import pymongo
# with pymongo.MongoClient('172.28.171.13') as client:
client = pymongo.MongoClient(host='172.28.171.13', port=27017)
db=client.DKX
coll=db.dkx_sn
coll.remove()
# client.database_names()
print(db.collection_names())
print(coll.find_one())