import json

from data_pipline import *

"""
SensorData  文件操作类

将传感器存储的文件转换成 DataFrame

"""

class SensorData:

    def __init__(self):
        self.data = None
        self.record = None

        self._load_record()

    def _load(self, path, form='excel'):
        self.data = self.load(path, form)

    def _load_record(self):
        self.record = pd.read_table('../old/record/test_log', header=None)
        self.record.columns = ['idx', 'name', 'file', 'h1', 'l1', 'h2', 'l2']

    @staticmethod
    def load(path, form='excel'):

        data = pd.DataFrame

        if form == 'txt':
            data = pd.read_table(path, header=None, sep=',')
        elif form == 'excel':
            data = pd.read_excel(path)

        return data

    @staticmethod
    def load_peek_index(k, default='peak_index'):
        path = SensorData._combine_path(k, default=default)
        idx = pd.read_table(path, header=None, sep=',')
        if idx.shape[1] == 1:
            idx.columns = ['ir1']
        elif idx.shape[1] == 2:
            idx.columns = ['ir1', 'ir2']
        return idx

    @staticmethod
    def _combine_path(k, default='data', form='txt'):
        return '../scene/' + default + '/' + str(k) + '.' + form

    def get_record_number(self):
        record = self.record[self.record['usage'] != 0]
        return record['number']

    def load_by_number(self, k, default='data'):
        path = SensorData._combine_path(k, default)
        return self.load(path)

    def resave_file(self, k, data, default='regular'):
        path = SensorData._combine_path(k, default)
        with open(path, 'w+') as f:
            f.seek(0)
            for i in range(data.shape[0]):
                line = data.loc[i]
                line = ','.join(str(_) for _ in line) + '\n'
                f.writelines(line)
            f.truncate()

    @staticmethod
    def load_all_index(k):
        pks = SensorData.load_peek_index(k)
        mid_pks = SensorData.load_peek_index(k, default='mid_peak_index')
        vl_pks = SensorData.load_peek_index(k, default='vally_peak_index')
        return pks, mid_pks, vl_pks

    @staticmethod
    def save_all_indicators(k, data, default='feature_point'):
        path = SensorData._combine_path(k, default)
        with open(path, 'w+') as f:
            f.seek(0)
            for i in range(len(data)):
                line = data[i]
                line = ','.join(str(_) for _ in line) + '\n'
                f.writelines(line)
            f.truncate()

    @staticmethod
    def load_feature_points(k):
        path = SensorData._combine_path(k, default='feature_point')
        data = pd.read_table(path, header=None, sep=',')
        data.columns = ['f1', 'f2', 'f3', 'f4']
        return data

    @staticmethod
    def save_metric(k, metrics):
        path = SensorData._combine_path(k, default='metric')
        with open(path, 'w+') as f:
            f.seek(0)
            tags = 'bf, bs, sd, df, sf, rr, asd, asf,ptt \n'
            f.writelines(tags)
            line = ','.join([str(_) for _ in metrics])
            f.writelines(line + '\n')
            f.truncate()

    @staticmethod
    def load_json_metric(k):
        path = SensorData._combine_path(k, default='metric', form='json')
        with open(path, 'r') as f:
            data = json.load(f)
        return data


if __name__ == '__main__':
    d = SensorData.load(path='../scene/data/2.txt')
    # print(data)
    sensor = SensorData()
    record = sensor.record

    # print(record[record['number'] > 20])
    # print(record)
    # print(sensor.get_record_number())

    # sensor.resave_file(100, data)

    print(sensor.get_record_number())
