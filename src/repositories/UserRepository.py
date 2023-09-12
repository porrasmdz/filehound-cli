from pathlib import Path
from typing import Dict, List

from src import DB_READ_ERROR, ID_ERROR
from src.database.db import DatabaseHandler
from src.models.UserModel import User

class UserRepository:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    
    def get_all_users(self) -> List[Dict[str,any]]:
        """Return the current users list"""
        read = self._db_handler.read_model("users")
        return read.model_list
    
    def add(self, name: List[str], age: int, username: str) -> User:
        """Adds new user to database"""
        name_text = " ".join(name)
        user = {
            "name": name_text,
            "age": age,
            "username": username
        }
        read = self._db_handler.read_model("users")
        if(read.error == DB_READ_ERROR):
            return User(user, read.error)
        read.model_list.append(user)
        write = self._db_handler.write_model("users",read.model_list)
        return User(user, write.error)
    
    def get_user(self, user_id: int)-> User:
        read = self._db_handler.read_model("users")
        try: 
            user = read.model_list[user_id - 1]
            return User(user, read.error)
        except IndexError:
            return User({}, ID_ERROR)

    def update(self,user_id:int, username: str, name: List[str]=None, age:int=None)-> User:
        """Updates an existing user"""
        read = self._db_handler.read_model("users")
        if read.error:
            return User({}, read.error)
        try:
            user = read.model_list[user_id - 1]
        except IndexError:
            return User({}, ID_ERROR)
        if(username is not None):
            user['username'] = username
        if(name is not None and len(name) > 0):
            name_text = " ".join(name)
            user['name'] = name_text
        if(age is not None):
            user['age'] = age
        write = self._db_handler.write_model("users",read.model_list)
        return User(user, write.error)
        
    def remove(self, user_id:int)->User:
        """Remove an user from the database with index""" 
        read = self._db_handler.read_model("users")
        if read.error:
            return User({}, read.error)
        try:    
            user = read.model_list.pop(user_id-1)
        except IndexError:
            return User({}, ID_ERROR)
        write = self._db_handler.write_model("users", read.model_list)
        return User(user, write.error)
        