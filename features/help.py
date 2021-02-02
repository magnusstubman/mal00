from features import *
import sys

class HelpCommand:
  command = 'help'

  def run(arguments, implant):
    global features
    for feature in features:
      if not hasattr(feature, 'hide'):
        print('  ' + feature.command + '\t\t' + feature.help())

  def help():
    return 'shows this message'
    
addFeature(HelpCommand)
