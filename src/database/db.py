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
        json_sample = """
        {
            "users": []
        }"""
        db_path.write_text(json_sample)
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    model_list: List[Dict[str, Any]]
    error: int

#Careful
class DatabaseHandler: 
    def __init__(self, db_path: Path) -> None:
        self._db_path=db_path
    
    def read_all(self):
        try:
            with self._db_path.open("r") as db:
                try:
                    result = json.load(db)
                    return result
                except json.JSONDecodeError:
                    return None
        except OSError:
            return None
    
    def read_model(self, key:str) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    result = json.load(db)
                    result = result[key]
                    return DBResponse(result, SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)      
        
    def write_model(self, key:str, user_list: List[Dict[str,Any]])-> DBResponse:
        try:
            state = self.read_all()
            if (state is None):
                return DBResponse(user_list, DB_WRITE_ERROR)
            state[key] = user_list
            with self._db_path.open("w") as db:
                json.dump(state,db, indent=4)
            return DBResponse(user_list, SUCCESS)
        except OSError: 
            return DBResponse(user_list, DB_WRITE_ERROR)