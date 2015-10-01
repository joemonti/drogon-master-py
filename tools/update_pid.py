#!/usr/bin/env python

import sys

import rcorelib
import rcorelib.event as revent

RCORE_HOST = "localhost"


def main(args):
    if len(args) <= 1:
        print "Usage: %s [-h host] TYPE KP KI KD" % (args[0])
        sys.exit(1)

    host = RCORE_HOST

    if args[1] == '-h':
        host = args[2]
        args = args[3:]

    pidType = args[1]
    kp = float(args[2])
    ki = float(args[3])
    kd = float(args[4])

    rcore = rcorelib.RCoreClient(host, "tool_update_pid")
    # rcore.start()

    evtType = rcore.read_event_type('arduino_pid')
    evt = revent.RCoreEventBuilder(evtType) \
        .add_string(pidType) \
        .add_float(kp) \
        .add_float(ki) \
        .add_float(kd) \
        .build()

    rcore.send(evt)

    rcore.close()

if __name__ == "__main__":
    main(sys.argv)
