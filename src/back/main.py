import datetime


class Main:
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





main = Main()

print(main.get_ratio_from_date(datetime.datetime(2016, 12, 22)))
