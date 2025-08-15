# Dotfiles

My personal configuration files for my arch setup.

## What's included

- **[niri](https://github.com/YaLTeR/niri)** - Scrollable-tiling Wayland compositor
- **[waybar](https://github.com/Alexays/Waybar)** - Wayland status bar
- **[foot](https://codeberg.org/dnkl/foot)** - Fast, lightweight and minimalistic Wayland terminal emulator
- **[fastfetch](https://github.com/fastfetch-cli/fastfetch)** - System information tool
- **[swaylock](https://github.com/swaywm/swaylock)** - Screen locker for Wayland
- **[MPD](https://github.com/MusicPlayerDaemon/MPD)** - Music Player Daemon 

## Custom script

`~/.config/scripts/wallpaper.py` - A Python script that:
- Sets a random wallpaper from a specified directory
- Automatically adapts niri and waybar themes based on the wallpaper colors
- Inspired by [pywal](https://github.com/dylanaraps/pywal)

## Installation

Clone this repository and copy the `.config` folder to your home directory.

## ⚠️ Warning

The keyboard shortcuts in the configuration are set up for an AZERTY keyboard layout. Some shortcuts won't work correctly on QWERTY keyboards.
