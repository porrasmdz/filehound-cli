from pathlib import Path
from typing import Optional
import typer
from src import __app_name__, __version__, config, database, ERRORS
from src.utils.Logger import Logger
import traceback

#Commands
import src.commands.users as users_cmd
  
app = typer.Typer()
app.add_typer(users_cmd.app, name="users")

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

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        Logger.add_to_log("info", "Checked cli version with --version")
        raise typer.Exit()
    
    Logger.add_to_log("info", "Executed general command")
    
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