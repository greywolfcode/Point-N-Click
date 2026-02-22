#import standard libraries
import os
import zipfile

#import packagers
from . import elementPackager #have to import from . ore it doesn't worjk

class Level():
    '''Storage for level data transfer'''
    def __init__(self, layout, triggers, cutscenes):
        self.layout = layout
        self.triggers = triggers
        self.cutscenes = cutscenes
    def getLayout(self):
        return self.layout
    def getTriggers(self):
        return self.triggers
    def getCutscenes(self):
        return self.cutscenes
    
def packageLevel(level, path):
    #package required data
    layout = elementPackager.exportLevelLayout(level.getLayout())
    #enforce file extension
    if (path[-7:] != ".mission"):
        path = path + ".mission"
    #write data to file
    with zipfile.ZipFile(path, "w") as file:
        #add directories to zip
        file.mkdir("triggers")
        file.mkdir("cutscenes")
        #add data to zip
        file.writestr("layout.xml", layout)

        triggers = level.getTriggers()
        for trigger in triggers:
            file.writestr(os.path.join("triggers", trigger + ".pncbas"), triggers[trigger])
        cutscenes = level.getCutscenes()
        for cutscene in cutscenes:
            file.writestr(os.path.join("triggers", cutscene + ".pncbas"), cutscenes[cutscene])

def loadLevel(path):
    with zipfile.ZipFile(path) as zip:
        files = zip.namelist()
        #read layout
        files.remove("layout.xml")
        with zip.open("layout.xml", "r") as file:
            layout = elementPackager.loadLevelLayout(file.read())
        #read everything in subfolders
        triggers = []
        cutscenes = []
        for fileName in files:
            if "triggers" in fileName:
                with zip.open(fileName, "r") as file:
                    triggers.append(file.read())
            elif "cutscenes" in fileName:
                with zip.open(fileName, "r") as file:
                    cutscenes.append(file.read())
    #create level object and return
    return Level(layout, triggers, cutscenes)
        