import os
import time
from getpass import getpass

import matplotlib.pyplot as plt
import requests


class Plotter:
    points = []

    def __init__(self):
        pass

    def add_point(self, pair):
        self.points.append(pair)
        pass

    def update(self):
        pass


def main():
    rel_path = "../back/logins/login.txt"
    login = open(rel_path)

    user = login.readline()[:-1];

    pw = login.readline()[:-1];


    connection = requests.get('https://itsnt2259.iowa.uiowa.edu/piwebapi/search/query?q=name:PP_BLR12_FT_006_KSCFH',
                              auth=(user, pw))

    print(connection.text);


if __name__ == "__main__":
    main()
