import mysql.connector
from mysql.connector import errorcode
import config
import click
from os import path, getcwd
import subprocess
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
    click.secho("Author: Aleksa Prtenjača \u00A9")
    click.secho("Github: www.github.com/Prki42\n")

@main.command()
@click.option('--sql', '-s', required=True, help="SQL file to use")
@click.option('--temp', '-t', required=False, help="Custom LaTeX template")
@click.option('--output', '-o', required=True, help="File to output LaTeX code")
@click.option('--db', '-d', type=bool, default=False, is_flag=True, required=False, help="Use existing database config file")
@click.option('--projectConfig', '-p', type=bool, default=False, is_flag=True, required=False, help="Use existing project config")
@click.option('--compilePDF', '-c', type=bool, default=False, is_flag=True, required=False, help="Compile to pdf using 'pdflatex'")
def generate(sql, temp, output, db, projectconfig, compilepdf):
    """
    Generates LaTeX file
    """
    templateFilePath = defaultTemplatePath
    dbConfig = None
    projConfig = None

    #TODO Can't be used rn except it follows the same rules as example template... Fix???
    if not temp:
        if not path.exists(defaultTemplatePath):
            click.secho("[-] Default template doesn't exist")
            return
    elif not path.exists(temp):
        click.secho("[-] Template file doesn't exist")
        return

    if not path.exists(sql):
        click.secho("[-] SQL file doesn't exist")
        return

    output = output.replace("\\", "/")

    #TODO Database config and project config handling is copy-paste, refactor...

    # Handling database config
    if db:
        if not path.exists('db_config.json'):
            click.secho("[-] There is no db_config.json in current directory")
            return
        dbConfig = config.readConfig("db_config.json", config.validateDatabaseConfig)
    else:
        dbConfig = config.createDatabaseConfig("db_config.json")

    # Handling project config
    if projectconfig:
        if not path.exists('proj_config.json'):
            click.secho("[-] There is no proj_config.json in current directory")
            return
        projConfig = config.readConfig("proj_config.json", config.validateProjectConfig)
    else:
        projConfig = config.createProjectConfig("proj_config.json")
    
    try:
        mysqldb = DatabaseConnection(dbConfig)
        click.secho("[+] Connected to database")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            click.secho("[-] Bad credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            click.secho("[-] Database doesn't exist")
        else:
            print("\tError:", err)
        return
    
    try:
        latexWriter = LatexCreator(mysqldb, sql, templateFilePath, output, projConfig)
        codeWrap = "\\begin{sqlCode}\n%s\n\\end{sqlCode}\n"
        latexWriter.write(codeWrap, "...template...")
        print("[+] Successfully written data to %s" % (output))
        if compilepdf:
            # OSError will be raised if called command in Popen is not available
            try:
                pdfOutput = "/".join(output.split("/")[:-1])
                if pdfOutput.strip() == "" : pdfOutput = "."
                compileProcess = subprocess.Popen(["pdflatex", "-interaction=nonstopmode", "-output-directory", pdfOutput, output], shell=False, stdout=subprocess.DEVNULL)
                compileProcess.wait()
                # Code 0 means success
                if compileProcess.returncode == 0:
                    click.secho("[+] Successfully compiled to PDF")
                else:
                    click.secho("[-] Failed to compile to PDF")
            except OSError as err:
                click.secho("[-] Command 'pdflatex' not found")
                print("\tError:", err)
    except Exception as e:
        print("\tError:", e)
    try: mysqldb.kill()
    except : pass
    

if __name__ == '__main__':
    main()