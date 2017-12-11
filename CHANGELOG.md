## v1.0.0

- Switched to semantic versioning.
- Beginning to work on the issues pointed out by Spindel.

## 081217 - 1812
- Fixed the api (again, missed out a parameter).
- Api should now ONLY return the results for, say generation index is set to 6, it will only return gen 6 and below.
- Basically dont set your offset too high or it's going to take forever to pull the API.
- Switched to Relative pathing.
- Renamed the github screenshot folder to make it less confusing.


## 081217 - 1427
- Added individual usage.
- I reccomend that you disable the group repeating job if you enable individual repeating.
- Requires mysql db.
- Script for db structure provided.
- You'll need to modify the code and tokens accordingly.
- Updated API to include generation parameters to narrow the number of results per page

## 071217 - 2140

- Added image support
- I need some help with exception handling in commands.py, appreciate help if anyone can read the comments there.
- cant seem to catch the socket timing out exception there.
- wand and imagemagick are required for images.

## 071217 - 1130

- Rewrote code to make it easier for users to customize after vice linked to this bot
- Removed image because its buggy at the moment.
- Fixed the cat api being changed at 5am this morning for the cattributes again
