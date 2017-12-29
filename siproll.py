import subprocess

class Roller:
    def __init__(self):
        pjsua = ["/usr/local/bin/pjsua",
                "--auto-play",
                "--play-file", "/tmp/message.wav"]
        self.process = subprocess.Popen(pjsua, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        for line in iter(self.process.stdout.readline,''):
            if line.startswith("You have"):
                print "Roller initialized"
                break

    def call(self, number):
        print "calling " + str(number)
        self.process.stdin.write("m\nsip:"+ str(number) + "@voip.eventphone.de\n")
