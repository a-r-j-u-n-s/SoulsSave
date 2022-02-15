# EldenSave
_A save file manager for Elden Ring on Steam_

## _About_
This Python CLI allows you to manage your save files for Elden Ring.

Primary features:
- _Create multiple labeled backups of your savegame with custom names/descriptions for reference_
- _Create/restore from a temporary unlabeled backup save_
- 

## _Usage_

There are three modes for this script to run in:

### load
`python eldensave.py [-l] [-c] load [-b] [savename]`

- For when you want to replace the current save file with one of your saved backups


_Optional_:

`-b, --backup`  : restore your temporary backup save


### save
`python eldensave.py [-l] [-c] save [-b] [savename]`

- For when you want to save your current savegame in a new backup

_Optional_:

`-b, --backup`  : store your current savegame as a temporary backup that you can easily restore from

### delete
`python eldensave.py [-l] [-c] delete [savenames...]`

- For when you want to delete one or more of your backups
- Leave `[savenames...]` blank to see the list of saves before choosing what to delete

_Options_:

`[savenames]`: a list of your custom saves to delete 

## Dependencies

[Python 3.8](https://www.python.org/downloads/release/python-380/)

[psutil 5.7.0](https://pypi.org/project/psutil/)


### Disclaimer
Although this CLI does create automatic backups of your save file before performing any actions, you should still
back up 