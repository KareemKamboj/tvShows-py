from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import shows_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__ (self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod 
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(DATABASE).query_db(query, data) 

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users JOIN shows on users.id = shows.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        list_of_shows = []
        for row in results:
            if row['shows.id'] == None:
                break
            show_data = {
                **row,
                'id': row['shows.id'],
                'created_at': row['shows.created_at'],
                'updated_at': row['shows.updated_at']            
            }
            this_show = shows_model.Show(show_data)
            list_of_shows.append(this_show)
        user.shows = list_of_shows
        return user

    @staticmethod
    def validate(user_data):
        is_valid = True
        if len(user_data['first_name']) < 1:
            flash("First name is required", "reg")
            is_valid = False
        if len(user_data['last_name']) < 1:
            flash("Last name is required", "reg")
            is_valid = False
        if len(user_data['email']) < 1:
            flash("Name is email", "reg")
            is_valid = False
        elif not EMAIL_REGEX.match(user_data['email']):
            flash("Inavalid email format", "reg")
            is_valid = False
        else:
            data = {
                'email':user_data['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                flash("email already registered", "reg")
                is_valid = False
        if len(user_data['password']) < 8:
            flash("Password needs to be atleast 8 characters", "reg")
            is_valid = False
        elif not user_data['password']== user_data['confirm_pass']:
            flash("passwords don't match", "reg")
            is_valid = False
        return is_valid