import os
import mne
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import font_manager
import matplotlib.pyplot as plt
import seaborn as sns
#前提
plt.rcParams['axes.unicode_minus'] = False
#plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字
matplotlib.use('Qt5Agg')  #交互
# 确认目录
os.chdir("D:/222experiment_material/EEG_DATA")   #修改当前工作目录
# print(os.getcwd()) #获取当前工作目录

#导入Epoches
file_epoch = './practice/wx_lkm/wx_epo.fif'
epochs = mne.read_epochs(file_epoch)
# 检查基本信息以及数据集
#epochs.info
#  mne.read_events(file_epoch,return_event_id=True)  # 检查事件
#epochs.copy().resample(sfreq=125) # 重降采样率，同时也能看事件

# 平均叠加，
onno = epochs['no_pain'].average()
onpa = epochs['pain'].average()


# 一些可视化函数


# onno.plot_topomap(times=[-0.2, 0.1, 0.4], average=0.05)   #可视化不同时段的地形图
# onno.plot_joint()   # 时域图与地形图结合


fig, ax = plt.subplots()
ax.plot(onno.times, onno.data[0] , color='lime')
ax.set(xlabel='Time (s)', ylabel='µV', title='EEG')


