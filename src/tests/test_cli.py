import json

import pytest
from typer.testing import CliRunner

from src import __app_name__, __version__, cli, models,DB_READ_ERROR, SUCCESS
from src.repositories.UserRepository import UserRepository

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    mock_database = {
        "users": [{"name": "Johan Silva", "age": 21, "username": "jsilva"}]
        }
    db_file = tmp_path / "user.json"
    with db_file.open("w") as db:
        json.dump(mock_database, db, indent=4)
    return db_file

test_data1 = {
    "name": ["Jorge", "de", "Castro"],
    "age": 23,
    "username":"jdecastro",
    "user": {
        "name": "Jorge de Castro",
        "age": 23,
        "username": "jdecastro",
    },
}

test_data2 = {
    "name": ["Arianna Silva"],
    "age": 24,
    "username": "asilva",
    "user": {
        "name": "Arianna Silva",
        "age": 24,
        "username": "asilva",
    },
}

@pytest.mark.parametrize(
    "name, age, username, expected",
    [
        pytest.param(
            test_data1["name"],
            test_data1["age"],
            test_data1["username"],
            (test_data1["user"], SUCCESS),
        ),
        pytest.param(
            test_data2["name"],
            test_data2["age"],
            test_data2["username"],
            (test_data2["user"], SUCCESS),
        ),
    ],
)

def test_add(mock_json_file, name, age, username,expected):
    user_repository = UserRepository(mock_json_file)
    assert user_repository.add(name, age, username) == expected
    read = user_repository._db_handler.read_model("users")
    assert len(read.model_list) == 2