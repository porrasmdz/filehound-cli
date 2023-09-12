
from typing import List
import typer
from src import __app_name__, __version__, config, database, ERRORS, models
from src.repositories.UserRepository import UserRepository
from src.utils.Logger import Logger

app = typer.Typer()

def get_repository() -> UserRepository:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.db.get_database_path()
    else:
        typer.secho(
            'Config file not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return UserRepository(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
    name: List[str]=typer.Argument(...),
    age: int= typer.Option(..., "--age","-a", min=1, max=199),
    username: str =typer.Option(...,"--username", "-u")
) -> None:
    repository= get_repository()
    user,error = repository.add(name, age, username)
    if error:
        message = str(f'Adding to-do failed with "{ERRORS[error]}"')
        typer.secho(
            message, fg=typer.colors.RED
        )
        Logger.add_to_log("error", message)
        raise typer.Exit(1)
    else:
        message = str(f"""User: "{user['name']}" was added """
            f"""with username: {user['username']}""")
        typer.secho(message ,
            fg=typer.colors.GREEN,
        )
        Logger.add_to_log("info", message)

@app.command()
def update(
    id: int =typer.Argument(...),
    username: str =typer.Option(None,"--username", "-u"),
    name: List[str]=typer.Option(None, "--name", "-n"),
    age: int= typer.Option(None, "--age","-a", min=1, max=199),
    ) -> None:
    repository= get_repository()
    user, error = repository.update(user_id=id,username=username,name=name,age=age)
    error = 0 #,error = repository.update(username, name, age)
    if error:
        message = str(f'Updating to-do failed with "{ERRORS[error]}"')
        typer.secho(
            message, fg=typer.colors.RED
        )
        Logger.add_to_log("error", message)
        raise typer.Exit(1)
    else:
        message = str(f"""User: "{user['username']}" was updated """
            f"""with id: {id}""")
        typer.secho(message ,
            fg=typer.colors.GREEN,
        )
        Logger.add_to_log("info", message)

@app.command()
def remove( 
    user_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation.",
    ),):
    """Remove using ID"""
    user_repository = get_repository()
    def _remove():
        user, error = user_repository.remove(user_id)
        if(error):
            message = str( f'Removing user # {user_id} failed with "{ERRORS[error]}"')
            typer.secho(message, fg=typer.colors.RED)
            raise typer.Exit(1)
        else:
            message = str(f"""User # {user_id}: '{user["username"]}' was removed""")
            typer.secho(message, fg=typer.colors.GREEN)
    if force:
        _remove()
    else:
        user, error = user_repository.get_user(user_id)
        if error:
            message = "Invalid USER_ID"
            typer.secho(message, fg=typer.colors.RED)
            raise typer.Exit(1)
        
        delete = typer.confirm(
            f"Delete user # {user_id}: {user['username']}?"
        )
        if(delete):
            _remove()
        else:
            typer.echo("Operation canceled")

@app.command(name="list")
def list_all()-> None:
    """List all users"""
    user_repository = get_repository()
    user_list = user_repository.get_all_users()
    if(len(user_list) == 0):
        message = "There are no tasks in the users list yet"
        typer.secho(message=message, fg=typer.colors.RED)
        raise typer.Exit()
    typer.secho("\nUser List\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.    ",
        "|  Age  ",
        "|  Username  ",
        "|  Full Name  "
    )
    build_users_table(columns, user_list)

def build_users_table(header_cols, user_list):
    headers = "".join(header_cols)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(user_list, 1):
        desc, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(header_cols[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(header_cols[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(header_cols[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)
