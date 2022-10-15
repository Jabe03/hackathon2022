import json
import time

import requests


class Reader:
    MISO_key: str = "wPNxKgt4iNxm13Iom2ox8VpnNddbSxRfviLBSBpc"

    boiler_12_flow = 'PP_BLR12_FT_006_KSCFH'

    points_dict ={
    'electric_gen': 'PP_Electric_Gen',
    'electric_purch':  'PP_Electric_Purch',
    'oakdale_purch' :  'SUBO-69K.3351.EA-734.MW',
    'oakdale_diesel':  'OAK_DG3_Real_Power',
    'oakdale_gen1':   'SUBO-PP1.3351.GN1-734.MW',
    'oakdale_gen2':   'SUBO-PP1.3351.GN2-734.MW'
    }

    values_dict = {
    "electric_gen":0,
    "electric_purch" : 0,
    "electric_gen" : 0,
    "oakdale_diesel": 0,
    "oakdale_gen1": 0,
    "oakdale_gen2" : 0,
    }

    rel_path = "../back/logins/login.txt"
    user = ""
    pw = ""


    def __init__(self):
        self.get_user_info()

    def get_user_info(self):
        login = open(self.rel_path)

        self.user = login.readline()[:-1];

        self.pw = login.readline()[:-1];

    def get_from_engie(self, engie_point: str):
        #print(engie_point)
        connection = requests.get("https://itsnt2259.iowa.uiowa.edu/piwebapi/search/query?q=name:" + engie_point,
                                  auth=(self.user, self.pw))

        #print(connection.text);

        return connection


    def get_value(self,point_code) -> float:
        value = 0

        response = self.get_from_engie(point_code)

        parsed = response.json()
        response = requests.get(parsed["Items"][0]["Links"]["Self"], auth=(self.user, self.pw))
        #print(parsed["Items"][0]["Links"]["Self"])

        parsed = response.json()
        response = requests.get(parsed["Links"]["Value"], auth=(self.user, self.pw))

        return response.json()["Value"]
        #print(parsed_self["Links"])

    def sum_energy_load(self):
        for key in self.values_dict:
            if key == "oakdale_diesel":
                self.values_dict[key]=self.get_value((self.points_dict[key]))/1000
            else:
                self.values_dict[key] = self.get_value(self.points_dict[key])
        values_list = self.values_dict.values()

        return sum(values_list)


def main():
    read = Reader();
    while(True):
        print(str(read.sum_energy_load()))
        print(read.values_dict)
        time.sleep(.5);
    #print(str)


if __name__ == "__main__":
    main()
