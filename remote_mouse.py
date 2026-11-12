#!/usr/bin/env python3
import time
import subprocess
from evdev import InputDevice, UInput, list_devices, ecodes as e

SPEED = 20

# Key Code Definitions
UP_KEYS = [e.KEY_UP, e.ABS_HAT0Y]
DOWN_KEYS = [e.KEY_DOWN]
LEFT_KEYS = [e.KEY_LEFT, e.ABS_HAT0X]
RIGHT_KEYS = [e.KEY_RIGHT]
SELECT_KEYS = [e.KEY_ENTER, e.KEY_KPENTER, e.BTN_SOUTH, e.KEY_OK, 28, 304]
MENU_KEYS = [e.KEY_MENU, e.KEY_CONTEXT_MENU, 139, 127, 147]

# Global System Keys
BACK_KEYS = [e.KEY_BACK, e.KEY_ESC, 158, 1]
HOME_KEYS = [e.KEY_HOMEPAGE, e.KEY_HOME, 172, 102]
VOL_UP_KEYS = [e.KEY_VOLUMEUP, 115]
VOL_DOWN_KEYS = [e.KEY_VOLUMEDOWN, 114]
MUTE_KEYS = [e.KEY_MUTE, 113]


def find_fire_remote():
    """Scans connected Bluetooth/USB input devices for the Fire TV Remote."""
    for path in list_devices():
        try:
            dev = InputDevice(path)
            name = dev.name.lower()
            if any(k in name for k in ["amazon", "fire", "remote", "ar", "gamepad"]):
                return dev
        except Exception:
            continue
    return None


def kill_active_window():
    """Closes the currently focused window using kdotool on KDE Wayland."""
    try:
        win_id = subprocess.check_output(
            ["kdotool", "getactivewindow"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8").strip()

        if win_id:
            subprocess.run(["kdotool", "windowclose", win_id], stderr=subprocess.DEVNULL)
    except Exception:
        pass


def main():
    cap = {
        e.EV_REL: [e.REL_X, e.REL_Y],
        e.EV_KEY: [
            e.BTN_LEFT, e.BTN_RIGHT,
            e.KEY_UP, e.KEY_DOWN, e.KEY_LEFT, e.KEY_RIGHT, e.KEY_ENTER,
            e.KEY_BACK, e.KEY_ESC, e.KEY_HOMEPAGE, e.KEY_HOME,
            e.KEY_VOLUMEUP, e.KEY_VOLUMEDOWN, e.KEY_MUTE
        ]
    }
    v_device = UInput(cap, name="Fire-Remote-Virtual-Controller")
    print("Fire TV Remote Service started. Waiting for remote connection...")

    try:
        while True:
            remote = find_fire_remote()
            if not remote:
                time.sleep(2)
                continue

            print(f"Connected to: {remote.name} ({remote.path})")
            mouse_mode = False

            try:
                remote.grab()
                for event in remote.read_loop():
                    if event.type != e.EV_KEY:
                        continue

                    code = event.code
                    val = event.value  # 1 = Press, 0 = Release, 2 = Hold

                    # 1. Toggle Mode via Menu Button (≡)
                    if code in MENU_KEYS and val == 1:
                        mouse_mode = not mouse_mode
                        mode_name = "MOUSE MODE" if mouse_mode else "NATIVE D-PAD MODE"
                        print(f">>> Switched to {mode_name}")
                        continue

                    # 2. Home Button -> Close Active Window & Return Home
                    if code in HOME_KEYS:
                        if val == 1:
                            kill_active_window()
                            mouse_mode = False
                            v_device.write(e.EV_KEY, e.KEY_HOMEPAGE, 1)
                            v_device.syn()
                        elif val == 0:
                            v_device.write(e.EV_KEY, e.KEY_HOMEPAGE, 0)
                            v_device.syn()
                        continue

                    # 3. Global System Keys (Back, Volume, Mute)
                    system_target = None
                    if code in BACK_KEYS:
                        system_target = e.KEY_BACK
                    elif code in VOL_UP_KEYS:
                        system_target = e.KEY_VOLUMEUP
                    elif code in VOL_DOWN_KEYS:
                        system_target = e.KEY_VOLUMEDOWN
                    elif code in MUTE_KEYS:
                        system_target = e.KEY_MUTE

                    if system_target:
                        v_device.write(e.EV_KEY, system_target, 1 if val in (1, 2) else 0)
                        v_device.syn()
                        continue

                    # 4. Mode-Specific Navigation
                    if mouse_mode:
                        if code in SELECT_KEYS:
                            v_device.write(e.EV_KEY, e.BTN_LEFT, 1 if val in (1, 2) else 0)
                            v_device.syn()
                        elif val in (1, 2):
                            dx, dy = 0, 0
                            if code in UP_KEYS:
                                dy = -SPEED
                            elif code in DOWN_KEYS:
                                dy = SPEED
                            elif code in LEFT_KEYS:
                                dx = -SPEED
                            elif code in RIGHT_KEYS:
                                dx = SPEED

                            if dx != 0 or dy != 0:
                                v_device.write(e.EV_REL, e.REL_X, dx)
                                v_device.write(e.EV_REL, e.REL_Y, dy)
                                v_device.syn()
                    else:
                        target_key = None
                        if code in UP_KEYS:
                            target_key = e.KEY_UP
                        elif code in DOWN_KEYS:
                            target_key = e.KEY_DOWN
                        elif code in LEFT_KEYS:
                            target_key = e.KEY_LEFT
                        elif code in RIGHT_KEYS:
                            target_key = e.KEY_RIGHT
                        elif code in SELECT_KEYS:
                            target_key = e.KEY_ENTER

                        if target_key:
                            v_device.write(e.EV_KEY, target_key, 1 if val in (1, 2) else 0)
                            v_device.syn()

            except OSError:
                print("Remote disconnected or went to sleep. Scanning for reconnect...")
                time.sleep(2)
            finally:
                try:
                    remote.ungrab()
                except Exception:
                    pass

    except KeyboardInterrupt:
        print("\nStopping remote controller.")
    finally:
        v_device.close()


if __name__ == "__main__":
    main()
