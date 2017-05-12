from flask import Flask
import flask
from flask import jsonify,abort
from flask_cors import CORS, cross_origin
from lib import utils
import json
app = Flask(__name__)
CORS(app)
app = Flask(__name__)
@app.route("/")
def index():
    
    
    resp=flask.Response(json.dumps({"abcd":"efgh"}))
    resp.headers['Access-Control-Allow-Headers']="X-Requested-With"
    return resp
@app.route("/chord",methods=['GET'])
def getBreakDown():
    t = minedData[0]
    resp=flask.Response(json.dumps(t))
    resp.headers['Access-Control-Allow-Headers']="X-Requested-With"
    return resp
@app.route("/league/<int:leagueId>/scores",methods=['GET'])
def getLeagueScore(leagueId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    t = minedData[1].get(leagueName)
    resp=flask.Response(json.dumps(t))
    resp.headers['Access-Control-Allow-Headers']="X-Requested-With"
    return resp

@app.route("/league/<int:leagueId>/transfers",methods=['GET'])
def getLeagueTransfer(leagueId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    t = minedTransfers.get(leagueName)
    resp=flask.Response(json.dumps(t))
    resp.headers['Access-Control-Allow-Headers']="X-Requested-With"
    return resp

@app.route("/league/<int:leagueId>/teams/<int:teamId>/evolution",methods=['GET'])
def getTopPlayerEvolution(leagueId,teamId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    teamName =''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    teams = utils.getAllDatafromTable('team')
    for team in teams:
        if team[1] == teamId:teamName=team[3]
    #print(minedLeagueData[0].keys())
    t = minedLeagueData[0].get(leagueName).get(teamName)
    resp=flask.Response(json.dumps(t))
    resp.headers['Access-Control-Allow-Headers']="X-Requested-With"
    return resp
    #return jsonify(minedLeagueData[0].get(leagueName).get(teamName))

@app.route("/league/<int:leagueId>",methods=['GET'])
def getLeagueTeams(leagueId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    t = minedLeagueData[1].get(leagueName)
    resp=flask.Response(json.dumps(t))
    resp.headers['Access-Control-Allow-Headers']="X-Requested-With"
    return resp
    

@app.route("/diversity/<int:teamId>",methods=['GET'])
def getTeamDiversity(teamId):
    t = divMap.get(teamId)
    resp=flask.Response(json.dumps(t))
    resp.headers['Access-Control-Allow-Headers']="X-Requested-With"
    return resp
@app.route("/predictions/<int:leagueId>",methods=['GET'])
def predict(leagueId):
    t = predictions.get(leagueId)
    resp=flask.Response(json.dumps(t))
    resp.headers['Access-Control-Allow-Headers']="X-Requested-With"
    return resp

if __name__ == '__main__':
    # first get all the data , before opening the port for client access.
    minedData = utils.temp1()
    #minedTransfers = utils.temp2()
    minedLeagueData = utils.topPlayerEvolution()
    divMap = utils.diversity1()
    predictions = utils.prediction()
    app.run()
    