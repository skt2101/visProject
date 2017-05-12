from flask import Flask
from flask import jsonify,abort
from flask_cors import CORS, cross_origin
from lib import utils
app = Flask(__name__)
CORS(app)
app = Flask(__name__)
@app.route("/")
def index():
    return "Hello World"

@app.route("/chord",methods=['GET'])
def getBreakDown():
    return jsonify(minedData[0])

@app.route("/league/<int:leagueId>/scores",methods=['GET'])
def getLeagueScore(leagueId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    return jsonify(minedData[1].get(leagueName))

@app.route("/league/<int:leagueId>/transfers",methods=['GET'])
def getLeagueTransfer(leagueId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    return jsonify(minedTransfers.get(leagueName))

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
    print(minedLeagueData[0].keys())
    return jsonify(minedLeagueData[0].get(leagueName).get(teamName))

@app.route("/league/<int:leagueId>",methods=['GET'])
def getLeagueTeams(leagueId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    return jsonify(minedLeagueData[1].get(leagueName))

@app.route("/diversity/<int:teamId>",methods=['GET'])
def getTeamDiversity(teamId):
    return jsonify(divMap.get(teamId))

if __name__ == '__main__':
    # first get all the data , before opening the port for client access.
    minedData = utils.temp1()
    minedTransfers = utils.temp2()
    minedLeagueData = utils.topPlayerEvolution()
    divMap = utils.diversity1()
    app.run()
    