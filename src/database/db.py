import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from src import DB_WRITE_ERROR, SUCCESS, config, JSON_ERROR, DB_READ_ERROR

def get_database_path()->Path:
    return Path(config.retrieve_config_value("database"))

def init_database(db_path:Path)-> int:
    """Creates database."""
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    user_list: List[Dict[str, Any]]
    error: int

#Careful
class DatabaseHandler: 
    def __init__(self, db_path: Path) -> None:
        self._db_path=db_path
    
    def read_users(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)
        

    def write_users(self, user_list: List[Dict[str,Any]])-> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(user_list,db, indent=4)
            return DBResponse(user_list, SUCCESS)
        except OSError: 
            return DBResponse(user_list, DB_WRITE_ERROR)