
import os
import mne
import numpy as np
import pandas as pd
import matplotlib
from matplotlib import font_manager
import matplotlib.pyplot as plt
import seaborn as sns



def filter_resample(raw,rate):
    # 滤波
    raw_filter = raw.copy()
    raw_filter.load_data()
    raw_filter.filter(l_freq=0.1, h_freq=30)
    raw_filter.notch_filter(freqs=50)
    plt.show(block=True)
    # raw_filter.plot(start=20, duration=1, block=True, title='无误请关闭窗口')
    # 降采样
    raw_filter.resample(sfreq=rate)
    return raw_filter


def annotation(raw_filter):
    sfreq = raw_filter.info['sfreq']
    events = mne.find_events(raw_filter, stim_channel='STI 014')
    oppa = mne.find_events(raw_filter, stim_channel='onpa')
    onno = mne.find_events(raw_filter, stim_channel='onno')
    if oppa[0, 2] < onno[0, 2]:
        events_dict = {
            1: 'stat',
            2: 'onpa',
            3: 'onno',
            4: 'rest'
        }
    else:
        events_dict = {
            1: 'stat',
            2: 'onno',
            3: 'onpa',
            4: 'rest'
        }

    anno = mne.annotations_from_events(events, sfreq, event_desc=events_dict, first_samp=0, orig_time=None,
                                       verbose=None)
    raw_filter.set_annotations(anno)
    return raw_filter



def handle_bad(raw_filter):
    # 查看坏导
    raw_bad = raw_filter.copy()  # 备份原数据
    raw_bad.plot(block=True, title='请选出坏导')
    # print(epoch_bad.info['bads'])
    # 插值坏导
    raw_bad.load_data()
    raw_bad.interpolate_bads()
    raw_bad.plot(block=True, title='坏导插值完成,请确认无误')
    while raw_bad.info['bads']:
        raw_bad.interpolate_bads()
        raw_bad.plot(block=True, title='检查坏导的循环')
    raw_bad.plot(block=True, title='坏导插值完成')
    return raw_bad

def reference(raw_bad,channel_list):
    raw_reference = raw_bad.copy()
    raw_reference.load_data()
    raw_reference.set_eeg_reference(ref_channels=channel_list)
    # ICA之前对通道的修正
    raw_reference.plot(block=True, title='重参考完成，按A开始选择坏段')
    # fig.fake_keypress('a')  # 注释坏段
    # 如果存在坏导对其进行重新插值
    return raw_reference

def ica_analyze(raw_reference):
    # ICA
    for_ica = raw_reference.copy().filter(l_freq=1, h_freq=None)  # 设置一个对象用来做ICA,更高频率可能更有助于筛选
    ica = mne.preprocessing.ICA(n_components=30, max_iter='auto')
    ica.fit(for_ica, reject_by_annotation=True)
    raw_reference.load_data()
    # ica.plot_components()
    # ica.plot_properties(raw, picks= [0,1,2,3,4,5,6,7,8,9])
    ica.plot_sources(raw_reference, show_scrollbars=False, title='选择需要去除的成分')
    plt.show(block=True)
    raw_ica = raw_reference.copy()
    raw_ica = ica.apply(raw_ica)
    del for_ica
    raw_reference.plot(title='ICA处理前, 确认请关闭')
    raw_ica.plot(title='ICA处理后, 确认请关闭')
    plt.show(block=True)
    # 预处理未分段数据保存
    return raw_ica

def epo_split(raw_ica,time):
    # 判断刺激标签
    event = mne.find_events(raw_ica, stim_channel='STI 014')
    oppa = mne.find_events(raw_ica, stim_channel='onpa')
    onno = mne.find_events(raw_ica, stim_channel='onno')
    if oppa[0, 2] < onno[0, 2]:
        events_id = {
            'stat': 1,
            'onpa': 2,
            'onno': 3,
            'rest': 4
        }
    else:
        events_id = {
            'stat': 1,
            'onno': 2,
            'onpa': 3,
            'rest': 4
        }
    # mne.viz.plot_events(event)
    events = [event, events_id]
    event_dict = {'no_pain': events[1]['onno'], 'pain': events[1]['onpa']}
    reject_criteria = dict(eeg=100e-6)  # 100 µV
    epochs = mne.Epochs(raw_ica, events[0], event_id=event_dict, preload=True, tmax=time['max'],
                        tmin=time['min'], reject=reject_criteria)  # 运行中基线校正自动进行了,先不拒绝100μv
    epochs.plot(events=events[0], block=True, title='请挑出坏的Epochs')
    return epochs























