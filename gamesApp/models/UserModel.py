import sqlite3
import json

class User:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        data = cursor.execute('SELECT * FROM users WHERE LOWER(username)=?', (username.lower(),)).fetchone()
        connection.close()
        return cls(*data) if data else None


    def check_pass(self, password):
        return self.password == password


    #method for converting a User Object into a JSON string for serialization.
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    #method for converting a JSON string back into a User object
    @classmethod
    def json_to_user(cls, json_data):
        if json_data is None:
            return None
        parsed_json = json.loads(json_data)
        parsed_json['_id'] = parsed_json.pop('id') #swapping the key named id to _id for the User object
        return User(**parsed_json)

    @classmethod
    def register_user(cls, **kwargs):
        if cls.find_by_username(kwargs['username'][0]):
            return False
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        data = cursor.execute('INSERT INTO users VALUES(?,?,?)',
                (None, kwargs['username'][0], kwargs['password'][0]))
        connection.commit()
        connection.close()
        return cls.find_by_username(kwargs['username'][0])
