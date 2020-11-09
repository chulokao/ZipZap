import json
import flask
from datetime import datetime, timedelta
from mitmproxy import http


def arenaStart(response):
    with open('data/arenaStartDummy.json') as f:
        dummyResponse=json.load(f)
    response["resultCode"]="success"
    #response["userArenaBattleMatch"]=dummyResponse["userArenaBattleMatch"]
    response["userArenaBattleResultList"]=dummyResponse["userArenaBattleResultList"]
    response["userArenaBattleResultList"][0]["createdAt"]=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    response["userQuestBattleResultList"]=dummyResponse["userQuestBattleResultList"]
    response["userQuestBattleResultList"][0]["createdAt"]=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    with open('data/user/userQuestBattleResult.json', 'w+', encoding='utf-8') as f:
        json.dump(response["userQuestBattleResultList"][0], f, ensure_ascii=False)
    
    #This actually matches with UserArenaBattle in /native/send/result
    with open('data/user/userArenaBattleResult.json', 'w+', encoding='utf-8') as f:
        json.dump(response["userArenaBattleResultList"][0], f, ensure_ascii=False)

def arenaReload(response):
    currentTime=(datetime.now()).strftime('%Y/%m/%d %H:%M:%S')
    with open('data/arenaFreeRankDummy.json') as f:
        dummyResponse=json.load(f)
    response['userArenaBattleMatch']=dummyResponse['userArenaBattleMatch']
    response['userQuestBattleResultList']=dummyResponse['userQuestBattleResultList']
    response['userArenaBattleResultList']=dummyResponse['userArenaBattleResultList']
    response['userArenaBattleMatch']['matchedAt']=(datetime.now()).strftime('%Y/%m/%d %H:%M:%S')
    response['userArenaBattleMatch']['expiredAt']=(datetime.now()+timedelta(minutes=20)).strftime('%Y/%m/%d %H:%M:%S')

    with open('data/user/userStatusList.json', encoding='utf-8') as f:
        userStatusList=json.load(f)

    battlePoints=next(filter(lambda item: item['statusId']=='BTP',userStatusList))
    #don't ask me why, reload always sends action points as well
    actionPoints=next(filter(lambda item: item['statusId']=='ACP',userStatusList))

    if(battlePoints['point']!=0):
        battlePoints['point']-=1

    battlePoints['checkedAt']:currentTime

    with open('data/user/userStatusList.json','w+', encoding='utf-8') as f:
        json.dump(userStatusList, f, ensure_ascii=False)
    #TODO debug why bp doesn't go down clientside
    print(battlePoints)
    response['userStatusList']=[battlePoints,actionPoints]

def handleArena(endpoint):
    specialCases={
        'start':arenaStart,
        'reload':arenaReload
    }
    response={} 
    if endpoint in specialCases.keys():
        specialCases[endpoint](response)
        return flask.jsonify(response)

