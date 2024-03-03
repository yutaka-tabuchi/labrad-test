
import labrad
import labrad.server
import labrad.devices
import twisted
#from labrad                 import types as T, util
#from labrad.units           import Value

class helloLabrad( labrad.devices.DeviceServer ):

  name = 'hello_labrad' # Service name to be informed

  @twisted.internet.defer.inlineCallbacks
  def initServer(self):
    yield labrad.devices.DeviceServer.initServer(self)

  def initContext(self, c):
    labrad.devices.DeviceServer.initContext(self,c)
    c['shared_variable_for_connection'] = dict()

  @labrad.server.setting( 100, 'Hello', returns = ['s'] )
  def service_hello(self,c):
    """
      This method returns Hello Labrad
    """
                                                            # *  Twisted allow to insert other task in the service
    ans0 = yield 0                                          # create generator here
                                                            # *  Twisted allow to insert other task in the service
    ans1 = yield 1                                          # create generator here
    twisted.internet.defer.returnValue( 'Hello Labrad {0}/{1}'.format( ans0, ans1 ))

  @labrad.server.setting( 101, 'Hello_without_threading', returns = ['s'] )
  def service_hello_without_threading(self,c):
    """
      This method returns Hello Labrad
    """
    return 'Hello Labrad'

  
if __name__ == '__main__':

  __server__ = helloLabrad()
  labrad.util.runServer( __server__ )

