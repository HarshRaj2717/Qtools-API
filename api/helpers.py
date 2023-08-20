import hashlib
import os
import subprocess
from PIL import Image


def generate_hash(value: str) -> str:
    '''
    Generate a SHA-256 hash and return it
    '''
    return hashlib.sha256(value.encode()).hexdigest()


def resize_image(file_url: str, width: int, height: int) -> tuple[str, int]:
    '''
    Downloads image from given file_url,
    resizes it,
    and gives back a url to resized image
    '''
    try:
        os.mkdir('tools_temp')
    except FileExistsError:
        pass

    # Creating a unique file_name using file_url and removing slashes
    file_name = file_url.replace(
        "/", "_").replace("\\", "_") + "." + file_url.split(".")[-1]

    # Downloading File
    downloader = subprocess.Popen(
        f'curl --output "tools_temp/{file_name}" {file_url}', shell=True, stdout=subprocess.PIPE, cwd=os.curdir)
    downloader.wait()

    # Finding file transferr size
    file_transfer_size = int(max(os.path.getsize(f'tools_temp/{file_name}') * 1e-6, 1))

    # Resizing Image
    downloaded_file = Image.open(f'tools_temp/{file_name}')
    downloaded_file = downloaded_file.resize(
        (width, height), Image.ANTIALIAS)  # type: ignore
    downloaded_file.save(f'tools_temp/{file_name}')

    # Uploading File & Saving URL
    uploader = subprocess.Popen(
        f"curl -F 'file=@tools_temp/{file_name}' https://0x0.st", shell=True, stdout=subprocess.PIPE)
    uploader.wait()
    uploader_output_url = uploader.communicate()[0].decode('UTF-8').strip()

    # Deleting Downloaded File
    os.remove(f'tools_temp/{file_name}')

    return (uploader_output_url, file_transfer_size)
