import flask
import json
from datetime import datetime
def use(response):
	response['resultCode']='success'
	with open('data/user/userItemList.json',encoding='utf-8') as f:
		userItemList=json.load(f)

	with open('data/user/userStatusList.json', encoding='utf-8') as f:
		userStatusList=json.load(f)

	bpPotions=next(filter(lambda item: item['itemId']=='CURE_BP',userItemList))
	bpPotions['quantity']-=1


	battlePoints=next(filter(lambda item: item['statusId']=='BTP',userStatusList))
	battlePoints['point']=5
	battlePoints['checkedAt']:(datetime.now()).strftime('%Y/%m/%d %H:%M:%S')

	with open('data/user/userStatusList.json','w+', encoding='utf-8') as f:
		json.dump(userStatusList, f, ensure_ascii=False)

	#uncomment when we have a way to restore bp
	#with open('data/user/userItemList.json','w+', encoding='utf-8') as f:
		#   json.dump(userItemList, f, ensure_ascii=False)
	response['userItemList']=[bpPotions]
	response['userStatusList']=[battlePoints]

def handleUserItem(endpoint):
    specialCases={
        'use':use,
    }
    response={} 
    if endpoint in specialCases.keys():
        specialCases[endpoint](response)
        return flask.jsonify(response)

