from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "login_and_registration"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            user_from_db = results[0]
            return cls(user_from_db)
        else:
            return False
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            user_from_db = results[0]
            return cls(user_from_db)
        else:
            return False

    @staticmethod
    def is_valid(user_dict):
        is_valid = True
        if len(user_dict["first_name"]) < 2:
            is_valid = False
            flash("First name should have at least 2 characters")
        if len(user_dict["last_name"]) < 2:
            is_valid = False
            flash("Last name should have at least 2 characters")
        if len(user_dict["email"]) < 2:
            is_valid = False
            flash("Email should have at least 2 characters")
        if not EMAIL_REGEX.match(user_dict['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user_dict["password"]) < 5:
            is_valid = False
            flash("Password must have at least 5 charcters")
        if user_dict["password_confirmation"] != user_dict["password"]:
            is_valid = False
            flash("Password must match password confirmation")
        return is_valid