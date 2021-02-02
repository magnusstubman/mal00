import messages

class ShellCommandMessage(object):
  name = 'shellcommand'
  command = None
  
  def __init__(self, command):
    self.command = command

  def getBuf(self):
    return messages.Message(self.name, bytes(self.command, 'ascii')).toBuf()
     
