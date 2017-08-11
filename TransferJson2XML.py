#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : FutureXML
@Time : 2017/8/10 16:40
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : TransferJson2XML.py
@desc :
"""
import os
import sys
import logging
import traceback
import json
import argparse

from tools.XmlWriter import write_future_xml
from tools.utils import *


logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s－%(asctime)s-%(filename)s-[line:%(lineno)d]-%(message)s')


def loop_transfer_json_2_xml(target_dir):
    for r_path, d_path, files in os.walk(target_dir):
        if os.path.basename(r_path) == 'xml':
            if XML_JSON_FILE in files:
                # start to produce metadata.xml
                try:
                    with open(os.path.join(r_path, XML_JSON_FILE), encoding='utf-8') as pf:
                        f_dict = json.load(pf)
                        write_future_xml(r_path, f_dict)
                except:
                    logging.error('error json <{}>, error reason <{}>'.
                                  format(os.path.join(r_path, XML_JSON_FILE), traceback.format_exc()))
                    sys.exit()


if __name__ == '__main__':
    arg_p = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                    usage='python3 %(prog)s ../path/target_dir',
                                    description='For example: \n\tpython3 {} ../path/target_dir'
                                    .format(os.path.basename(sys.argv[0])))
    arg_p.add_argument('target_dir', type=str, nargs=1, help='input target dir including all yielded file')
    input_paras = arg_p.parse_args()
    if os.path.exists(input_paras.target_dir[0]) and os.path.isdir(input_paras.target_dir[0]):
        print(input_paras.target_dir[0])
        # loop_transfer_json_2_xml(input_paras.target_dir[0])
    logging.info('all xml get!!!')


