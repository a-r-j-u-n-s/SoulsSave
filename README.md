# Elden Ring Save Manager
_A save file manager for Elden Ring on Steam_

## _About_
This Python CLI allows you to manage your save files for Elden Ring

## _Usage_
There are two primary modes for this script to run in:

### restore
`python eldensave.py load`

`load` is for when you want to replace the current save file with one of your saved backups

### save
`python eldensave.py save`

`save` is for when you want to save your current savegame in a new backup

## Dependencies

[Python 3.8](https://www.python.org/downloads/release/python-380/)

[psutil 5.7.0](https://pypi.org/project/psutil/)


### Disclaimer
Although this CLI does create automatic backups of your save file before performing any actions, you should still
back up 