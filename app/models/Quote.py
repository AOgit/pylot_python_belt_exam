""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()

    def show_all_quotes(self):
        query = "SELECT * FROM quotes"
        return self.db.query_db(query)

    def show_favorites(self):
        query = "SELECT * FROM myfavs"
        return self.db.query_db(query)

    def create(self, b, alias):
        query = "INSERT INTO quotes (name, quote, quoted_by) VALUES (:name, :quote, :quoted_by)"
        values = {
            'name': alias,
            'quote': b['message'],
            'quoted_by': b['quoted_by']
        }
        return self.db.query_db(query, values)

    def delete_fav(self, id, method='POST'):
        query = "DELETE FROM myfavs WHERE id=:id"
        values = {"id":id}
        return self.db.query_db(query, values)

    def get_one_quote(self, id):
        query = "SELECT * FROM quotes WHERE id=:id"
        data = {"id":id}
        return self.db.query_db(query, data)

    def paste_quote_to_fav(self, one_fav):
        query = "INSERT INTO myfavs (name, quote, quoted_by) VALUES (:name, :quote, :quoted_by)"
        values = {
            'name': one_fav[0]['name'],
            'quote': one_fav[0]['quote'],
            'quoted_by': one_fav[0]['quoted_by']
        }
        return self.db.query_db(query, values)

    def get_profile(self, id):
        query = "SELECT name FROM quotes WHERE id=:id"
        values = {'id':id}
        return self.db.query_db(query, values)

    def show_indi_quotes(self, alias):
        query = "SELECT quote, quoted_by FROM quotes WHERE name=:name"
        values = {'name': alias}
        return self.db.query_db(query, values)


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