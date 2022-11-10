from enum import Enum
import time
import re
import logging
import sys
import lgpio

# open the gpio chip and set TRIG pin as output
TRIG = 26
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, TRIG)

STEAM_PROC = '/proc/asound/card2/stream0'

class State(Enum):
    UNKNOWN = 'unkown'
    OFF = 'off'
    ON = 'on'

#
# Here we look for the playback status
#
#    $ cat /proc/asound/card2/stream0
#    MOTU M4 at usb-0000:01:00.0-1.3, high speed : USB Audio
#    Playback:
#      Status: Running
#        ...
#
def getSoundState() :
    state = State.UNKNOWN
    
    file = open(STEAM_PROC)
    data = file.read()
    file.close()
    
    result = re.search("Playback:\s+Status:\s+(Running|Stop)", data)
    if result is not None:
        match result.group(1):
            case 'Running':
                state = State.ON
            case 'Stop':
                state = State.OFF
        
    #log.info("Sound is " + str(state))
    return state

#
# Get the state of the gpio pin
#
def getAmpState() :
    state = State.UNKNOWN
    data = lgpio.gpio_read(h, TRIG)
    if data is not None:
        match str(data):
            case '1':
                state = State.ON
            case '0':
                state = State.OFF
    
    log.info("Amp is " + str(state))
    return state

#
# Set the state of the gpio pin
#
def setAmpState(state) :
    if (state == State.UNKNOWN):
        return
    log.info("Setting Amp to " + str(state))
    match str(state):
        case 'State.ON':
            data = 1
        case 'State.OFF':
            data = 0

    lgpio.gpio_write(h, TRIG, data)

#
# Main loop
#
if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log = logging.getLogger("amp_trigger")
    log.info("Starting")

    sound_prev_state = State.UNKNOWN
    while (True) :
        sound_new_state = getSoundState()
        if sound_new_state == State.UNKNOWN:
            log.error("Unable to get sound state")
            sys.exit()
        elif sound_prev_state != sound_new_state:
            log.info("Sound changed from " + str(sound_prev_state) + " to " + str(sound_new_state))
            amp_state = getAmpState()
            if amp_state == State.UNKNOWN:
                log.error("Unable to get amp state")
                sys.exit()
            elif amp_state != sound_new_state:
                setAmpState(sound_new_state)
            else:
                log.info("Amp is already " + str(sound_new_state))
        sound_prev_state = sound_new_state
        time.sleep(1)
