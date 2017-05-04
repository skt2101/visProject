from flask import Flask
from flask import jsonify,abort
from lib import utils
app = Flask(__name__)
@app.route("/")
def index():
    return "Hello World"

@app.route("/chord",methods=['GET'])
def getBreakDown():
    return jsonify(minedData[0])

@app.route("/league/scores/<int:leagueId>",methods=['GET'])
def getLeagueScore(leagueId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    return jsonify(minedData[1].get(leagueName))

@app.route("/league/transfers/<int:leagueId>",methods=['GET'])
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
if __name__ == '__main__':
    # first get all the data , before opening the port for client access.
    #minedData = utils.temp1()
    #minedTransfers = utils.temp2()
    minedLeagueData = utils.topPlayerEvolution()
    app.run()
    