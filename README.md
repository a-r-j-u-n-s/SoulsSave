# SaveGame
_A save manager for PC games_

## _About_
This Python CLI allows you to manage your save folders for PC games.

Primary features:
- _Create multiple labeled backups of your savegame with custom names/descriptions for reference_
- _Create/restore from a temporary unlabeled backup save_
- _Add/delete your custom saves easily_

## _Usage_

There are three modes for this script to run in:

#### Optional flags

`-l`: display all your current saves

`-c`: indicate that you want to script to use your custom savegame location (i.e. not its default installed location)

**There are _three_ primary modes for this script to run in:**

### load
`python eldensave.py [-l] [-c] load [-b] [savename]`

- For when you want to replace the current save file with one of your saved backups

_Optional_:

`-b, --backup`  : restore your temporary backup save

`savename`: the name of the save you want to restore. Leave blank to be prompted after seeing the current list of saves

### save
`python eldensave.py [-l] [-c] save [-b] [savename]`

- For when you want to save your current savegame in a new backup

_Optional_:

`-b, --backup`  : store your current savegame as a temporary backup that you can easily restore from

`savename`: the name of your custom save. Leave blank to be prompted after seeing the current list of saves

### remove
`python eldensave.py [-l] [-c] remove [savenames...]`

- For when you want to delete one or more of your backups

_Optional_:

`savenames`: a list of your custom saves to delete. Leave blank to choose which save to delete after seeing the list

## Dependencies

* **This program is is only supported for Windows 10**

[Python 3.8](https://www.python.org/downloads/release/python-380/)

[psutil 5.7.0](https://pypi.org/project/psutil/)

## _Current Tasks_
Version: 1.0
- Configure script to work with multiple games!


### Disclaimer
Although this CLI does create automatic backups of your save file before performing any actions, you should still
back up your original save folder just once before using the script
