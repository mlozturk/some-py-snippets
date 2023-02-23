import os
import subprocess
from fontTools.ttLib import TTFont


def get_font_paths():
    """
    Try to get the font paths using `fc-list`, and return them as a set.
    If `fc-list` fails, use a default set of font paths.
    """
    try:
        font_output = subprocess.check_output(['fc-list', ':', '-f', '%{file}\n'])
        font_paths = set(os.path.dirname(line.strip().decode('utf-8')) for line in font_output.split(b'\n') if line.strip())
    except subprocess.CalledProcessError:
        font_paths = ['/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.fonts')]
    return font_paths


def print_font_charmaps(font_file_path):
    """
    Load a font file using `TTFont` and print its name and character maps.
    If loading the font file fails, print an error message with the exception.
    """
    try:
        font = TTFont(font_file_path)
    except Exception as e:
        print(f'Error: failed to load font file "{font_file_path}": {e}')
        return
    charmap = font.getBestCmap()
    font_name = font['name'].getName(1, 3, 1, 1033).toUnicode()
    char_list = [chr(code) for code in charmap.keys()]
    print(f'Font name: {font_name}\nFont charmaps: {" ".join(char_list)}\n')
    font.close()


def main():
    """
    Get the font paths using `get_font_paths`, and loop over all the font files
    in each path. For each font file, call `print_font_charmaps` to print its
    name and character maps.
    """
    font_paths = get_font_paths()
    for font_path in font_paths:
        for filename in os.listdir(font_path):
            if not (filename.endswith('.ttf') or filename.endswith('.otf')):
                continue
            font_file_path = os.path.join(font_path, filename)
            print_font_charmaps(font_file_path)


if __name__ == '__main__':
    main()
