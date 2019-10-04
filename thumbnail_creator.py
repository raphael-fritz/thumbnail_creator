"""
Bulk Thumbnail Creator
    Create an image program which can take hundreds of images and converts them to a specified size in the background thread.
    For added complexity, have one thread handling re-sizing, have another bulk renaming of thumbnails etc.
        from: https://github.com/karan/Projects
"""

from pathlib import Path
from os import listdir
from os import mkdir
from os import path
from sys import stdout
from PIL import Image
from multiprocessing import Process

#loading, resizing & saving
def create_thumbnail(img_path, size):
    # loading
    img = Image.open(img_path)

    # resizing
    img.thumbnail(size)

    # saving
    save_path = Path().absolute() / "thumbnails"/img_path.name
    img.save(save_path)

# threading implementation
def thumbnail_creator(img_list, folder_path, size):
    for i in range(img_list.__len__()):
        img_path = folder_path / img_list[i]
        
        p = Process(target=create_thumbnail, args=(img_path, size,))
        p.start()
        progressBar(i+1, img_list.__len__())
        p.join()

        """create_thumbnail(img_path, size)
        progressBar(i+1, img_list.__len__())"""

def progressBar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    stdout.write("\rcreating thumbnails: [{0}] {1}%".format(
        arrow + spaces, int(round(percent * 100))))
    stdout.flush()

if __name__ == "__main__":
    print("bulk thumbnail creator\n")

    # retrieving a list with pictures
    folder_path = Path(str(input("path of the directory with images: ")))
    img_list = listdir(folder_path)

    # retrieving desired thumbnail resolution
    x_size = int(input("desired size: x: "))
    y_size = int(input("              y: "))
    size = x_size, y_size

    if not path.exists("./thumbnails"):
        mkdir("./thumbnails")
    print("\n")
    thumbnail_creator(img_list, folder_path, size)