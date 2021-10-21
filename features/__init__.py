from lib import implants
from lib import globals

global features
features = []

def addFeature(feature):
  features.append(feature)

def run(command, arguments):
  for feature in features:
    if not hasattr(feature, 'hide'):
      if feature.command == command:
        feature.run(arguments, implants.currentImplant)
        globals.lastCommand = command
        return
  print('command not found.')

def parseCommand(s):
  if ' ' in s:
    parts = s.split(' ')
    run(parts[0], parts[1:])
  else:
    run(s, None)

def getFeatureByName(name):
  global features
  for feature in features:
    if feature.command == name:
      return feature
    

from features import help 
#from features import info 
from features import list 
from features import use 
#from features import shell
from features import eval 
from features import evalshell
from features import executeglobal
from features import executeglobalfile
from features import upload
#from features import socks
from features import kill
from features import sleep
from features import exit 

print('loaded ' + str(len(features)) + ' commands.')
