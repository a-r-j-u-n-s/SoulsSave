@echo off
"python" ".\src\savegame\__main__.py" %*

@REM issue: %~dp0 ends up making 'savegame' corresponding to the venv scripts directory, making the absolute path not work
@REM         . ends up using the current directory we are in, which only works if we are calling the script from the project directory
@REM         need to find a solution that covers all cases (try importing all of src code?)