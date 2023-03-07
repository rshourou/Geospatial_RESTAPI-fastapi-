from fastapi import responses
import requests
from loguru import logger
def download_image(url, file_name):
    logger.info(f'Initiating downloading image:{url}')
    with open(file_name, "wb") as f:
        response = requests.get(url)
        f.write(response.content)
        f.close()
    logger.info(f'image downloaded at {file_name}')
    