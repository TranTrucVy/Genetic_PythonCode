import csv
import os

def read_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.readlines()
    else:
        return None







    