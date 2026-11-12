# Fire TV Remote Adapter for KDE Plasma Bigscreen (Wayland)

A lightweight Python `evdev`/`uinput` background service that turns an Amazon Fire TV Bluetooth Remote into a complete HTPC controller for **KDE Plasma Bigscreen** on Fedora / Wayland.

## Features

- **Dual-Mode Toggle (`≡` Menu Button):** Switch seamlessly between native D-pad navigation (for Plasma Bigscreen TV tiles) and virtual mouse cursor mode (for web browsers and desktop apps).
- **Smart Home Button (`⌂`):** Automatically closes the currently focused foreground app via `kdotool`, resets back to D-pad mode, and returns to the Plasma Bigscreen home screen.
- **Global Media & Navigation Keys:** Back, Volume Up, Volume Down, and Mute work across both modes.
- **Auto-Reconnect on Wake:** Automatically re-attaches when the Fire TV remote wakes up from Bluetooth sleep.

---

## Button Mapping

| Remote Button | Native D-Pad Mode (Default) | Virtual Mouse Mode |
| :--- | :--- | :--- |
| **Menu (`≡`)** | Switch to Mouse Mode | Switch to Native D-Pad Mode |
| **D-Pad** | Up / Down / Left / Right | Move Mouse Cursor |
| **Select (Center)** | Enter / OK | Left Mouse Click |
| **Home (`⌂`)** | Close Active App + Go Home | Close Active App + Go Home |
| **Back (`↩`)** | Back | Back |
| **Volume + / - / Mute** | System Volume Control | System Volume Control |

---

## Installation (Fedora / KDE Plasma 6)

### 1. Pair Your Fire TV Remote
1. Unplug any nearby Fire TV Stick power adapter temporarily so it doesn't reclaim the remote.
2. Press and hold the **Home (`⌂`)** button on the Fire TV remote for **10–15 seconds** until the top LED flashes rapidly.
3. Open **System Settings → Bluetooth** on your Linux machine and pair **"AR"** (or *Amazon Fire TV Remote*).

### 2. Run the Installer
Open **Konsole** and run:

```bash
git clone [https://github.com/YOUR_USERNAME/fire-tv-bigscreen-remote.git](https://github.com/YOUR_USERNAME/fire-tv-bigscreen-remote.git)
cd fire-tv-bigscreen-remote
chmod +x install.sh
./install.sh
