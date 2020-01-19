from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from models.UserModel import User
import random

loadedQuestionsBP = Blueprint('loadedQuestions', __name__, template_folder='templates',
                    static_folder='static', static_url_path='/games/loadedQuestions/static', url_prefix='/LQ')

#Ensures user is logged in for all LoadedQuestions routes
@loadedQuestionsBP.before_request
def before_request():
    user = getUser()
    if not user:
        return redirect(url_for('index'))

@loadedQuestionsBP.route('/lobby')
def lobby():
    return render_template('lobby.html', username = getUser().username)

@loadedQuestionsBP.route('/play')
def play():
    return render_template('play.html', username= getUser().username)

# ---------------- Loaded Questions Game --------------------------

rooms = {} #{roomCode: LQ}
cards = []

with open('games/loadedQuestions/questionCards.txt') as f:
    cards = list(map(lambda x: x.rstrip(), f.readlines()))

class LQ:
    def __init__(self, room_code):
        self.room_code = room_code
        self.users = [] #[{'user': user, score: 0, role: player}]
        self.playerInfo = []#[{'username': name, score: 0, role: player}]
        self.gameStarted = False

        self.askerIndex = 0

        self.current_question = ''
        self.answer_list = []   #{id: user.id, user: username, answer: answer}
        self.all_answers_in = False

    def ask_question(self, question):
        self.current_question = question
        self.gameStarted = False
        self.all_answers_in = False

    def answer_question(self, user, answer):
        self.answer_list.append({'id': user.id, 'user': user.username, 'answer': answer})
        if len(self.answer_list) >= len(self.users) - 1:    #-1 as asker does not answer
            self.all_answers_in = True

    def submit_score(self, score):
        for u in self.users:
            if u['role'] == 'asker':
                u['score'] += score
        self.next_turn()

    def init_room(self):
        self.gameStarted = True
        self.next_turn()

    def next_turn(self):    #set player roles, and update playerInfo
        self.current_question = ''
        self.answer_list = []
        print(self.answer_list)
        for u in self.users:
            u['role'] = 'lobby'

        self.users[self.askerIndex]['role'] = 'asker'

        if self.askerIndex + 1 >= len(self.users):
            self.users[0]['role'] = 'reader'
            self.askerIndex = 0
        else:
            self.users[self.askerIndex+1]['role'] = 'reader'
            self.askerIndex += 1

        self.playerInfo = []    #setup playerInfo for get_info()
        for u in self.users:
            self.playerInfo.append({'username': u['user'].username, 'score': u['score'], 'role': u['role']})

        self.gameStarted = True #notifies players of the next turn


    def join_room(self, user):
        for k,v in rooms.items():       #removes user from any existing rooms
            if v.user_in_room(user):
                v.remove_user(user)

        if not self.user_in_room(user): #adds a user to this room if not already in it
            self.users.append({'user': user, 'score': 0, 'role': 'noob'})
            return {'status': 200}
        return {'status': 400, 'message': 'User {} already in room'.format(user.username)}

    def remove_user(self, user):
        for u in self.users:
            if u['user'].id == user.id:
                self.users.remove(u)
                return {'status': 200}

    def user_in_room(self, user):
        return any([d['user'].id == user.id for d in self.users])

    def find_player_by_id(self, _id):
        for u in self.users:
            if u['user'].id == _id:
                return u
        return None

    def info(self, user):
        player = self.find_player_by_id(user.id)

        return {'nameList': [u['user'].username for u in self.users],
                'role': player['role'], 'playerInfo': self.playerInfo,
                'gameStarted': self.gameStarted, 'currentQuestion': self.current_question,
                'answer_list': self.answer_list, 'allAnswersIn': self.all_answers_in}

# -------------- Play ------------------------
@loadedQuestionsBP.route('/ask_question/<room_code>/<string:question>')
def ask_question(room_code, question):
    room = rooms[room_code]
    room.ask_question(question)
    return jsonify({'status': 200})

@loadedQuestionsBP.route('/answer_question/<room_code>/<answer>')
def answer_question(room_code, answer):
    user = getUser()
    room = rooms[room_code]
    room.answer_question(user, answer)
    return jsonify({'status': 200})

@loadedQuestionsBP.route('/already_answered/<room_code>')
def already_answered(room_code):
    room = rooms[room_code]
    user = getUser()
    return jsonify({'answered': user.id in [a['id'] for a in room.answer_list]})

@loadedQuestionsBP.route('/submit_score/<room_code>/<int:score>')
def submit_score(room_code, score):
    room = rooms[room_code]
    room.submit_score(score)
    return jsonify({'status': 200})

# -------------- General ---------------------

@loadedQuestionsBP.route('/cardList/<int:set_number>')
def card_list(set_number):
    set_number *= 10
    if(set_number + 10 <= len(cards)):
        return jsonify({'cards': cards[set_number:set_number+10], 'moreCards': True})
    return jsonify({'cards': cards[0:10], 'moreCards': False})

@loadedQuestionsBP.route('/room_info/<room_code>')
def room_info(room_code):
    return jsonify(rooms[room_code].info(getUser()))

@loadedQuestionsBP.route('/whatsmyroomcode')
def whats_my_room_code():
    user = getUser()
    for k,v in rooms.items():
        if v.user_in_room(user):
            return jsonify({'status': 200, 'room_code': v.room_code})
    return jsonify({'status': 400})
# ------------- Lobby ------------------------
@loadedQuestionsBP.route('/init/<room_code>') #Start the Game, set roles,
def init_game(room_code):
    r = rooms[room_code.upper()]
    r.init_room()
    return jsonify({'status': 200})

@loadedQuestionsBP.route('/host')
def host():
    rc = getRandomRoomCode()
    rooms[rc] = LQ(rc)
    rooms[rc].join_room(getUser())
    return jsonify({'room_code': rc})

@loadedQuestionsBP.route('/join/<room_code>')
def join(room_code):
    if room_code not in rooms:
        return jsonify({'status': 400, 'message': 'Room not found!'})
    return jsonify(rooms[room_code.upper()].join_room(getUser()))

#-------------- Helpers ----------------------
def getRandomRoomCode():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(4):
        code += letters[random.randint(0,len(letters) - 1)]
    return code if code not in rooms else getRandomRoomcode()

def getUser():
    user = User.json_to_user(session.get('User'))
    return user if user else None
