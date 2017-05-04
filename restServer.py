from flask import Flask
from flask import jsonify,abort
from lib import utils
app = Flask(__name__)
@app.route("/")
def index():
    return "Hello World"
players = []
players.append({"name":"Messi","country":"Argentina","id":0})
players.append({"name":"Ronaldo","country":"Portugal","id":1})

@app.route("/players",methods=['GET'])
def getPlayers():
    return jsonify({"players":players})
@app.route("/players/<int:playerId>",methods=['GET'])
def getPlayer(playerId):
    temp = [ player for player in players if player.get("id") == playerId ]
    if len(temp) == 0 :
        # no player found with this particular Id.
        abort(404)
    return jsonify(temp)
@app.route("/chord",methods=['GET'])
def getBreakDown():
    return jsonify(t[0])
@app.route("/league/scores/<int:leagueId>",methods=['GET'])
def getLeagueScore(leagueId):
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]
    return jsonify(t[1].get(leagueName))
if __name__ == '__main__':
    # first get all the data , before opening the port for client access.
    t = utils.temp1()
    print("calling app")
    app.run()
    