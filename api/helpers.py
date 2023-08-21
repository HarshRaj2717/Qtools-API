import hashlib
import os
import requests
import moviepy.editor as mp
from PIL import Image

TEMP_STORAGE_FOLDER = 'tools_temp_storage'

try:
    os.mkdir(TEMP_STORAGE_FOLDER)
except FileExistsError:
    pass


def download_file(url: str, save_as: str) -> None:
    '''
    dowanload frile from `url` to `save_as`
    '''
    response = requests.get(url)
    with open(save_as, "wb") as f:
        f.write(response.content)


def upload_file(file_path: str) -> str:
    '''
    Upload provided file to 0x0.st and return uploaded URL
    '''
    file_name = file_path.replace('/', '_')
    with open(file_path, "rb") as file:
        response = requests.post(
            "https://0x0.st", files={"file": (f'@{file_name}', file)})
    return response.content.decode("UTF-8").strip()


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

    # Creating a unique file_name using file_url and removing slashes
    file_name = file_url.replace(
        "/", "_").replace("\\", "_") + "." + file_url.split(".")[-1]

    # Downloading File
    download_file(file_url, f'{TEMP_STORAGE_FOLDER}/{file_name}')

    # Finding file transferr size
    file_transfer_size = int(
        max(os.path.getsize(f'{TEMP_STORAGE_FOLDER}/{file_name}') * 1e-6, 1))

    # Resizing Image
    downloaded_file = Image.open(f'{TEMP_STORAGE_FOLDER}/{file_name}')
    downloaded_file = downloaded_file.resize(
        (width, height), Image.ANTIALIAS)  # type: ignore
    downloaded_file.save(f'{TEMP_STORAGE_FOLDER}/{file_name}')

    # Uploading File & Saving URL
    uploader_output_url = upload_file(f'{TEMP_STORAGE_FOLDER}/{file_name}')

    # Deleting The File
    os.remove(f'{TEMP_STORAGE_FOLDER}/{file_name}')

    return (uploader_output_url, file_transfer_size)


def video_to_mp3(file_url: str) -> tuple[str, int]:
    '''
    Downloads video from given file_url,
    resizes it,
    and gives back a url to it's audio file
    '''

    # Creating a unique file_name using file_url and removing slashes
    file_name = file_url.replace(
        "/", "_").replace("\\", "_") + "." + file_url.split(".")[-1]

    # Downloading File
    download_file(file_url, f'{TEMP_STORAGE_FOLDER}/{file_name}')

    # Finding file transferr size
    file_transfer_size = int(
        max(os.path.getsize(f'{TEMP_STORAGE_FOLDER}/{file_name}') * 1e-6, 1))

    # Converting to audio
    clip = mp.VideoFileClip(f'{TEMP_STORAGE_FOLDER}/{file_name}')
    clip.audio.write_audiofile(f'{TEMP_STORAGE_FOLDER}/{file_name}.mp3')

    # Uploading File & Saving URL
    uploader_output_url = upload_file(f'{TEMP_STORAGE_FOLDER}/{file_name}.mp3')

    # Deleting Downloaded File
    os.remove(f'{TEMP_STORAGE_FOLDER}/{file_name}')
    os.remove(f'{TEMP_STORAGE_FOLDER}/{file_name}.mp3')

    return (uploader_output_url, file_transfer_size)
