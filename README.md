# Neda Submission File Workaround

## Description
Tool made for automating 5 minutes of the monotonous activity when doing SQL homework for school...

## Usage
- Run `python -m pip install -r requirements.txt` to install all dependencies
- Use `python nedaSFW.py --help` to see the help message

## Database config
Script reads the configuration from file `db_config.json` in a working directory if flag `--db` (`-d`) is set and if not, user is prompted to enter credentials and `db_config.json` will be created in the working directory.

`db_config.json`:
```json
{
    "host": "HOST",
    "user": "USER",
    "password": "USER_PASSWORD",
    "database": "DATABASE"
}
```

## Project config
If `--projectConfig` (`-p`) flag is omitted user will be prompted to enter title, author and date values which will be used for LaTeX and will be saved in `proj_config.json`. When `-p` flag is used script looks for `proj_config.json` file in the working directory.

`proj_config.json`:
```json
{
    "title": "TITLE",
    "date": "DECEMBER 2020",
    "author": "YOUR NAME"
}
```

## SQL file rules
Above every query there **must** be exactly one line of comment which will be used as a section heading in LaTeX file.

Example:
```SQL
# Commend used as heading
SELECT * FROM example
WHERE something = 'test';

# Commment used as heading
SELECT some_column FROM example;
```

## Adding script to PATH on Windows
Create a directory somwhere on your computer and copy `nedaSFW.bat` there. In `nedaSFW.bat` change 
```
{PUT YOUR SCRIPT (nedSFW.py) PATH HERE}
```
with path to `src/nedaSFW.py` script on your computer.
Finally, edit PATH environmental variable and add folder containing `nedaSFW.bat`. Now script can be used by calling `nedaSFW` from cmd or Powershell from any directory.

## Adding script to PATH on Linux
Add cloned folder to your path by appending to your `.bashrc` the following:
```
export PATH=$PATH:<path/to/nedaSFW>
```

Script is now executable from everywhere on the system by executing `nedaSFW`.

## Compile to .pdf when generating .tex
If `--compilePDF` (`-c`) flag is used when running `generate` command and `pdflatex` is installed .pdf will be generated.

## Usage example
**-t option in generate command still not *(completely)* usable**

Generate .tex output, `db_config.json` and `proj_config.json`
```
nedaSFW generate -s sqlFile.sql -o texFile.tex
```

Generate .tex output and use already created `db_config.json` and `proj_config.json`
```
nedaSFW generate -s sqlFile.sql -o texFile.tex -d -p
```

Same as above, but .pdf is also generated
```
nedaSFW generate -s sqlFile.sql -o texFile.tex -d -p -c
```
