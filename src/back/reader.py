import datetime
import time

import requests

import matplotlib.pyplot as plt


class Reader:
    MISO_key: str = "wPNxKgt4iNxm13Iom2ox8VpnNddbSxRfviLBSBpc"
    root_url = "https://itsnt2259.iowa.uiowa.edu/piwebapi/search/query?q=name:"
    scaled_gas = "PP_TB1_2_WCB3_Scaled_Gas_Flow"
    boiler_12_flow = 'PP_BLR12_FT_006_KSCFH'

    oakdale_engine_values = []
    oakdale_boiler_values = []
    normal_gas_values = []
    gas_values = []
    pellets_values = []
    coal_pellets_values = []
    total_values = []

    dates_to_ratio = {
        datetime.datetime(2017, 1, 1): .285,
        datetime.datetime(2021, 12, 13): .375,
        datetime.datetime(2021, 12, 14): .32,
        datetime.datetime(2021, 12, 15): .5,
        datetime.datetime(2021, 12, 16): .3925,
        datetime.datetime(2021, 12, 17): .285,
        datetime.datetime(2022, 1, 18): .625,
        datetime.datetime(2022, 1, 19): .5,
        datetime.datetime(2022, 1, 24): .625,
        datetime.datetime(2022, 6, 1): .285,
        datetime.datetime(2022, 8, 29): .375,

    }
    gas_points_dict = {
        'scaled_gas': 'PP_TB1_2_WCB3_Scaled_Gas_Flow',
        'hospital_blr_gas': 'HBLR_GAS_FLOW',
        'b7_gas': 'PP_B7_Gas_Flow_Adj ',
        'b8_gas': 'PP_B8_Gas_Flow_Adj',
        'b10_gas': 'PP_B10_FLT_235_FT',
        'b11_gas_day': 'PP_AF-XI-8220A',
        'b12_gas': 'PP_BLR12_FT_006_KSCFH ',
        'gg1_fuel_flow': 'PP_GG1_FUEL_FLOW ',
        'gg2_fuel_flow': 'PP_GG2_FUEL_FLOW ',
        'gg3_fuel_flow': 'PP_GG3_FUEL_FLOW',
        'gg4_fuel_flow': 'PP_GG4_FUEL_FLOW '

    }

    gas_values_that_need_to_be_scaled_up = [
        gas_points_dict['hospital_blr_gas'],
        gas_points_dict['b7_gas'],
        gas_points_dict['b8_gas'],
        gas_points_dict['b12_gas'],
        gas_points_dict['b11_gas_day']
    ]

    gas_values_dict = {
        'scaled_gas': 0,
        'hospital_blr_gas': 0,
        'b7_gas': 0,
        'b8_gas': 0,
        'b10_gas': 0,
        'b11_gas_day': 0,
        'b12_gas': 0,
        'gg1_fuel_flow': 0,
        'gg2_fuel_flow': 0,
        'gg3_fuel_flow': 0,
        'gg4_fuel_flow': 0

    }
    oakdale_gas_points_dict = {
        "oak1_blr": "OAK_Boiler1_Steam_MMBTU/HR",
        "oak2_blr": "OAK_Boiler2_Steam_MMBTU/HR",
        "oak3_blr": 'OAK_Boiler3_Steam_MMBTU/HR',
        "oak4_blr": 'OAK_Boiler4_Steam_MMBTU/HR'
    }

    consumption_points_dict = {
        'electric_gen': 'PP_Electric_Gen',
        'electric_purch': 'PP_Electric_Purch',
        'oakdale_purch': 'SUBO-69K.3351.EA-734.MW',
        'oakdale_diesel': 'OAK_DG3_Real_Power',
        'oakdale_gen1': 'SUBO-PP1.3351.GN1-734.MW',
        'oakdale_gen2': 'SUBO-PP1.3351.GN2-734.MW'
    }

    consumption_values_dict = {
        "electric_gen": 0,
        "electric_purch": 0,
        "oakdale_diesel": 0,
        "oakdale_gen1": 0,
        "oakdale_gen2": 0,
    }

    pellet_points_dict = {
        'b10_pellet_flow': 'PP_CHS_B10WeighBelt_MvgAvg',

    }
    oats_points_dict = {
        'b11_oat_flow': 'PP_BIO_Weight',

        # 'b11_oat_day' : 'PP_B11OHTOTY'
    }

    b11_other_dict = {
        'b11_coal_and_pellets': 'PP_SF-WIT-6044A'

    }

    all_fuels_dict = {
        'gasses': gas_points_dict,
        'pellets': pellet_points_dict,
        'coal+pellets': b11_other_dict,
        'oakdale_gasses': oakdale_gas_points_dict

    }

    gas_conversion_factor = .001026 * 53.0611
    coal_conversion_factor = 24.93 * 93.2926
    pellet_conversion_factor = 20.89375 * 31.875

    rel_path = "../back/logins/login.txt"
    user = ""
    pw = ""
    page_get_counter = 0;

    start_time = 0;
    def __init__(self):
        self.get_user_info()

    def start_timer(self):
        self.start_time = time.time()*1000;

    def get_elapsed(self):
        result = time.time()*1000 - self.start_time;
        start = time.time()
        return result

    def print_elapsed_time(self,msg):
        print(msg + " elapsed in: " + str(self.get_elapsed()));
    def get_user_info(self):
        login = open(self.rel_path)

        self.user = login.readline()[:-1];

        self.pw = login.readline()[:-1];

    def get_from_engie(self, engie_point: str):
        # print(engie_point)
        connection = requests.get(self.root_url + engie_point,
                                  auth=(self.user, self.pw))

        # print(connection.text);

        return connection

    def get_ratio_from_date(self, dt):

        for change_date in self.dates_to_ratio.__reversed__():
            if dt > change_date:
                return self.dates_to_ratio[change_date];

        return None

    def get_value(self, point_code) -> float:
        value = 0

        response = self.get_from_engie(point_code)

        parsed = response.json()
        response = requests.get(parsed["Items"][0]["Links"]["Self"], auth=(self.user, self.pw))
        # print(parsed["Items"][0]["Links"]["Self"])

        parsed = response.json()
        response = requests.get(parsed["Links"]["Value"], auth=(self.user, self.pw))

        return response.json()["Value"]
        # print(parsed_self["Links"])

    def sum_energy_load(self):
        for key in self.consumption_values_dict:
            if key == "oakdale_diesel":
                self.consumption_values_dict[key] = self.get_value((self.consumption_points_dict[key])) / 1000
            else:
                self.consumption_values_dict[key] = self.get_value(self.consumption_points_dict[key])
        values_list = self.consumption_values_dict.values()

        return sum(values_list)

    def get_page_json(self, url):
        self.page_get_counter += 1
        return requests.get(url, auth=(self.user, self.pw)).json()

    def get_factor(self, gas_type):
        if (gas_type in self.gas_values_that_need_to_be_scaled_up):
            return 1000
        return 1

    def day_sum_gas_consumption(self, gas_type, days_ago):

        factor = self.get_factor(gas_type)
        recorded_url = 'recorded/?startTime=-{}d&endTime=-{}d'.format(days_ago, days_ago + 1)
        interpolation_url = 'interpolated/?startTime=-{}d&endTime=-{}d&interval=1h'.format(days_ago, days_ago + 1)
        value_url = 'value/?time=-{}d'.format(days_ago)
        response = self.get_page_json(self.root_url + gas_type)

        response = self.get_page_json(response["Items"][0]["Links"]["Self"])

        if gas_type[0:2] != "gg":
            response = self.get_page_json(
                response["Links"]["InterpolatedData"].replace('interpolated', interpolation_url))
        elif gas_type[0:2] == 'gg':
            response = self.get_page_json(response["Links"]["RecordedData"].replace('recorded'), recorded_url)
        elif (gas_type == self.gas_points_dict["b11_gas_day"]):
            response = self.get_page_json(response["Links"]["Value"].replace('value', value_url))
            self.gas_values.append(response['Value']*self.gas_conversion_factor)
            sum += response['Value']
            return sum * self.gas_conversion_factor
        else:
            pass

        items = response["Items"]
        sum = 0;
        for i in range(1, len(items)):
            item = items[i]["Value"]

            if item < 0:
                item = 0

            sum = sum + (factor * item)
            self.gas_values.append(item*factor*self.gas_conversion_factor)

        # print(gas_type + ": " + str(sum) + "(factor: " + str(factor) + ")")
        # CHANGE

        # print('Gas number '+ str((sum + self.sum_oakdale_boilers_daily(days_ago) + self.oakdale_gas_engine_consumption(days_ago)) * self.gas_conversion_factor))

        result = (sum) * self.gas_conversion_factor


        return result



    def sum_one_oakdale_boiler(self, boiler, days_ago):

        interpolation_url = 'interpolated/?startTime=-{}d&endTime=-{}d&interval=1d'.format(days_ago, days_ago + 1)
        response = self.get_page_json(self.root_url + boiler)
        response = self.get_page_json(response["Items"][0]["Links"]["Self"])
        response = self.get_page_json(response["Links"]["InterpolatedData"].replace('interpolated', interpolation_url))

        items = response["Items"]
        return items[0]["Value"] * 24
        sum = 0;
        for i in range(1, len(items)):
            item = items[i]["Value"]

            if item < 0:
                item = 0

            sum = sum + item
        return sum * 24

    def sum_oakdale_boilers_daily(self, days_ago):
        sum = 0;
        for boiler in self.oakdale_gas_points_dict:
            append_sum = self.sum_one_oakdale_boiler(self.oakdale_gas_points_dict[boiler], days_ago)
            self.oakdale_boiler_values.append(append_sum/0.8*1.07*self.gas_conversion_factor)
            sum+=append_sum
        return sum / 0.8 * 1.07 * self.gas_conversion_factor

    def oakdale_gas_engine_consumption(self, days_ago):

        interpolated_url = 'interpolated/?startTime=-{}d&endTime=-{}d&interval=1d'.format(0, days_ago + 1)
        response = self.get_page_json(self.root_url + "Oak_FIT041")

        response = self.get_page_json(response["Items"][0]["Links"]["Self"])

        response = self.get_page_json(response["Links"]["InterpolatedData"].replace('interpolated', interpolated_url))

        items = response["Items"]
        sum = 0;
        for i in range(1, len(items)):
            item = items[i]["Value"]

            if item < 0:
                item = 0

            sum = sum + item
            self.oakdale_engine_values.append(item*24*self.gas_conversion_factor)

        return sum * 24 * self.gas_conversion_factor

    def sum_daily_pellets_consumption(self,days_ago):
        interpolated_url = 'interpolated/?startTime=-{}d&endTime=-{}d&interval=1d'.format(0, days_ago + 1)
        response = self.get_page_json(self.root_url + "PP_CHS_B10WeighBelt_MvgAvg")
        response = self.get_page_json(response["Items"][0]["Links"]["Self"])
        response = self.get_page_json(response["Links"]["InterpolatedData"].replace('interpolated', interpolated_url))

        items = response["Items"]
        sum = 0;
        for i in range(1, len(items)):
            item = items[i]["Value"]

            if item < 0:
                item = 0

            sum = sum + item
            self.pellets_values.append(item/2*self.pellet_conversion_factor)
        # print("Thousands of pounds of pellets total: " + str(sum))
        return sum / 2 * self.pellet_conversion_factor * 24

    def extract_datetime_from_timestamp(self, timestamp: str):
        year = int(timestamp[0:4])
        month = int(timestamp[5:7])
        day = int(timestamp[8:10])
        return datetime.datetime(year, month, day)

    def sum_daily_coal_and_pellet_consumption(self, days_ago):
        interpolation_url = 'interpolated/?startTime=-{}d&endTime=-{}d&interval=1d'.format(0, days_ago + 1)
        response = self.get_page_json(self.root_url + "PP_SF-WIT-6044A")
        response = self.get_page_json(response["Items"][0]["Links"]["Self"])
        response = self.get_page_json(response["Links"]["InterpolatedData"].replace('interpolated', interpolation_url))

        items = response["Items"]
        sum = 0;
        pellets = 0
        coal = 0
        append_sum = 0;
        for i in range(1, len(items)):
            item = items[i]["Value"]
            date = self.extract_datetime_from_timestamp(items[i]["Timestamp"])
            #print("Item: " + str(item))
            if type(item) is float:
                if item < 0:
                    item = 0
                ratio = self.get_ratio_from_date(date)

                pellets += item * ratio  # pellets

                coal += item * (1 - ratio)  # coal
                self.coal_pellets_values.append(item*ratio*self.pellet_conversion_factor/2+item*(1-ratio)*self.coal_conversion_factor/2)
            else:
                self.coal_pellets_values.append(0)

        sum += pellets * self.pellet_conversion_factor / 2
        sum += coal * self.coal_conversion_factor / 2
        # print("Coal amount: " + str(coal))
        # print("Pellets amount: " + str(pellets))
        return sum * 24

    def sum_all_fuels(self, days_ago):
        global burner_name
        gas_value = 0
        pellets_value = 0
        coal_pellets_value = 0

        for dict in self.all_fuels_dict:
            self.start_timer()
            for burner_name in self.all_fuels_dict[dict]:

                curr = 0
                if dict == 'gasses':
                    add_value = self.day_sum_gas_consumption(self.all_fuels_dict[dict][burner_name], days_ago)
                    gas_value += add_value
                    add_value=0

                elif dict == 'pellets':
                    gas_add_value = self.sum_daily_pellets_consumption(days_ago)
                    pellets_value += gas_add_value
                elif dict == 'coal+pellets':
                    add_value = self.sum_daily_coal_and_pellet_consumption(days_ago)
                    coal_pellets_value += add_value
            self.print_elapsed_time(dict + "had " + "number of page calls: " + str(self.page_get_counter))
        gas_value += self.sum_oakdale_boilers_daily(days_ago) + self.oakdale_gas_engine_consumption(days_ago)

        # heat conversion constant and carbon factor
        return gas_value, pellets_value, coal_pellets_value

    def get_points_over_time(self, days):

        values = self.sum_all_fuels(days)



def main():
    read = Reader();

    results = read.sum_all_fuels(365)
    print("Gas values(Kg CO2): "+ str(read.gas_values))
    print("Pellets values(Kg CO2): " + str(read.pellets_values))
    print("Coal/Pellets mixture values(Kg CO2): " + str(read.coal_pellets_values))
    #print(str(year_1))
    print("Number of times APi was queried: " + str(read.page_get_counter))
    print("Yearly gas total "+str(results[0]))
    print("Yearly pellets total "+str(results[1]))
    print("Yearly coal/pellets total "+str(results[2]))
    print("Yearly total energy in MW"+str(read.sum_energy_load()))



if __name__ == "__main__":

    main()
