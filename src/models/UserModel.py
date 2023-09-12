from pathlib import Path
from typing import Any, Dict, NamedTuple, List

from src.database.db import DatabaseHandler
from src import DB_READ_ERROR


class User(NamedTuple):
    user: Dict[str,Any]
    error:int
    
class UserController:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
    
    def add(self, name: List[str], age: int, username: str) -> User:
        """Adds new user to database"""
        name_text = " ".join(name)
        user = {
            "name": name_text,
            "age": age,
            "username": username
        }
        read = self._db_handler.read_users()
        if(read.error == DB_READ_ERROR):
            return User(user, read.error)
        read.user_list.append(user)
        write = self._db_handler.write_users(read.user_list)
        return User(user, write.error)
    # def __init__(self, id, username, password, fullname) -> None:
    #     self.id = id
    #     self.username = username
    #     self.password = password
    #     self.fullname = fullname


    # def to_json(self):
    #     return {
    #         'id': self.id,
    #         'username': self.username,
    #         'fullname': self.fullname
    #     }