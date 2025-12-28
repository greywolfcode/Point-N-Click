# Mission and Story file formats

Point n' CLick's  Editor has two wile formats for storing playable files. Stories are full "campaigns", which have multiple "missions" as a part, although .mission files can be played on their own. For example, the main single player story will be stored in a .story file. This document will detial how the .story and .mission file formats are made. Both these files will be secretly .zip files.

## Story files (.story)

(NAME).story
|
|-info.json
|-order.json
|
|-mission1.mission
|-mission2.mission
|-missionn.mission
|

### info.json

info.json stores metadata about the story: author, date created, date exported, etc.

### order.json

order.json stores the order of each mission.

## Mission files (.mission)

(NAME).mission
|
|-layout.json
|-triggers.json
|-cutscenes
  |-cutscene1.json
  |-cutscene2.json
  |-cutscenen.json
|

### layout.json

layout.json stores the layout of the map.

### triggers.json

triggers.json stores all the code for the triggers.

### cutscenes

The cutscenes folder stores all cutscenes that will be activated by triggers. The .json files inside store dialoge, map elements to move, cursor position, and settings for every cutscene.