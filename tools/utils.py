#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : FutureXML
@Time : 2017/7/26 16:40
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : utils.py
@desc :
"""
import os
import sys
import traceback
import platform
import logging
import shutil
import threading
from urllib.parse import urlparse
import requests
import subprocess
import json
import re

__author__ = 'achilles_xushiyin'

SIZE_TYPE = ['small', 'medium', 'big']

sample_url = 'http://images.center.bcs.ottcn.com:8080/poster/2016-12-14/996b4cb5ec0647749db058877ea1eefc.jpg'
sample_file = 'C:\\Users\\admins\\Desktop\\20170215\\sd_zy_aphts_20111011_1280x720_2500k.ts'

q_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    "Connection": "close"
}


def get_http_file_name(src_url):
    url_output = urlparse(src_url)
    url_path = url_output.path
    file_name = os.path.basename(url_path)
    return file_name


def pic_file_download_txt(down_url_dict, p_dir):
    file_d = '{}/pic_download.json'.format(p_dir)
    j_str = json.dumps(down_url_dict, ensure_ascii=False)
    with open(file_d, mode='w', encoding='utf-8') as pf:
        pf.write(j_str)


def get_resolution_bit_rate_new_name(file_name, real_name):
    exe_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if platform.system() == 'Windows':
        cmd_str = "{}\\ffprobe.exe -v quiet -of json -show_format -show_streams -i ".format(exe_dir)
    else:
        cmd_str = "ffprobe -v quiet -of json -show_format -show_streams -i "
    # get complete cmd str
    cmd_str = cmd_str + file_name
    suffix_name = os.path.basename(file_name).split('.')[-1]
    # logging.info(cmd_str)
    with subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pp:
        std_out, std_err = pp.communicate()
        std_err = std_err.decode('utf-8', 'replace')
        std_out = std_out.decode('utf-8', 'replace')
        msg = std_err.strip().split('\n')[-1]

        if msg:
            logging.error('video <{}> parse error, reason <{}>'.format(file_name, msg))
            return '', '', '', ''
        else:
            try:
                width = '0'
                height = '0'
                bit_rate = '0'
                j_obj = json.loads(std_out)
                for stream in j_obj['streams']:
                    if stream['codec_type'] == 'video':
                        if 'width' in stream.keys():
                            width = stream['width']
                        if 'height' in stream.keys():
                            height = stream['height']
                if 'bit_rate' in j_obj['format'].keys():
                    bit_rate = j_obj['format']['bit_rate']
                if bit_rate == '0':
                    bit_rate = 0
                else:
                    bit_rate = int(bit_rate)//1024

                # if 500 <= bit_rate <= 1200:
                #     bit_rate = 800
                # elif 1200 < bit_rate <= 1800:
                #     bit_rate = 1500
                # elif 1800 < bit_rate <= 10000:
                #     bit_rate = 7500
                # else:
                #     pass
                bit_rate = str(bit_rate)
                res_str = real_name + '_' + str(width) + 'x' + str(height) + '_' + bit_rate + 'k.' + suffix_name
                return res_str, width, height, bit_rate
            except:
                logging.error('ffprobe json error, error file <{}>, reason--<{}>'.format(file_name,
                                                                                         traceback.format_exc()))
                return '', '', '', ''


def mk_dir(dir_name):
    try:
        os.mkdir(dir_name)
    except Exception:
        logging.error(traceback.format_exc())


def rm_file(file_name):
    try:
        os.remove(file_name)
    except Exception:
        logging.error(traceback.format_exc())


def mv_files_to_dir(src, dst):
    if isinstance(src, list):
        for x in src:
            try:
                shutil.move(x, dst)
            except IOError:
                logging.error(traceback.format_exc())
    else:
        try:
            shutil.move(src, dst)
        except IOError:
            logging.error(traceback.format_exc())


def copy_file_to_dir(src, dst):
    try:
        shutil.copyfile(src, dst)
    except IOError:
        logging.error(traceback.format_exc())

R_pattern = r'_\d+x\d+_\d+k.'
F_name = 'sd_zy_zzxe10_20120807_1280x720_1500k.ts'


def rename_file_bat(dir_name):
    for d_root, ds, file_list in os.walk(dir_name):
        pass
    for src in file_list:
        dst_str = re.sub(R_pattern, '.', src, flags=re.IGNORECASE)
        os.rename('{}/{}'.format(d_root, src), '{}/{}'.format(d_root, dst_str))


if __name__ == '__main__':
    # pic_file_download(sample_url, '菜花.jpg', 'C:\\Users\\admins\\Desktop\\20170215')
    # ret_name, r_width, r_height, r_bit_rate = get_resolution_bit_rate_new_name(sample_file, '菜花')
    # print(ret_name, r_width, r_height, r_bit_rate)
    # smalll_t = threading.Thread(target=pic_file_download,
    #                            args=(sample_url, 'small.jpg', 'C:\\Users\\admins\\Desktop\\20170215'))
    # # small_t = threading.Thread(target=print, args=('hello', 'C:\\Users\\admins\\Desktop\\20170215'))
    # smalll_t.setDaemon(daemonic=True)
    # smalll_t.start()
    # print('ok')
    # print((freeproxy.read_proxies()))
    # rename_file_bat(sys.argv[1])
    vi_file = 'D:\\Castlevania.S01E01.mp4'
    get_resolution_bit_rate_new_name(vi_file, 'test')


