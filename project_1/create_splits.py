import argparse
import glob
import os
import random
import shutil

import numpy as np
from utils import get_module_logger


def create_folder(path, directory):
    if not os.path.exists(path + directory):
        os.mkdir(directory)

def delete_folder(path):
    try:
        shutil.rmtree(path)
    except OSError as error:
        print(error)
        print(path + " can not be removed")


def split_files(count, path, files):
    for i in range(count):
        p = files.pop()
        os.symlink('preprocessed_data' + p, path + p)
    print(path + " files has been splitted successfully!")


def split(data_dir):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - data_dir [str]: data directory, /home/workspace/data/preprocessed_data
    """
    # TODO: Complete this function
    os.chdir("data")
    total = 0
    files = []
    src_path = data_dir + "/preprocessed_data"

    for file in os.listdir(src_path):
        if file.endswith(".tfrecord"):
            total += 1
            files.append(file)

    random.shuffle(files)
    train = int(75 / 100 * total)
    val = int(15 / 100 * total)
    test = int(10 / 100 * total)

    delete_folder('train/')
    delete_folder('test/')
    delete_folder('val/')

    create_folder(data_dir, 'train/')
    create_folder(data_dir, 'test/')
    create_folder(data_dir, 'val/')

    split_files(train, 'train/', files)
    split_files(test, 'test/', files)
    split_files(val, 'val/', files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--data_dir', required=True,
                        help='data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.data_dir)