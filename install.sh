#!/usr/bin/env bash
set -e

echo "Installing dependencies (python3-evdev, kdotool)..."
sudo dnf install -y python3-evdev kdotool

echo "Configuring persistent udev permissions for /dev/uinput..."
echo 'KERNEL=="uinput", MODE="0660", GROUP="input"' | sudo tee /etc/udev/rules.d/99-uinput.rules > /dev/null
sudo udevadm control --reload-rules && sudo udevadm trigger

echo "Adding user $USER to the 'input' group..."
sudo usermod -aG input "$USER"

echo "Installing script and systemd user service..."
mkdir -p ~/.local/bin ~/.config/systemd/user
cp remote_mouse.py ~/.local/bin/remote_mouse.py
chmod +x ~/.local/bin/remote_mouse.py
cp fire-remote-mouse.service ~/.config/systemd/user/fire-remote-mouse.service

systemctl --user daemon-reload
systemctl --user enable --now fire-remote-mouse.service

echo "Done! Log out and log back in once if group permissions require a refresh."
