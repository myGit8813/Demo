import logging;
import time;

#import pymysql;
import xlrd;
#from influxdb import InfluxDBClient

hws_logname = 'SmartTest.xls';
source_data_url = 'time.txt'
time_format = '%Y年%m月%d日-%H时%M分%S秒'
mysql_format = '%Y-%m-%d %H:%M:%S'
influx_format = '%Y-%m-%dT%H:%M:%SZ'
last_time = 0;

month_table = 201712
# connect = pymysql.Connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='ucorespace@2017',
#     db='test',
#     charset='utf8'
# )
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y %H:%M:%S',
                    filename='dail.log',
                    filemode='w'
                    )


def read_curr_time():
    f = open(source_data_url)
    str = f.readline();
    return int(str)


def write_curr_time(curr_time):
    f = open(source_data_url, "w")
    f.write(str(curr_time))


def str_to_utc(time_str):
    #print(time_str)
    time_s = time.strptime(time_str, time_format)
    utc_time = int(time.mktime(time_s))
    # print(utc_time)
    return utc_time


def read_data():
    wb = xlrd.open_workbook(hws_logname, encoding_override="cp1252")
    table = wb.sheet_by_name('拨测结果')
    nrows = table.nrows
    ncols = table.ncols
    curr_time = read_curr_time()
    print(str(curr_time))
    for i in range(1, nrows):
        project = "华为公有云"
        name = table.cell(i, 1).value
        id = table.cell(i, 2).value
        time_strs = table.cell(i, 3).value
        duration = table.cell(i, 4).value
        result = table.cell(i, 5).value
        utc_time = str_to_utc(time_strs)
        if utc_time > curr_time:
            if i == 1:
                temp_time = utc_time
                write_curr_time(temp_time)
            #print(time_strs)
            logging.info('The message is:'+project+name+id+time_strs+duration+result)
            # save_to_mysql(project, name, id, time_strs, duration, result)
            # save_to_influxdb(project, name, id, time_strs, duration, result)
        else:
            break;


# def create_table(table_name):
#     sql = "CREATE TABLE IF NOT EXISTS %s (project VARCHAR(50),test_name VARCHAR (100),test_id VARCHAR (100),time_strs VARCHAR (50),duration VARCHAR (50),result VARCHAR (50)) " % table_name
#     crusor = connect.cursor()
#     crusor.execute(sql)
#     connect.commit()
#
#
# def save_to_mysql(project, name, id, time_strs, duration, result):
#     time_s = time.strptime(time_strs, time_format)
#     mysql_time = time.strftime(mysql_format, time_s)
#     print(project + name + id + time_strs + duration + result)
#     table_name = "dialResult" + str(time_s.tm_year) + str(time_s.tm_mon);
#     create_table(table_name)
#     #
#     sql = "insert into %s VALUES ('%s', '%s', '%s', '%s', '%s','%s' )" % (
#         table_name, project, name, id, mysql_time, duration, result)
#     crusor = connect.cursor();
#     crusor.execute(sql)
#     connect.commit()


# def save_to_influxdb(project, name, id, time_strs, duration, result):
#     time_s = time.strptime(time_strs, time_format)
#     influx_time = time.strftime(influx_format, time_s)
#     client = InfluxDBClient('10.185.54.248', 8086, 'root', 'ucorespace@2017', 'dialtest')
#     json_body = [
#         {
#             "measurement": "dialresult",
#             "tags": {
#                 "project": project,
#                 "result": result,
#             },
#             "time": influx_time,
#             "fields": {
#                 "name": name,
#                 "id": id,
#                 "duration": duration
#             }
#         }
#     ]
#     client.write_points(json_body)
    # showDatas(client)
    # print(client.query('show measurements;'))
if __name__ == "__main__":
    # save_to_influxdb('华为公有云', 'DataReport_001_001', '001', '2017年12月18日-16时46分45秒', '38s', 'Pass')
    # client = InfluxDBClient('10.185.54.248', 8086, 'root', 'ucorespace@2017', 'dialtest')
    # showDatas(client)
    while True:
        read_data()
        time.sleep(90)
