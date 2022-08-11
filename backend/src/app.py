from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/teams'
mongo = PyMongo(app)

CORS(app)

playerDB = mongo.db.playerCollection
teamDB = mongo.db.teamCollection


# @app.route("/teams")
# def index():
#     return '<h1>Hello</h1>'

@app.route("/addTeam", methods=["POST"])
def addTeam():
    team_name = request.json["team_name"]
    id = teamDB.insert_one({
        'team_name': team_name
    })
    return jsonify({
        'msg': "Team Added Successfully"
    })

@app.route("/teams", methods=["GET"])
def getAllTeams():
    teams = []
    for doc in teamDB.find():
        teams.append({
            '_id': str(ObjectId(doc['_id'])),
            'team_name': doc['team_name']
        })
    return jsonify(teams)

@app.route("/team/<team_name>", methods=["GET"])
def getTeamByTeamName(team_name):
    team = teamDB.find_one({'team_name': team_name})
    return jsonify({
        '_id': str(ObjectId(team['_id'])),
        'team_name': team['team_name']
    })

@app.route("/addPlayer", methods=["POST"])
def addPlayer():
    name = request.json["name"]
    age = request.json["age"]
    position = request.json["position"]
    ranking = request.json["ranking"]
    team = request.json["team"]
    
    id = playerDB.insert_one({
        'name': name,
        'age': age,
        'position': position,
        'ranking': ranking,
        'team': team
    })
    return jsonify({
        'msg': "Player Added Successfully"
    })

@app.route("/players", methods=["GET"])
def getAllPlayers():
    players = []
    for doc in playerDB.find():
        players.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'age': doc['age'],
            'position': doc['position'],
            'ranking': doc['ranking'],
            'team': doc['team']
        })
    return jsonify(players)

@app.route("/player/<id>", methods=["GET"])
def getPlayerById(id):
    player = playerDB.find_one({'_id': id})
    return jsonify({
        '_id': str(ObjectId(player['id'])),
        'name': player['name'],
        'age': player['age'],
        'position': ['position'],
        'ranking': ['ranking'],
        'team': ['team']
    })

if __name__ == '__main__':
    app.run(debug = True)