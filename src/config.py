import configparser
from pathlib import Path
import typer
from src import (
    DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__
)
CONFIG_DIR_PATH = Path(".")#typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

def init_app(db_path: str)->int:
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    
    database_code = _create_database(db_path)
    if database_code != SUCCESS:
        return database_code

    return SUCCESS

def _init_config_file() -> int:
    print(f"THE PATH IS {CONFIG_DIR_PATH}")
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
        print("Created folder")
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
        
        print("Created file")
    except OSError:
        return FILE_ERROR
    return SUCCESS

def _create_database(db_path:str)->int:
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS

def retrieve_config_value(key:str)->str:
    config_parser = configparser.ConfigParser()
    config_parser.read(CONFIG_FILE_PATH)
    return config_parser["General"][key]