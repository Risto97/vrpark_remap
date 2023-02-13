from evdev import InputDevice, UInput, categorize, ecodes as e
import time
import evdev
from enum import Enum
from evdev.eventio_async import asyncio
from pynotifier import Notification
import os


class InputType(Enum):
    KEYBOARD = 0
    MOUSE = 1

class AliexpressJoystickMapper:
    def __init__(self, dev_path : str, DEFAULT_MODE : InputType = InputType.KEYBOARD, TIME_DELAY : float=0.2):
        self.mode = DEFAULT_MODE
        self.TIME_DELAY = TIME_DELAY

        self.dev = evdev.InputDevice(dev_path)
        self.ui = UInput.from_device(self.dev, name='Keyboard remmapped from joystick')

        self.dev.grab()
    
    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.mouse_joystick_event())

    def toggle_mode(self):
        dir_path = os.path.abspath(os.path.dirname(__file__))
        if self.mode == InputType.KEYBOARD:
            self.mode = InputType.MOUSE
            icon_path = os.path.join(dir_path, 'icons/input-mouse.svg')
        else:
            self.mode = InputType.KEYBOARD
            icon_path = os.path.join(dir_path, 'icons/input-keyboard.svg')

        print(icon_path)
        # message("Some title", "Changed mode")
        
        Notification(
            title='Joystick mode changed',
            description=f'Mode is: {self.mode.name}',
            icon_path=icon_path,
            duration=2,                                   # Duration in seconds
            urgency='normal'
        ).send()




    async def mouse_joystick_event(self):
        prev_timestamp = 0

        async for ev in self.dev.async_read_loop():
            elapsed = ev.timestamp() - prev_timestamp

            # Keyboard mode
            if self.mode == InputType.KEYBOARD:
                if ev.type == evdev.ecodes.EV_REL and elapsed > self.TIME_DELAY:
                    if ev.code == evdev.ecodes.REL_X:
                        if ev.value > 0:
                            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 1)  # KEY_A down
                            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 0)  # KEY_A down
                        elif ev.value < 0:
                            self.ui.write(e.EV_KEY, e.KEY_LEFT, 1)  # KEY_A down
                            self.ui.write(e.EV_KEY, e.KEY_LEFT, 0)  # KEY_A down

                    elif ev.code == evdev.ecodes.REL_Y:
                        if ev.value < 0:
                            self.ui.write(e.EV_KEY, e.KEY_UP, 1)  # KEY_A down
                            self.ui.write(e.EV_KEY, e.KEY_UP, 0)  # KEY_A down
                        elif ev.value > 0:
                            self.ui.write(e.EV_KEY, e.KEY_DOWN, 1)  # KEY_A down
                            self.ui.write(e.EV_KEY, e.KEY_DOWN, 0)  # KEY_A down

                    self.ui.syn()
                    prev_timestamp = ev.timestamp()
                if ev.type == evdev.ecodes.EV_KEY and elapsed > self.TIME_DELAY:
                    if ev.code == evdev.ecodes.BTN_LEFT:
                         self.ui.write(e.EV_KEY, e.KEY_ENTER, 1)
                         self.ui.write(e.EV_KEY, e.KEY_ENTER, 0)
                    if ev.code == evdev.ecodes.BTN_SIDE:
                         self.ui.write(e.EV_KEY, e.KEY_BACKSPACE, 1)
                         self.ui.write(e.EV_KEY, e.KEY_BACKSPACE, 0)
                    if ev.code == evdev.ecodes.KEY_VOLUMEDOWN: # Toggle mode
                        self.toggle_mode()
                    prev_timestamp = ev.timestamp()
                    self.ui.syn()

            # Mouse self.mode
            elif self.mode == InputType.MOUSE and not (ev.type == evdev.ecodes.EV_KEY and ev.code == evdev.ecodes.KEY_VOLUMEDOWN):
                self.ui.write_event(ev)
                self.ui.syn()
            elif (ev.type == evdev.ecodes.EV_KEY and ev.code == evdev.ecodes.KEY_VOLUMEDOWN) and elapsed > self.TIME_DELAY:
                if ev.code == evdev.ecodes.KEY_VOLUMEDOWN: # Toggle mode
                    self.toggle_mode()
                prev_timestamp = ev.timestamp()
                self.ui.syn()


import sys

def main():
    args = sys.argv[1:]
    print(args)
    dev_path = args[0]
    print(dev_path)

    ali_joy = AliexpressJoystickMapper(dev_path)
    ali_joy.run()

if __name__ == "__main__":
    main()

