import random
import re
import subprocess
from pathlib import Path

from fast_colorthief import get_palette, get_dominant_color

IMAGE_FOLDER = "~/Pictures/wallpapers"
COLOR_COUNT = 4
BASH_COMMANDS = [('swww img "{PATH}"', False), ("killall -SIGUSR2 waybar", False)]

CONFIG_UPDATES = {
    "~/.config/niri/config.kdl": [
        {
            "pattern": r'active-gradient from="[^"]*" to="[^"]*"',
            "template": lambda colors: f'active-gradient from="#{colors[0][0]:02x}{colors[0][1]:02x}{colors[0][2]:02x}" to="#{colors[1][0]:02x}{colors[1][1]:02x}{colors[1][2]:02x}"',
        },
        {
            "pattern": r'inactive-gradient from="[^"]*" to="[^"]*"',
            "template": lambda colors: f'inactive-gradient from="#{colors[2][0]:02x}{colors[2][1]:02x}{colors[2][2]:02x}" to="#{colors[3][0]:02x}{colors[3][1]:02x}{colors[3][2]:02x}"',
        },
    ],
    "~/.config/waybar/style.css": [
        {
            "pattern": r"border-color:\s*#[0-9a-fA-F]{6};",
            "template": lambda dominant: f"border-color: #{dominant[0]:02x}{dominant[1]:02x}{dominant[2]:02x};",
        }
    ],
}


def get_random_image(folder_path: str) -> Path | None:
    folder = Path(folder_path).expanduser()
    image_extensions = {".png", ".jpg", ".jpeg", ".avif", ".gif", ".pnm", ".tga", ".tiff", ".webp", ".bmp", ".farbfeld"}
    images = [f for f in folder.glob("*") if f.suffix.lower() in image_extensions]
    return random.choice(images) if images else None


def extract_colors(image_path: Path):
    palette = get_palette(str(image_path), color_count=COLOR_COUNT)
    dominant = get_dominant_color(str(image_path), quality=1)
    return palette, dominant


def lighten_color(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(min(int(c + (255 - c) * amount), 255) for c in color)


def darken_color(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(max(int(c * (1 - amount)), 0) for c in color)


def update_file(
    file_path: Path,
    updates: list[dict],
    palette: list[tuple[int, int, int]],
    dominant: tuple[int, int, int],
):
    path = Path(file_path).expanduser()
    if not path.exists():
        return

    content = path.read_text()

    for update in updates:
        if "dominant" in update["template"].__code__.co_varnames:
            replacement = update["template"](dominant)
        else:
            replacement = update["template"](palette)

        content = re.sub(update["pattern"], replacement, content)

    path.write_text(content)


def run_commands(commands: list[tuple[str, bool]], image: Path):
    for cmd, is_background in commands:
        if is_background:
            subprocess.Popen(
                cmd.replace("{PATH}", image.as_posix()),
                shell=True,
                start_new_session=True,
            )
        else:
            subprocess.run(
                cmd.replace("{PATH}", image.as_posix()), shell=True, check=True
            )


def main():
    image = get_random_image(IMAGE_FOLDER)
    if not image:
        return

    palette, dominant = extract_colors(image)
    palette_sorted = sorted(palette, key=lambda c: sum(c))
    palette = [lighten_color(c, 0.1) for c in palette_sorted[COLOR_COUNT // 2 :]] + [
        darken_color(c, 0.2) for c in palette_sorted[: COLOR_COUNT // 2]
    ]
    dominant = lighten_color(dominant, 0.3)

    for file_path, updates in CONFIG_UPDATES.items():
        update_file(file_path, updates, palette, dominant)

    run_commands(BASH_COMMANDS, image)


if __name__ == "__main__":
    main()
