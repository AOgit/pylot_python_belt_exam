""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self, info):

        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not info['name']:
            errors.append('Name cannot be blank')
        elif len(info['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        elif not info['name'].isalpha():
            errors.append("Name must be letters only.")
        if not info['alias']:
            errors.append('Alias cannot be blank')
        elif len(info['alias']) < 2:
            errors.append('Alias must be at least 2 characters long')
        elif not info['alias'].isalpha():
            errors.append("Alias must be letters only.")
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['p_con']:
            errors.append('Password and confirmation must match!')

        if errors:
            return {"status": False, "errors": errors}
        else:
            password = info['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (name, alias, email, pw_hash, birthdate) VALUES (:name, :alias, :email, :pw_hash, :birthdate)"
            data = {'name': info['name'], 'alias': info['alias'], 'email': info['email'], 'pw_hash': hashed_pw, 'birthdate': info['birthdate']}
            self.db.query_db(query, data)
            return {"status": True} 

    def login_user(self, info):
        password = info['password']
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.query_db(user_query, user_data)
        if user:
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                return True
        return False

    def get_alias(self, info):
        user_query = "SELECT alias FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        return self.db.query_db(user_query, user_data) 

       
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """