import mysql.connector
from mysql.connector import errorcode
import config
import click
from os import path, getcwd
from pyfiglet import Figlet
from db import DatabaseConnection
from latex import LatexCreator

defaultTemplatePath = path.normpath(path.join(path.realpath(__file__), '../../tex_template/template.tex'))

@click.group()
def main():
    """
    Neda Submission File Workaround - NSFW
    """
    pass

@main.command()
def about():
    """
    Info about this tool
    """
    f = Figlet(font="doom")
    click.secho(f.renderText("NedaSFW"), nl=False)
    click.secho("Neda Submission File Workaround - NedaSFW")
    click.secho("Executes SQL queries from .sql file and creates")
    click.secho(".tex file containing results and queries.\n")
    click.secho("Author: Aleksa Prtenjača")
    click.secho("Github: www.github.com/Prki42\n")

@main.command()
@click.option('--sql', '-s', required=True, help="SQL file to use")
@click.option('--temp', '-t', required=False, help="Custom LaTeX template")
@click.option('--output', '-o', required=True, help="File to output LaTeX code")
@click.option('--db', '-d', type=bool, default=False, is_flag=True, required=False, help="Use existing database config file")
def generate(sql, temp, output, db):
    """
    Generates LaTeX file
    """
    templateFilePath = defaultTemplatePath
    dbConfig = None
    if not temp:
        if not path.exists(defaultTemplatePath):
            click.secho("Default template doesn't exist")
            return
    elif not path.exists(temp):
        click.secho("Template file doesn't exist")
        return

    if not path.exists(sql):
        click.secho("SQL file doesn't exist")
        return

    if db:
        if not path.exists('db_config.json'):
            click.secho("There is no db_config.json in current directory")
            return
        dbConfig = config.readConfig("db_config.json")
    else:
        dbConfig = config.createDatabaseConfig("db_config.json")
    
    try:
        mysqldb = DatabaseConnection(dbConfig)
        print("[+] Connected to database")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Bad credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        else:
            print(err)
        return
    
    try:
        latexWriter = LatexCreator(mysqldb, sql, templateFilePath, output)
        codeWrap = "\\begin{sqlCode}\n%s\n\\end{sqlCode}\n"
        latexWriter.write(codeWrap, "...template...")
        print("[+] Successfully written data to %s" % (output))
    except Exception as e:
        print(e)
    try: mysqldb.kill()
    except : pass
    

if __name__ == '__main__':
    main()