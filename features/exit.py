from features import addFeature
import sys

class ExitCommand:
  command = 'exit'

  def run(arguments, implant):
    sys.exit(0)

  def help():
    return 'exits the application'
    


addFeature(ExitCommand)
