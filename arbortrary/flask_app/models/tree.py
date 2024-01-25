from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Tree:
    def __init__(self, data):
        self.id = data["id"]
        self.species = data["species"]
        self.location = data["location"]
        self.reason = data["reason"]
        self.date_planted = data["date_planted"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO tree (species, location, reason, date_planted, user_id) VALUES(%(species)s,%(location)s,%(reason)s,%(date_planted)s, %(user_id)s);"
        return connectToMySQL("arbortrary").query_db(query, data)

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM tree"
        result = connectToMySQL("arbortrary").query_db(query, data)
        user = []
        for row in result:
            user.append(cls(row))
        return user

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tree WHERE id = %(id)s;"
        results = connectToMySQL("arbortrary").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE tree SET species=%(species)s, location=%(location)s, reason=%(reason)s, date_planted=%(date_planted)s WHERE id=%(id)s;"
        return connectToMySQL("arbortrary").query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM tree WHERE id = %(id)s;"
        return connectToMySQL("arbortrary").query_db(query, data)
