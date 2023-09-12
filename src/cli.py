from pathlib import Path
from typing import Optional, List
import typer
from src import __app_name__, __version__, config, database, ERRORS, models
from src.utils.Logger import Logger
import traceback

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        database.DEFAULT_DB_FILE_PATH,
        "--db-path",
        "-db",
        prompt="Name of database file? (Empty for default)"
    ),
)->None:
    """Creates config.ini file and database"""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        message = str(f'Creating config file failed with "{ERRORS[app_init_error]}"')
        typer.secho(
            message,
            fg=typer.colors.RED
        )
        Logger.add_to_log("error",message)
        raise typer.Exit(1)
    
    Logger.add_to_log("info","Successfully created config.ini file")

    db_init_error = database.db.init_database(Path(db_path))
    
    if db_init_error:
        message = str(f"Creating database failed with '{ERRORS[db_init_error]}'")
        typer.secho(message, fg=typer.colors.RED)
        Logger.add_to_log("error",traceback.format_exc())
    else:
        message = str(f"Created database at: {db_path}")
        typer.secho(message, fg=typer.colors.GREEN)
        Logger.add_to_log("info",message)

def get_controller() -> models.UserModel.UserController:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.db.get_database_path()
    else:
        typer.secho(
            'Config file not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return models.UserModel.UserController(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "rptodo init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
    name: List[str]=typer.Argument(...),
    age: int= typer.Option(..., "---age","-p", min=1, max=199),
    username: str =typer.Option(...,"--username", "-u")
) -> None:
    usercontroller= get_controller()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        Logger.add_to_log("info", "Checked cli version with --version")
        raise typer.Exit()
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, 
        "--version",
        "-v",
        help="Shows version and exits", 
        callback=_version_callback,
        is_eager=True))->None:    
    return