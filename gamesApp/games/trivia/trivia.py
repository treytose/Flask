from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from models.UserModel import User
import random
import time

triviaBP = Blueprint('trivia', __name__, template_folder='templates',
                    static_folder='static', static_url_path='/games/trivia/static', url_prefix='/trivia')


@triviaBP.route('/lobby')
def lobby():
    return render_template('trivia_lobby.html', username=get_user().username)

@triviaBP.route('/host')
def host():
    return render_template('trivia_host.html', username=get_user().username)

@triviaBP.route('/play')
def play():
    return render_template('trivia_player.html', username=get_user().username)


@triviaBP.before_request
def before_request():
    if not get_user():
        return redirect(url_for('index'))



# ---------------- Trivia Game ---------------------- #
# ______________________ API ________________________ #
@triviaBP.route('/create_room', methods=['POST'])
def create_room():
    room_code = get_random_roomcode()
    room_mapping[room_code] = Trivia_Room(room_code)
    get_room(room_code).host_id = get_user().id
    return jsonify({'room_code': room_code, 'status': 200})

@triviaBP.route('/join_room/<room_code>/<team_name>', methods=['POST'])
def join_room(room_code, team_name):
    room = get_room(room_code)
    if not room:
        return jsonify({'status': 404})
    resp = room.add_player(get_user(), team_name)
    return jsonify({'first_player': resp['first_player'], 'status': 200})

@triviaBP.route('/next_turn/<room_code>', methods=['POST'])
def next_turn(room_code):
    get_room(room_code).new_round()
    return jsonify({'status': 200})

@triviaBP.route('/room_info/<room_code>', methods=['GET', 'POST'])
def room_info(room_code):
    return jsonify(get_room(room_code).get_room_info())

@triviaBP.route('/start_timer/<room_code>', methods=['POST'])
def start_time(room_code):
    get_room(room_code).start_timer()

# ___________________ Gameplay API ________________ #
@triviaBP.route('/answer_question/<room_code>/<answer>', methods=['POST'])
def answer_question(room_code, answer):
    room = get_room(room_code)
    return jsonify(room.answer_question(get_user(), answer))

@triviaBP.route('/game_over/<room_code>', methods=['POST'])
def game_over(room_code):
    room = get_room(room_code)
    if room and get_user().id == room.host_id:
        room.game_over = True
        for p in room.players:
            p.score = 0
        return jsonify({'status': 200})
    return jsonify({'status': 404, 'message': 'room or user not found'})

@triviaBP.route('/play_again/<room_code>', methods=['POST'])
def play_again(room_code):
    room = get_room(room_code)
    if room and room.get_player_by_user(get_user()):
        room.play_again = True
        return jsonify({'status': 200})
    return jsonify({'status': 404, 'message': 'room or user not found'})


# __________________________ Host _______________________ #
#this just informs the server the host asked the questions and the clients should now display the answerlist
@triviaBP.route('/question_asked/<room_code>', methods=['POST'])
def question_asked(room_code):
    room = get_room(room_code)
    room.question_asked = True
    return jsonify({'status': 200})

@triviaBP.route('/times_up/<room_code>', methods=['POST'])
def times_up(room_code):
    room = get_room(room_code)
    room.times_up = True
    room.game_started = False
    return jsonify({'status': 200})
# ______________________ Init _____________________ #
room_mapping = {} #{room_code: room()}
questions_list = [] #[[question, answer, fasle1, false2, false3], ...]

def get_room(room_code):
    room_code = room_code.upper()
    return room_mapping[room_code] if room_code in room_mapping else None


# ----------- Create Questions List -------------------#
with open('games/trivia/questions.csv') as f:
    for count, line in enumerate(f.readlines()):
        questions_list.append(line.split('~'))
        questions_list[count][len(questions_list[count])-1] = questions_list[count][len(questions_list[count])-1].rstrip('\n')
        random.shuffle(questions_list)


# _______________________ Classes _____________________ #
class Player:
    def __init__(self, _id, username):
        self.id = _id
        self.username = username
        self.score = 0
        self.answer = ''
        self.answer_correct = False

    def to_json(self):
        return {'id': self.id, 'username': self.username, 'score': self.score,
                'answer': self.answer, 'answer_correct': self.answer_correct}



class Trivia_Room:
    def __init__(self, room_code):
        self.room_code = room_code
        self.players = []   #[Player, Player]
        self.current_question = ''
        self.q_index = 0
        self.current_answer = ''
        self.answer_list = []
        self.room_info = {}
        self.game_started = False   #tells clients when to load in
        self.game_over = False #tells the client when someone has won the match. Prompts play again?
        self.play_again = False #tells the host the player clicked play again.

        self.host_id = -1

        self.all_answers_in = False #tells the clients and host to load the next stage when all players have answered
        self.question_asked = False #tells the clients when to display the answer list
        self.times_up = False       #if times_up players can no longer submit an answer
        random.shuffle(questions_list)

    def new_round(self):
        self.current_question = questions_list[self.q_index][0] #get new question
        self.current_answer = questions_list[self.q_index][1]
        self.answer_list = questions_list[self.q_index][1:5]
        self.q_index += 1
        random.shuffle(self.answer_list)
        self.game_started = True
        self.times_up = False
        self.question_asked = False
        self.all_answers_in = False

        for player in self.players:
            player.answer = ''
            player.answer_correct = False

    def add_player(self, user, team_name):
        if not user.id in [player.id for player in self.players]:
            self.players.append(Player(user.id, team_name))
        if(len(self.players) == 1):
            return {'first_player': True}
        return {'first_player': False}

    def answer_question(self, user, answer):
        if self.times_up:
            return {'message': "Time's up!", 'status': 200}

        self.game_started = False   #TODO may need to move this?



        player = self.get_player_by_user(user)
        if not player:
            return {'status': 404}  #return 404 if player not found

        player.answer = answer
        if answer.lower() == self.current_answer.lower():
            player.score += 1
            player.answer_correct = True

        self.check_all_answers_in()

        return {'message': 'Answered Successfully', 'status': 200}

    def get_player_by_user(self, user):
        for p in self.players:
            if p.id == user.id:
                return p
        return None

    def check_all_answers_in(self):
        num_answers = 0         #check if all answers are in
        for p in self.players:
            if p.answer != '':
                num_answers += 1
        if num_answers >= len(self.players):
            self.all_answers_in = True

        self.game_over = False   #TODO may need to change?
        self.play_again = False

    #places valuable information of the room all in one dictionary
    def get_room_info(self):
        playersJSON = [p.to_json() for p in self.players]
        return {'players': playersJSON, 'current_question': self.current_question,
                'current_answer': self.current_answer, 'answer_list': self.answer_list,
                'game_started': self.game_started, 'question_asked': self.question_asked,
                'times_up': self.times_up, 'all_answers_in': self.all_answers_in,
                'game_over': self.game_over, 'play_again': self.play_again}





# ________________________ Helpers ____________________ #
def get_random_roomcode():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(4):
        code += letters[random.randint(0,len(letters) - 1)]
    return code if code not in room_mapping else getRandomRoomcode()

def get_user():
    user = User.json_to_user(session.get('User'))
    return user if user else None
