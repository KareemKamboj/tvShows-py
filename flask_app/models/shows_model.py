from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model

class Show:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.date = data['date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod 
    def create(cls, data):
        query = "INSERT INTO shows (title, network, date, description, user_id) VALUES (%(title)s, %(network)s,  %(date)s, %(description)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows JOIN users on shows.user_id = users.id"
        results = connectToMySQL(DATABASE).query_db(query)
        if len(results) > 0:
            all_shows = []
            for row in results:
                this_show = cls(row)
                user_data = {
                    **row,
                    'id': row['user_id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_show.person = this_user
                all_shows.append(this_show)
            return all_shows
        return []

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM shows JOIN users on users.id = shows.user_id WHERE shows.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        this_show = cls(row)
        user_data = {
            **row,
            'id': row['user_id'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        person = user_model.User(user_data)
        this_show.person = person
        return this_show

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, date = %(date)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
        
    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['title']) < 1:
            flash("title required")
            is_valid = False
        if len(form_data['network']) < 1:
            flash('network required')
            is_valid = False
        if len(form_data['date']) < 1:
            flash("date required")
            is_valid = False
        if len(form_data['description']) < 1:
            flash("description required")
            is_valid = False
        return is_valid