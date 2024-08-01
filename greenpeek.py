"""
Program to display a picture using catimg.

Version: 0.1

Author: new_green
"""

import os
import json
import subprocess
import shutil  # Import shutil for checking executable path
from colored import fg, attr
import re

debug = False  # Debug True=enable False=disable (False is default)

def show_picture():
    """
    Displays a picture using catimg.

    The picture path and pixel size are read from a JSON file named 'data.json'
    in the same directory as the script.

    Args:
        None

    Returns:
        None

    Raises:
        FileNotFoundError: If the picture file or catimg executable is not found.
        json.JSONDecodeError: If the data file is not valid JSON.
        RuntimeError: If the image display fails.

    Example:
        >>> show_picture()
        # Displays the picture specified in data.json

    Notes:
        The data.json file should contain the following keys:
            - picture_name: The name of the picture file.
            - default_pixel_size: The default pixel size for the picture.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, 'data.json')

        with open(data_dir, 'r') as file:
            data = json.load(file)

        picture = data['picture_path']
        pixel_size = data['default_pixel_size']

        if not os.path.isfile(picture):
            raise FileNotFoundError(f"Image file not found: {picture}")

        # Check if catimg is executable
        if not shutil.which('catimg'):
            raise FileNotFoundError("catimg executable not found. Please install catimg.")

        check_errors = subprocess.run(
            ['catimg', '-w', str(pixel_size), picture],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if check_errors.returncode != 0:
            raise RuntimeError("Image display failed: " + picture)

        os.system(f'catimg -w {pixel_size} {picture}')

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        print(f"Data file is not valid JSON - {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    if debug:
        debug_message = f"{fg('red')}Debug mode is enabled{attr('reset')}"
        print(debug_message)

def show_system_features():
    try:
        pcname = f"{subprocess.check_output('whoami', shell=True).decode().strip()}@{subprocess.check_output('hostname', shell=True).decode().strip()}"
        print(f"{fg('green')}{pcname}{attr('reset')}")
        print("#-"*20)

        distro_info = subprocess.check_output('lsb_release -d', shell=True).decode().strip().split(':', 1)[1].strip()
        print(f"{fg('green')}OS:{attr('reset')} {distro_info}")

        kernel_name = os.popen('uname -r').read().strip()
        print(f"{fg('green')}Kernel:{attr('reset')} {kernel_name}")

        output = subprocess.check_output('uptime', shell=True).decode().strip()
        match = re.search(r'up\s+(\d+)\s+days?,?\s*(\d+):(\d+)|up\s+(\d+):(\d+)', output)

        if match:
            days = int(match.group(1) or 0)
            hours = int(match.group(2) or match.group(4))
            minutes = int(match.group(3) or match.group(5))
            total_hours = days * 24 + hours
            print(f"{fg('green')}Uptime:{attr('reset')} {total_hours} hours, {minutes} minutes")
        else:
            print(f"{fg('yellow')}Unable to parse uptime information{attr('reset')}")

        processor_name = os.popen('grep -m 1 "model name" /proc/cpuinfo').read().split(':')[1].strip()
        print(f"{fg('green')}Processor Name:{attr('reset')} {processor_name}")

        integr_gpu_info = ' '.join(os.popen('lspci | grep -i "vga\\|3d\\|2d"').read().strip().split(':')[2:]).strip()
        external_gpu_info = os.popen('lspci | grep -i "vga\\|3d\\|2d" | grep -i "amd\\|nvidia"').read().strip()

        print(f"{fg('green')}Integrated GPU:{attr('reset')} {integr_gpu_info}")

        if external_gpu_info:
            print(f"{fg('green')}External GPU:{attr('reset')} {external_gpu_info}")
        else:
            external_gpu_info = ' '.join(os.popen('lspci | grep -i "amd\\|nvidia"').read().strip().split(':')[2:]).strip()
            if external_gpu_info:
                print(f"{fg('green')}External GPU:{attr('reset')} {external_gpu_info}")
            else:
                print(f"{fg('yellow')}External GPU is not found!{attr('reset')}")

        total_ram_gb = subprocess.check_output('free -g | awk \'NR==2{print $2}\'', shell=True).decode().strip()
        print(f"{fg('green')}Memory:{attr('reset')} {total_ram_gb} GiB")

    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    show_picture()
    show_system_features()
