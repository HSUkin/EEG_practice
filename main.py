# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



import os
import mne
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import font_manager
import matplotlib.pyplot as plt
import seaborn as sns
from EEG import preprocessing


matplotlib.use('Qt5Agg')  # 交互
os.chdir("D:/222experiment_material/EEG_DATA")  # 修改当前工作目录

channel_ref = ['E57','E100']
time = {
    'min':-0.2,
    'max':1
}
save_path = "D:/222experiment_material/EEG_DATA/lkm_epo/"
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for i in range(1,4):
        file_path = './practice/lkm_p_raw/pain_{0}.mff'.format(i)
        raw = mne.io.read_raw_egi(file_path)
        # 注释
        raw = preprocessing.annotation(raw)
        # 滤波和降采样
        raw_filter = preprocessing.filter_resample(raw, 250)
        # 插值坏导
        raw_bad = preprocessing.handle_bad(raw_filter)
        # 重参考与初步剔除坏段
        raw_reference = preprocessing.reference(raw_bad,channel_ref)
        #ICA
        raw_ica = preprocessing.ica_analyze(raw_reference)
        #raw_ica.save(save_path+'.finic_{0}_raw.fif'.format(i))  # 保存ICA处理后文件
        #分段
        epochs = preprocessing.epo_split(raw_ica,time)
        #epochs.save(save_path+'{0}_epo.fif'.format(i))  # 保存分段文件
        plt.close('all')































# See PyCharm help at https://www.jetbrains.com/help/pycharm/
