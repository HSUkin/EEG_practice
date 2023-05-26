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
from EEG import erp_analyze

matplotlib.use('Qt5Agg')  # 交互
read_data_path = r"D:\222experiment_material\EEGpy\data"
os.chdir(read_data_path)  # 修改当前工作目录
save_path = "./lkm/lkm_epo"


channel_ref = ['E57','E100']
time = {
    'min':-0.2,
    'max':1
}



if __name__ == '__main__':
    # #  数据导入
    # folder_path = './lkm/lkm_p_raw'
    # file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mff')]
    # #预处理
    # for i,file_path in zip(range(1,4),file_list):
    #     raw_ica = preprocessing.ppc_ica(file_path,channel_ref)
    #     raw_ica.save(save_path + 'finic_{0}_raw.fif'.format(i))  # 保存ICA处理后文件
    #     epoch  = preprocessing.ppc_epoch(raw_ica,time)
    #     plt.close('all')
    #     epoch.save(save_path+'{0}_epo.fif'.format(i))  # 保存分段文件

    # ERP
    # 参数设置
    df = pd.DataFrame(columns=['sub', 'condition', 'channel', 'latency', 'Amplitude'])
    nplist = []
    palist = []
    list_epochs = []
    condition_name = ['nopa', 'pain']
    cp = ['E55', 'E37', 'E42', 'E47', 'E87', 'E93', 'E98']
    folder_epo = './lkm/lkm_epo'
    epofile_list = [os.path.join(folder_epo, f) for f in os.listdir(folder_epo) if f.endswith('_epo.fif')]
    # 预处理
    for i, file_path in zip(range(1, 4), epofile_list):
        epochs,new_df = erp_analyze.ANAL_ERP(i,file_path,cp,df)
        df = new_df
        list_epochs.append(epochs)
        # nplist.append(evoke1)  # 执行这个命令需要返回nopa,pain
        # palist.append(evoke2)
    nopa,pain=erp_analyze.get_condition_epolist(list_epochs)
    ek_nopa_list = erp_analyze.get_condition_evoke(nopa)
    ek_pain_list = erp_analyze.get_condition_evoke(pain)
    epos = [ek_nopa_list,ek_pain_list]
    erp_analyze.plot_compare(epos,condition_name,cp)
    plt.close('all')

    # # 受试者平均对比
    # evokes = [nplist,palist]
    # erp_analyze.plot_subwise_compare(evokes, condition_name,cp)
    # plt.close('all')












