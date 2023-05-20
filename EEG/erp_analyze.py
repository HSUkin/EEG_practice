

import os
import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


matplotlib.use('Qt5Agg')  # 交互
read_data_path = r"D:\222experiment_material\EEGpy\data"
os.chdir(read_data_path)  # 修改当前工作目录
save_path = "./lkm/lkm_epo"


sublist = []
conditionlist = []
channellist = []
Latencylist = []
Amplitudelist = []
nopalist = []
painlist = []





def roi_get(epochs,roi) :
    # 获取感兴趣区
    area_emo = mne.pick_channels(epochs.info['ch_names'], include=roi)
    emo_dict = {'ROI': area_emo}  # 够建虚拟通道，dict中的key就是通道的名字，常用于左右脑分离
    roi_epoch = mne.channels.combine_channels(epochs, emo_dict, method= 'mean')
    return roi_epoch

def evoke_get(epochs):
    epoch = epochs.copy()
    eid_list = list(epoch.event_id.keys())
    ek = []
    for i in range(len(eid_list)):
        x = epochs[eid_list[i]].average()
        ek.append(x)
    return ek


    # nopalist.append(no_pain)   # 通道未筛选
    # painlist.append(ek_pain)
    # # emo_dict=dict(cp=area_emo) # dict中的key就是通道的名字
    #
    #
    # # 感兴趣通道综合
    # nopa = mne.channels.combine_channels(no_pain, emo_dict, method='mean')
    # pain = mne.channels.combine_channels(ek_pain,emo_dict, method='mean')
    # good_tmin, good_tmax = 0.3, 1   # 设置时间窗，这个时间窗通常是p100发生时间段
def  data_get(i,condition,ek,time_dict,n_p):
    # 不痛苦条件
    np_ch, np_lat, np_amp = ek.get_peak(ch_type='eeg',
                                    tmin=time_dict['min'], tmax=time_dict['max'],
                                   mode=n_p, return_amplitude=True)



    np_amp = np_amp * 1e6
    # Extract mean amplitude in µV over time
    mean_amp_roi = ek.data.mean(axis=1) * 1e6  # 按时间点进行平均
    sub = i
    condition = condition
    # # Store the data in a data frame
    # mean_amp_roi_df = pd.DataFrame(
    #     {
    #         "ch_name": l_vis_mean_roi.ch_names,
    #         "hemisphere": ["left", "left", "right", "right"],
    #         "mean_amp": mean_amp_roi,
    #     }
    # )

    # # Print the data frame
    # print(mean_amp_roi_df.groupby("hemisphere").mean(numeric_only=True))
    subdata = [sub,condition,np_ch, np_lat, np_amp,mean_amp_roi]
    return subdata


# def get_df (sub,condition,data_list):
#
#
#     conditionlist.append('no_pain')
#     channellist.append(np_ch)
#     Latencylist.append(np_lat)
#     Amplitudelist.append()

    # # 痛苦条件
    # pa_ch, pa_lat, pa_amp =  pain.get_peak(ch_type='eeg',
    #                                 tmin=good_tmin, tmax=good_tmax,
    #                               mode='pos', return_amplitude=True)
    # sublist.append(i)
    # conditionlist.append('pain')
    # channellist.append(pa_ch)
    # Latencylist.append(pa_lat)
    # Amplitudelist.append(pa_amp*1e6)


# data_frame

def get_df(df,datalist):  # 一个包含单被试所有需要的数据的信息，以列表方式存储
        data = {'sub': datalist[0],
                'condition': datalist[1],
                'channel': datalist[2],
                'latency': datalist[3],
                'Amplitude': datalist[4],
                'Mean_Amp':datalist[5]
                }
        data = pd.DataFrame(data, index=[0])
        df = pd.concat([df, data], ignore_index=True)
        return df


#


# 受试者平均对比
def plot_subwise_compare(condi,clist,roi):
    list_condi = []
    condi1=0
    for i in range(len(condi)):
        for ii in range(len(condi[0])-1):
            condi1 = mne.grand_average([condi[i][ii], condi[i][ii+1]]) # 跨被试的evoke
        list_condi.append(condi1)
    evokeds = {
        clist[0]:list_condi[0],
        clist[1]:list_condi[1]
    }
    mne.viz.plot_compare_evokeds(evokeds ,picks = roi,title='ERP_mt',combine = 'mean', truncate_xaxis=False,
                                 truncate_yaxis=False )







# 此函数作用在于将所有被试的epoch分段整合为一个，不再考虑被试因素
def con_data(list_epoch):
    data_all = np.empty(shape=(0, 135, 301))  # 存储data
    for i in range(3):
        data = list_epoch[i].get_data()
        data_all = np.concatenate((data_all, data), axis=0)
    return data_all
def get_condition_epolist(list_epoch): # 传入包含所有被试的分段
    # 先按条件分
    nopa=[]
    pain=[]
    for i in range(len(list_epoch)):
        nopa.append(list_epoch[i]['no_pain'])
        pain.append(list_epoch[i]['pain'])
    return nopa,pain
def get_condition_evoke(list_nopa):
    nopa_ek = []
    for i in range(len(list_nopa)):
        nopa_ek.append(list_nopa[i].average())
    return nopa_ek





def plot_compare(epos,clist,roi):

    evokeds = {
        clist[0]: epos[0],
        clist[1]: epos[1]
    }
    mne.viz.plot_compare_evokeds(evokeds ,picks = roi,title='ERP_mt',combine = 'mean', truncate_xaxis=False,
                                 truncate_yaxis=False)




















# plt.close('all')
# # 创建文件
# data = {'sub': sublist,
#         'condition': conditionlist,
#         'channel': channellist,
#         'latency': Latencylist,
#         'Amplitude': Amplitudelist}
#
# # 使用 DataFrame() 函数创建数据帧
# df = pd.DataFrame(data)
# df.to_csv('./practice/lkm_epo/data_final/lkm_erp.csv', index=False)
#

# ERP



def ANAL_ERP(i,file_path,roi,df):
        epochs = mne.read_epochs(file_path)

        # 不同条件进行分段叠加
        #明确有哪些条件
        epoch = epochs.copy()
        eid_list = list(epoch.event_id.keys())  # 明确条件的顺序
        print(eid_list)
        eklist = evoke_get(epoch)
        nopa = eklist[0]
        pain = eklist[1]
        # 获得感兴趣区域
        roi_nopa = roi_get(nopa,roi)
        roi_pain = roi_get(pain, roi)

        # 获取数据
        # 需要的参数的调节
        erp_time_windows = {
            'min': -0.2,
            'max': 1
        }
        mode = ['pos', 'neg', 'abs']
        npdata = data_get(i,'nopa',roi_nopa,erp_time_windows,mode[0])
        padata = data_get(i,'pain',roi_pain,erp_time_windows,mode[0])
        #数据顺序：'sub', 'condition', 'channel', 'latency', 'Amplitude'，'mean_amp'

        # 形成dataframe
        np_pa_list = [npdata, padata]
        for ii in range(2):
            df = get_df(df,np_pa_list[ii])

        # 导出数据
        df.to_csv(save_path+'/data_final/lkm_erp_new.csv', index=False)

        return epochs,df





