import time
import subprocess
import threading

def do_call(uri, timeout):
    pjsua = ["/usr/local/bin/pjsua",
            "--auto-play",
            "--play-file", "/tmp/message.wav",
            uri]
    p = subprocess.Popen(pjsua, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    print "calling " + uri

    def terminate(p):
        if p.poll() == None:
            p.terminate()
    
    t = threading.Timer(timeout, terminate, [p])
    t.start() 

    for line in iter(p.stdout.readline,''):
        if "(PJ_EEOF)" in line.rsplit():
            print "call hung up"
            t.cancel()
            terminate(p)
        
