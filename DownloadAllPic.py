#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : FutureXML
@Time : 2017/8/10 14:59
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : DownloadAllPic.py
@desc :
"""
import os
import sys
import logging
import traceback
import json
import time
import argparse
import requests
from PIL import Image

from tools.utils import *

d_log = logging.getLogger(__file__)
d_log.propagate = False

s_handler = logging.StreamHandler(stream=sys.stderr)
file_formatter = logging.Formatter('%(levelname)s－%(asctime)s-%(filename)s-[line:%(lineno)d]-%(message)s')
s_handler.setFormatter(file_formatter)
d_log.addHandler(s_handler)
d_log.setLevel(logging.INFO)


def png2jpg(in_file):
    f, e = os.path.splitext(in_file)
    outfile = f + ".jpg"
    if in_file != outfile:
        im = Image.open(in_file)
        im.convert('RGB').save(outfile, 'JPEG')


def download_pic_file(in_url, out_file_name):
    try:
        ret = requests.get(in_url, stream=True)
        if ret.status_code == 200:
            with open(out_file_name, 'wb') as f:
                for chunk in ret.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            png2jpg(out_file_name)
            rm_file(out_file_name)
            return True
        else:
            logging.error('download <{}>, http error num <{}>'.format(in_url, ret.status_code))
            return False
    except:
        logging.error('download <{}>, error reason <{}>'.format(in_url, traceback.format_exc()))
        return False


def loop_dir_download_pic(target_dir):
    for r_path, m_path, files in os.walk(target_dir):
        if os.path.basename(r_path) == 'image':
            for xi in files:
                if xi == PIC_JSON_FILE:
                    # need to download file, delete json file
                    try:
                        with open(os.path.join(r_path, PIC_JSON_FILE), encoding='utf-8') as pf:
                            f_dict = json.load(pf)
                            for k, v in f_dict:
                                ret_val = download_pic_file(v, os.path.join(r_path, k))
                                if ret_val:
                                    rm_file(os.path.join(r_path, PIC_JSON_FILE))
                                    break
                                else:
                                    logging.warning('please run this script again, douche bag!!!')
                                    sys.exit()
                    except:
                        logging.error('file <{}> error, reason <{}>'.
                                      format(os.path.join(r_path, PIC_JSON_FILE), traceback.format_exc()))


def loop_check_exist_json_file(target_dir):
    for r_path, m_path, files in os.walk(target_dir):
        if os.path.basename(r_path) == 'image':
            for xi in files:
                if xi == PIC_JSON_FILE:
                    logging.info('please check the file <{}>'.format(os.path.join(r_path, PIC_JSON_FILE)))


if __name__ == '__main__':
    arg_p = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                    usage='python3 %(prog)s ../path/target_dir mode'
                                          ' \n----mode(download if mode=0, check pic if mode=1)',
                                    description='For example: \n\tpython3 {} ../path/target_dir mode'
                                                ' \n----mode(download if mode=0, check pic if mode=1)'
                                    .format(os.path.basename(sys.argv[0])))
    arg_p.add_argument('target_dir', type=str, nargs=1, help='input target dir including all yielded file')
    arg_p.add_argument('mode', type=int, nargs=1, choices=[0, 1],
                       help='select mode to download or check any pic that need to download')
    input_paras = arg_p.parse_args()
    if int(input_paras.mode[0]) == 0:
        try:
            if os.path.exists(input_paras.target_dir[0]) and os.path.isdir(input_paras.target_dir[0]):
                t_dir = os.path.normpath(input_paras.target_dir[0])
                loop_dir_download_pic(t_dir)
            else:
                logging.error('please check target directory, think twice!!!')
        except:
            logging.error('error reason <{}>'.format(traceback.format_exc()))
    elif int(input_paras.mode[0]) == 1:
        if os.path.exists(input_paras.target_dir[0]) and os.path.isdir(input_paras.target_dir[0]):
            t_dir = os.path.normpath(input_paras.target_dir[0])
            loop_check_exist_json_file(t_dir)
        else:
            logging.error('please check target directory, think twice!!!')
