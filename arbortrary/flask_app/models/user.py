from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL("arbortrary").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user"
        result = connectToMySQL("arbortrary").query_db(query)
        user = []
        for row in result:
            user.append(cls(row))
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL("arbortrary").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL("arbortrary").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE user SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id=%(id)s;"
        return connectToMySQL("arbortrary").query_db(query, data)

    @classmethod
    def delete(cls, user_id):
        query = "DELETE FROM user WHERE id = %(id)s;"
        return connectToMySQL("arbortrary").query_db(query, data)

    @classmethod
    def user_trees(cls, data):
        query = "SELECT * FROM user LEFT JOIN tree ON user.id = tree.user_id WHERE user.id = %(id)s;"
        results = connectToMySQL("arbortrary").query_db(query, data)
        user = cls(results[0])
        for row in results:
            tree_data = {
                "id": row["tree.id"],
                "species": row["species"],
                "location": row["location"],
                "reason": row["reason"],
                "date_planted": row["date_planted"],
                "created_at": row["tree.created_at"],
                "updated_at": row["tree.updated_at"],
                "user_id": row["user_id"],
            }
            user.tree.append(tree.Tree(tree_data))
            return user

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL("arbortrary").query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email!!", "register")
            is_valid = False
        if len(user["first_name"]) < 3:
            flash("First Name must be at least 3 characters.", "register")
            is_valid = False
        if len(user["last_name"]) < 3:
            flash("Last Name must be at least 3 characters.", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if user["password"] != user["confirm"]:
            flash("Passwords don't match", "register")
        return is_valid
