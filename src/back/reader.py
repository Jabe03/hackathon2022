import json
import time

import requests


class Reader:
    MISO_key: str = "wPNxKgt4iNxm13Iom2ox8VpnNddbSxRfviLBSBpc"
    root_url = "https://itsnt2259.iowa.uiowa.edu/piwebapi/search/query?q=name:"
    scaled_gas = "PP_TB1_2_WCB3_Scaled_Gas_Flow"
    boiler_12_flow = 'PP_BLR12_FT_006_KSCFH'



    gas_points_dict = {
        'scaled_gas':'PP_TB1_2_WCB3_Scaled_Gas_Flow',
        'hospital_blr_gas':'HBLR_GAS_FLOW',
        'b7_gas':'PP_B7_Gas_Flow_Adj ',
        'b8_gas':'PP_B8_Gas_Flow_Adj',
        'b10_gas' : 'PP_B10_FLT_235_FT',
        'b11_gas_day' : 'PP_AF-XI-8220A',
        'b12_gas' : 'PP_BLR12_FT_006_KSCFH ',
        'gg1_fuel_flow' : 'PP_GG1_FUEL_FLOW ',
        'gg2_fuel_flow' : 'PP_GG2_FUEL_FLOW ',
        'gg3_fuel_flow' : 'PP_GG3_FUEL_FLOW',
        'gg4_fuel_flow' : 'PP_GG4_FUEL_FLOW '


    }

    gas_values_that_need_to_be_scaled_up = [
        gas_points_dict['hospital_blr_gas'],
        gas_points_dict['b7_gas'],
        gas_points_dict['b8_gas'],
        gas_points_dict['b12_gas'],
        gas_points_dict['b11_gas_day']
    ]

    gas_values_dict = {
        'scaled_gas' : 0,
        'hospital_blr_gas' : 0,
        'b7_gas': 0,
        'b8_gas': 0,
        'b10_gas' : 0,
        'b11_gas_day':0,
        'b12_gas':0,
        'gg1_fuel_flow': 0,
        'gg2_fuel_flow': 0,
        'gg3_fuel_flow': 0,
        'gg4_fuel_flow' : 0

    }

    consumption_points_dict ={
    'electric_gen': 'PP_Electric_Gen',
    'electric_purch':  'PP_Electric_Purch',
    'oakdale_purch' :  'SUBO-69K.3351.EA-734.MW',
    'oakdale_diesel':  'OAK_DG3_Real_Power',
    'oakdale_gen1':   'SUBO-PP1.3351.GN1-734.MW',
    'oakdale_gen2':   'SUBO-PP1.3351.GN2-734.MW'
    }

    consumption_values_dict = {
    "electric_gen":0,
    "electric_purch" : 0,
    "oakdale_diesel": 0,
    "oakdale_gen1": 0,
    "oakdale_gen2" : 0,
    }

    pellet_points_dict={
        'b10_pellet_flow' : 'PP_CHS_B10WeighBelt_MvgAvg',
        'b10_pellet_day' : 'PP_CHS_B10WeighBelt_TotalizedWeight',
    }
    oats_points_dict={
        'b11_oat_flow' : 'PP_BIO_Weight',

        #'b11_oat_day' : 'PP_B11OHTOTY'
    }

    b11_other_dict={
        'b11_coal_and_pellets' : 'PP_SF-WIT-6044A'

    }

    all_fuels_dict = {
        'gasses': gas_points_dict,
        'pellets': pellet_points_dict,
        'coal+pellets' : b11_other_dict

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
        connection = requests.get(self.root_url + engie_point,
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
        for key in self.consumption_values_dict:
            if key == "oakdale_diesel":
                self.consumption_values_dict[key]= self.get_value((self.consumption_points_dict[key])) / 1000
            else:
                self.consumption_values_dict[key] = self.get_value(self.consumption_points_dict[key])
        values_list = self.consumption_values_dict.values()

        return sum(values_list)
    def get_page_json(self,url):
        return requests.get(url, auth=(self.user, self.pw)).json()

    def get_factor(self,gas_type):
        if(gas_type in self.gas_values_that_need_to_be_scaled_up):
            return 1000
        return 1
    def day_sum_gas_consumption(self, gas_type):
        factor = self.get_factor(gas_type)


        interpolation_url = 'interpolated/?startTime=-1d&endTime=-1d&interval=1h'
        response = self.get_page_json(self.root_url + gas_type)

        response = self.get_page_json(response["Items"][0]["Links"]["Self"])
        if gas_type[0:2]!="gg":
            response = self.get_page_json(response["Links"]["InterpolatedData"])
        else:
            response = self.get_page_json(response["Links"]["RecordedData"])

        if(gas_type == self.gas_points_dict["b11_gas_day"]):
            sum = response["Items"][0]["Value"] * factor
            print(gas_type + ": " + str(sum) + "(factor: " + str(factor) + ")")
            return sum

        items = response["Items"]
        sum = 0;
        for i in range(1,len(items)):
            item = items[i]["Value"]

            if item < 0:
                item = 0


            sum = sum + (factor * item)

        print(gas_type + ": " + str(sum) + "(factor: " + str(factor)+ ")")

        return sum
    def sum_yearly_gas_emissions(self):
       pass
    #implement

    def sum_daily_pellets_consumption(self):

        response =  self.get_page_json(self.root_url +"SF-WIT-6044A")
        response = self.get_page_json(response["Items"][0]["Links"]["Self"])
        response = self.get_page_json(response["Links"]["InterpolatedData"])

        items = response["Items"]
        sum = 0;
        for i in range(1,len(items)):
            item = items[i]["Value"]

            if item < 0:
                item = 0


            sum = sum + item
        return sum/2

    def sum_all_fuels(self):
        i = 0
        sum = 0
        for dict in self.all_fuels_dict:
            print(dict)
            for burner_name in self.all_fuels_dict[dict]:
                if dict =='gasses':
                    sum = sum + self.day_sum_gas_consumption(self.all_fuels_dict[dict][burner_name]) * .001026 * 53.0611
                elif dict=='pellets':
                    sum += self.sum_daily_pellets_consumption() * 20.89375 * 31.875
                elif dict == 'coal+pellets':

        #heat conversion constant and carbon factor
        return sum







def main():
    read = Reader();

    print(read.sum_all_fuels())
    #print(str)


if __name__ == "__main__":
    main()
