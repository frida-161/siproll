import siproll
import sys

siproll.do_call("sip:"+ sys.argv[1] + "@voip.eventphone.de", 60)
