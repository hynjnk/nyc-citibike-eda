#!/usr/bin/python3
# written by Hyunjoon Kim
import csv
import os
import datetime as dt
import matplotlib
#for cli
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def filepath(year, month, city='nyc', data_dir='data'):
    """
    return filepath
    """
    if city == 'nyc':
        return os.path.join(data_dir, filename_nyc(year, month))
    else:
        raise ValueError("Undefined City! : ", city)


def filename_nyc(year, month):
    """
    input:
        year, month : int
    return:
        string
    ~ 2014-08
    "YYYY-MM - Citi Bike trip data.csv"
    2014-09 ~ 2017-12
    "YYYYMM-citibike-tripdata.csv"
    2018-01 ~ 2018-03
    "YYYYMM-citibikenyc_tripdata.csv"
    2018-04 ~
    "YYYYMM-citibike-tripdata.csv"
    """
    if int(year) < 2014 or ((int(year) == 2014) and (int(month) <= 8)):
        filename = "{0:04d}-{1:02d} - Citi Bike trip data.csv".format(year, month)
    #elif year == 2018 and month <= 3 :
        #filename = "{0:04d}{1:02d}_citibikenyc_tripdata.csv".format(year, month)
    else:
        filename = "{0:04d}{1:02d}-citibike-tripdata.csv".format(year, month)
    return filename


def refresh_station_dict(station_id, name, lat, lon, year, month, station_dict):
    latest_use_date = dt.date(year, month, 1).toordinal()
    if station_id in station_dict:
        station_dict[station_id][5] = latest_use_date
    else:
        station_dict[station_id] = [station_id, name, lat, lon, latest_use_date, latest_use_date]
    return station_dict


def append_station_dict(year, month, station_dict):
    with open(filepath(year, month)) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            station_dict = refresh_station_dict(row[3], row[4], row[5], row[6], year, month, station_dict)
            station_dict = refresh_station_dict(row[7], row[8], row[9], row[10], year, month, station_dict)
    return station_dict


def make_station_dict(start_year, start_month, end_year, end_month):
    station_dict = {}
    start = dt.date(start_year, start_month, 1)
    end = dt.date(end_year, end_month, 1)
    tmp = start
    while tmp < end:
        print("append_station_dict {}-{}".format(tmp.year, tmp.month))
        station_dict = append_station_dict(tmp.year, tmp.month, station_dict)
        if tmp.month == 12:
            tmp = dt.date(tmp.year + 1, 1, 1)
        else:
            tmp = dt.date(tmp.year, tmp.month + 1, 1)
    return station_dict


def save_station_dict_csv(station_dict):
    with open("station_info.csv", "w") as f:
        fn = ['station id', 'station name', 'station latitude', 'station longitude', 'first usage', 'lastest usage']
        writer = csv.DictWriter(f, fieldnames=fn)
        writer.writeheader()
        for i, v in station_dict.items():
            print(v)
            writer.writerow({fn[0]: v[0], fn[1]: v[1], fn[2]: v[2], fn[3]: v[3], fn[4]: v[4], fn[5]: v[5]})


def make_tripduration_list(year, month):
    with open(filepath(year, month)) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        td = []
        for row in reader:
            td.append(int(row[0]))
    '''
    with open(filepath(year, month)) as csvfile:
        reader = csv.DictReader(csvfile)
        td = []
        for row in reader:
            try:
                td.append(int(row["tripduration"]))
            except:
                td.append(int(row["Trip Duration"]))
    #print(td[0:6])
    '''
    return td


def plot_month_tripduration(year, month):
    td = make_tripduration_list(year, month)
    filename = 'tripduration_{0:d}{1:02d}.png'.format(year, month)

    fig = plt.figure()
    plt.title("Trip distribution {0:d}-{1:02d}".format(year, month))
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(td, bins=60, range=(0, 2500))
    ax.set_xlabel("Trip duration (s)")
    ax.set_ylabel("Counts")

    plt.savefig(filename)
    print(" End to plot '{}'".format(filename))

if __name__ == "__main__":
    station_dict = make_station_dict(2013, 7, 2014, 9)
    print("aaa")
    save_station_dict_csv(station_dict)
    """
    for j in range(2015, 2017):
        for i in range(12):
            plot_month_tripduration(j, i+1)
    """
