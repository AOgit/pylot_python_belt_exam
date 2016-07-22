"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        """
        This is an example of loading a model.
        Every controller has access to the load_model method.
        """
        self.load_model('User')
        self.load_model('Quote')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):
        """
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_users()
        
        self.models['WelcomeModel'].add_message()
        # messages = self.models['WelcomeModel'].grab_messages()
        # user = self.models['WelcomeModel'].get_user()
        # to pass information on to a view it's the same as it was with Flask
        
        # return self.load_view('index.html', messages=messages, user=user)
        """
        return self.load_view('users/index.html')

    def create(self):
        user_info = {
            'name': request.form['name'],
            'alias': request.form['alias'],
            'email': request.form['email'],
            'password': request.form['password'],
            'p_con': request.form['p_con'],
            'birthdate': request.form['birthdate']
        }

        create_status = self.models['User'].create_user(user_info)
        
        if create_status['status'] == True:
            flash('Success!! You may now log in.')
            return redirect('/')
        else:
            for message in create_status['errors']:
                flash(message)
            return redirect('/')           

    def login(self):
        session['email'] = request.form['email']
        user_info = {
            'email': session['email'],
            'password': request.form['password']
        }

        login_status = self.models['User'].login_user(user_info)

        if login_status == True:
            # return self.load_view('books_home.html', name=alias[0]['alias'])
            return redirect('/home')
        else:
            flash('Access denied')
            return redirect('/')

    def show(self):
        all_quotes = self.models['Quote'].show_all_quotes()
        all_favs = self.models['Quote'].show_favorites()
        email_info = {
            'email': session['email']
        }
        name = self.models['User'].get_alias(email_info)
        return self.load_view('/quotes/home.html', all_quotes=all_quotes, my_favorites=all_favs, name=name[0]['alias'])

    def create_quote(self):
        b = request.form
        email_info = {
            'email': session['email']
        }
        name = self.models['User'].get_alias(email_info)
        alias = name[0]['alias']
        self.models['Quote'].create(b, alias)
        return redirect('/home')

    def remove_fav(self, id):
        self.models['Quote'].delete_fav(id)
        return redirect('/home')

    def get_fav(self, id):
        one_fav = self.models['Quote'].get_one_quote(id)
        self.models['Quote'].paste_quote_to_fav(one_fav)
        return redirect('/home')

    def show_profile(self, id):
        name = self.models['Quote'].get_profile(id)
        email_info = {
            'email': session['email']
        }
        bb = self.models['User'].get_alias(email_info)
        alias = bb[0]['alias']
        quotes = self.models['Quote'].show_indi_quotes(alias)
        return self.load_view('/quotes/profile.html', name=name[0]['name'], quotes=quotes)

    def logout(self):
        session.clear()
        return redirect('/')

