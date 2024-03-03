
import labrad
import labrad.server
import labrad.devices
import twisted

class hogehogeWrapper( labrad.devices.DeviceWrapper ):

  @twisted.internet.defer.inlineCallbacks
  def connect( self, *args, **kw ):

    name, _dummy, handle = args
    yield print( 'device hogehoge channel {} is connected.'.format( name ))

  @twisted.internet.defer.inlineCallbacks
  def hello_channel( self, repeat : int ):
    resp = yield 'hoge' * repeat
    twisted.internet.defer.returnValue( resp )


class fufufuWrapper( labrad.devices.DeviceWrapper ):
  
  @twisted.internet.defer.inlineCallbacks
  def connect( self, *args, **kw ):

    name, _dummy, handle = args
    yield print( 'device fufufu channel {} is connected.'.format( name ))

  @twisted.internet.defer.inlineCallbacks
  def hello_channel( self, repeat : int ):
    resp = yield 'fufufu' * repeat
    twisted.internet.defer.returnValue( resp )


class helloLabrad( labrad.devices.DeviceServer ):

  name           = 'hello_labrad' # Service name to be informed
  deviceWrappers = { 'hoge': hogehogeWrapper, 
                     'fufu': fufufuWrapper }

  possibleLinks  = { 'chan0' : { 'type' : 'hoge', 'addr' : 10 },      # better to be load from the registry
                     'chan1' : { 'type' : 'hoge', 'addr' : 11 },
                     'chan2' : { 'type' : 'fufu', 'addr' :  1 },
                     'chan3' : { 'type' : 'fufu', 'addr' :  4 },
                     'chan4' : { 'type' : 'fufu', 'addr' :  6 },
                     'chan5' : { 'type' : 'fufu', 'addr' :  2 } }

  @twisted.internet.defer.inlineCallbacks
  def initServer(self):
    yield labrad.devices.DeviceServer.initServer(self)

  def initContext(self, c):
    labrad.devices.DeviceServer.initContext(self,c)
    c['shared_variable_for_connection'] = dict()

  def chooseDeviceWrapper( self, *args, **kw ):

    if args[ 2 ] in [ 'hoge', 'fufu' ]:                     # args is the list made in the last part of self.findDevices()
      tag = args[ 2 ] 
    else:
      raise Exception()
    return self.deviceWrappers[ tag ]

  @twisted.internet.defer.inlineCallbacks
  def findDevices( self ):

    found = list ()

    for channel_name in self.possibleLinks.keys():
      print( 'checking chanel {}...'.format( channel_name ))
      try:
        print( 'pinging address {}'.format( self.possibleLinks[ channel_name ][ 'addr' ] ))
                                                            # pinging here... it sometimes tooks long time
        yield
      except Exception as e:
        print(sys._getframe().f_code.co_name,e)             # could not obtain any response from the device under test
        continue
                                                            # open device handle with lower APIs 
      # handle = open_device( self.possibleLinks[ channel_name ][ 'addr' ] )
      # handle.initialize()                                 # you can do some initialization here
      handle       = None
      device_type  = self.possibleLinks[ channel_name ][ 'type' ]
      device       = ( channel_name, ( channel_name, device_type, handle ), { } )
      found.append( device )
    twisted.internet.defer.returnValue( found ) 

                                                            # labrad communication protocol (to scalabrad) uses some 
                                                            # special variable type, e.g., 
                                                            # w: unsigned long,        i: signed int, 
                                                            # v: 64bit floating point, c: complex number of 64bit f.p., etc ..     
  @labrad.server.setting( 201, 'Hello', repeat = [ 'w' ], returns = ['s'] )
  def service_hello( self, c, repeat ):
    """
    This method returns Hello Labrad
    """
    dev  = self.selectedDevice( c )
    resp = yield dev.hello_channel( repeat )
    twisted.internet.defer.returnValue( 'Hello Labrad {0}'.format( resp ))

  
if __name__ == '__main__':

  __server__ = helloLabrad()
  labrad.util.runServer( __server__ )

