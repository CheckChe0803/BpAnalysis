from load_file import SensorData
from plot import Plot
from pre_process import *
from pre_process import _scale

if __name__ == '__main__':

    sensor = SensorData()
    numbers = sensor.get_record_number()

    for k in numbers:
        print('regular ---> ' + str(k))
        df = sensor.load_by_number(k, 'regular')
        ###################################################################
        # 原始数据
        plt.figure(figsize=(10, 8))
        fig1 = plt.subplot(211)
        plt.plot(df.ir1, c='b')
        Plot.figture_update(fig1, 'Time (s)', 'Amplitude', 'Raw PPG signal', df.ir1)
        ###################################################################
        # 处理数据
        # df = remove_dc(df)
        # df = filter(df)
        # df = scale(df)
        df.ir2 = _scale(df.ir2)
        #df = mean_filter(df)
        #df = reverse(df)
        ###################################################################
        # 结果数据
        fig2 = plt.subplot(212)
        plt.plot(df.ir1, c='r')
        Plot.figture_update(fig2, 'Time (s)', 'Amplitude', 'Pre-process PPG signal', df.ir1)
        plt.subplots_adjust(wspace=0, hspace=0.5)
        # plt.show()
        ###################################################################
        # 存储文件
        sensor.resave_file(k, df, 'regular')
        ###################################################################