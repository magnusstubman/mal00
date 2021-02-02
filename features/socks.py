from features import addFeature

class SocksCommand:
  command = 'socks'
  hide = True

  def run(arguments, implant):
    pass

  def help():
    return 'start/stop socks5 tunnel. Usage: socks (<local port>|stop)'


addFeature(SocksCommand)
