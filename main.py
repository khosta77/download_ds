import os
import requests
import pandas as pd
import numpy as np
import progressbar
from tqdm import tqdm
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

'''
def download_image(url, class_number, i):
    directory = f'data/{class_number}'
    os.makedirs(directory, exist_ok=True)
    filename = f"{i}.png"
    file_path = os.path.join(directory, filename)
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        pass
        #print(f"Ошибка при скачивании изображения: {e}")
'''

def download_image(url, class_number, i, max_size=(256, 256)):
    """
    :param url: str, URL изображения
    :param max_size: tuple, максимальный размер (ширина, высота)
    :param output_path: str, путь для сохранения уменьшенного изображения
    """
    directory = f'data/{class_number}'
    os.makedirs(directory, exist_ok=True)
    filename = f"{i}.png"
    file_path = os.path.join(directory, filename)
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.thumbnail(max_size)
        img.save(file_path)
        #print(f"Изображение сохранено как {output_path}")
    except Exception as e:
        pass
        #print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    df = pd.read_csv('labirint_dataset.csv', sep=';')
    df = df[['imgUrl', 'rate']].dropna()
    df['rate'] = np.where(df['rate'] <= 9.25, 0, 1)
    for i, row in tqdm(df.iterrows()):
        download_image(row['imgUrl'], row['rate'], i)
