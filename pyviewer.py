#!/bin/env python3
from argparse import Namespace
import sys
import os


def to_string(obj):
    if isinstance(obj, str):
        return f"\"{obj}\""

    elif isinstance(obj, Namespace):
        dictobj = vars(obj)
        string = str.join('\n  ',
                          [f'{to_string(key)} : {to_string(value)}' for key, value in dictobj.items()])
        return f"Namespace(\n  {string}\n)"

    else:
        return str(obj)


def numpy_viewer(data):
    """data: np.ndarray"""
    import numpy as np
    returnstr = "Data shape: " + str(data.shape) + "\n"
    returnstr += "Data type: " + str(data.dtype) + "\n"
    returnstr += \
        f"""Summary properties:
    min: {data.min()}
    max: {data.max()}
    mean: {data.mean()}
    median: {np.median(data)}
    std: {data.std()}
    sum: {data.sum()}
"""
    returnstr += "Data:\n" + to_string(data) + "\n"
    return returnstr


def parse_file(filename) -> None:
    basename, ext = os.path.splitext(filename)

    if ext == '.npy':
        import numpy as np
        data = np.load(filename)
        return "file type: numpy array.\n" + numpy_viewer(data)

    elif ext == '.csv':
        import pandas as pd
        returnstr = "file type: csv file."

    elif ext == '.pth':
        try:
            import torch
            data = torch.load(filename)
            returnstr = f"Data type: {type(data)}\n"
            returnstr += 'Data:\n' + to_string(data) + '\n'
            return returnstr

        except Exception as e:
            print('Error:', e)

    else:
        raise Exception('Unsupported file type: {}'.format(ext))


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Usage: pyviewer.py <filename>")
        sys.exit(1)

    for i in range(1, len(sys.argv)):
        print(f'filename: {sys.argv[i]}')
        print(parse_file(sys.argv[i]))
        print('-'*min(int(os.get_terminal_size(0).columns/2), 50))
