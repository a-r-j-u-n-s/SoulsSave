# Elden Ring Save Manager
_A save file manager for Elden Ring on Steam_

## _About_
This Python CLI allows you to manage your save files for Elden Ring

## _Usage_

#### Optional flags

-l : display all your current saves

-c : indicate that you want to script to use your custom savegame location (i.e. not its default installed location)

There are _three_ primary modes for this script to run in:

### load
`python eldensave.py [-l] [-c] load [savename]`

`load` is for when you want to replace the current save file with one of your saved backups.


### save
`python eldensave.py [-l] [-c] save [savename]`

`save` is for when you want to save your current savegame in a new backup

### delete
`python eldensave.py [-l] [-c] delete [savenames...]`

`delete` is for when you want to delete one or more of your backups

## Dependencies

[Python 3.8](https://www.python.org/downloads/release/python-380/)

[psutil 5.7.0](https://pypi.org/project/psutil/)


### Disclaimer
Although this CLI does create automatic backups of your save file before performing any actions, you should still
back up 
