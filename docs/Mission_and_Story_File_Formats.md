# Mission and Story file formats

Point n' Click's  Editor has two file formats for storing playable files. Stories are full "campaigns", which have multiple "missions" as a part, although .mission files can be played on their own. For example, the main single player story will be stored in a .story file. This document will detial how the .story and .mission file formats are made. Both these files will be secretly .zip files.

## Story files (.story)

```
(NAME).story
|
|-info.json
|-order.json
|
|-mission1.mission
|-mission2.mission
|-missionn.mission
|
```

### info.json

info.json stores metadata about the story: author, date created, date exported, etc.

### order.json

order.json stores the order of each mission.

## Mission files (.mission)

```
(NAME).mission
|
|-layout.xml
|-triggers
  |-trigger1.pncbas
  |-trigger2.pncbas
  |-triggerN.pncbas
|-cutscenes
  |-cutscene1.json
  |-cutscene2.json
  |-cutssceneN.json
|
```

### layout.xml

layout.xml stores the layout of the map. Each object on the map will be its own block

### triggers

The triggers folder stores all the trigger files for the mission. Triggers are written in Point n' Click Basic, and saved with the .pncbas file extension

### cutscenes

The cutscenes folder stores all cutscenes that will be activated by triggers. The .json files inside store dialoge, map elements to move, cursor position, and settings for every cutscene.
