import sys
import yaml
import pjsua as pj

file = open("settings.yaml", "r") 
settings = yaml.load(file.read())

server = settings["server"]
number = settings["number"]
password = settings["password"]


lib = pj.Lib()


def log_cb(level, str, len):
    print str,

class MyAccountCallback(pj.AccountCallback):

    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)

    # Notification on incoming call
    def on_incoming_call(self, call):
        print "Incoming call from ", call.info().remote_uri
        call.answer(180)
        #call.set_callback(MyCallCallback(call))

class MyCallCallback(pj.CallCallback):

    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        global current_call
        print "Call with", self.call.info().remote_uri,
        print "is", self.call.info().state_text,
        print "last code =", self.call.info().last_code, 
        print "(" + self.call.info().last_reason + ")"
        
        if self.call.info().state == pj.CallState.DISCONNECTED:
            current_call = None
            print 'Current call is', current_call

    # Notification when call's media state has changed.
    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            player = lib.createPlayer("/tmp/message.wav",True)
            lib.conf_conncect(player, call_slot)
            lib.conf_conncect(call_slot, player)
            #pj.Lib.instance().conf_connect(player, call_slot
            #pj.Lib.instance().conf_connect(call_slot, player)
            print "Media is now active"
        else:
            print "Media is inactive"

try:
    lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))

    transport = lib.create_transport(pj.TransportType.UDP)

    lib.start()

    acc_cfg = pj.AccountConfig()
    acc_cfg.id = "sip:" + str(number) + "@" + server
    acc_cfg.reg_uri = "sip:" + server
    acc_cfg.proxy = [ "sip:" + server + ";lr" ]
    acc_cfg.auth_cred = [ pj.AuthCred("*", str(number), password) ]

    acc = lib.create_account(acc_cfg)
    acc = lib.create_account_for_transport(transport, cb = MyAccountCallback())
    

    while True:
        x = raw_input("Press [Enter] to stop\n")
        if x == "":
            break

    
    # Shutdown the library
    transport = None
    acc.delete()
    acc = None
    lib.destroy()
    lib = None

except pj.Error, err:
    print 'Error doing stuff:', err
