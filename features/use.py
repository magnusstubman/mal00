from features import addFeature
from lib import implants

class UseCommand:
  command = 'use'

  def run(arguments, inf):
    if len(implants.implants) > 0:
      if not arguments or len(arguments) != 1:
        if not arguments:
          if implants.currentImplant == None:
            print('Usage: use implantname')
          else:
            implants.currentImplant = None
        else:
          print('Usage: use implantname')
      else:
        for i in implants.implants:
          if i.name == arguments[0]:
            implants.currentImplant = i
            return
        print('implant not found')
    else:
      print('no implants')

  def help():
    return 'change current implant. Usage: use implantname'
    
addFeature(UseCommand)
