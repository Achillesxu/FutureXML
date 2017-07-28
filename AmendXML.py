#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : FutureXML
@Time : 2017/7/26 16:25
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : AmendXML.py
@desc :
"""
import os
import sys
import io
import logging
import logging.handlers
import traceback
import json
import time
import argparse
from lxml import etree

from tools.XmlWriter import yield_target_xml_file
from tools.XmlParser import XmlParser
from tools.utils import *

INPUT_FILE = 'C:\\Users\\admins\\Desktop\\20170215\\fullData20170215.xml'

MY_LOG_NAME = 'file_record'
MY_LOG_FILE_NAME = '{}/file_process_record.log'.format(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s－%(asctime)s-%(filename)s-[line:%(lineno)d]-%(message)s')


r_log = logging.getLogger(MY_LOG_NAME)
r_log.propagate = False

file_info = logging.handlers.RotatingFileHandler(filename=MY_LOG_FILE_NAME, maxBytes=100*1024*1024,
                                                 backupCount=10, encoding='utf-8')
file_formatter = logging.Formatter('%(levelname)s－%(asctime)s-%(filename)s-[line:%(lineno)d]-%(message)s')
file_info.setFormatter(file_formatter)
r_log.addHandler(file_info)
r_log.setLevel(logging.INFO)


def test_open_xml_read_element(input_file):
    if os.path.exists(input_file):
        print('{file} exist'.format(file=input_file))
        try:
            doc = etree.ElementTree(file=input_file)
        except:
            logging.error('{}'.format(traceback.format_exc()))
            sys.exit()
        root = doc.getroot()
        # for child in root:
        #     print(child.tag)
        children = list(root)
        # for child in children:
        #     sub_element = child.find('programTotalCount')
        #     sub_element1 = child.find('name')
        #     print(sub_element1.text, sub_element.text)
        for child in children:
            programs_node = child.find('programs')
            program_node_list = list(programs_node)
            for p in program_node_list:
                p_name = p.find('programName').text
                medias_node = p.find('medias')
                media_node_list = list(medias_node)
                # print(p_name, 'with {} media file'.format(len(media_node_list)))
                if len(media_node_list) > 1:
                    print('{} has many medias file'.format(p_name))

    else:
        print('{file} not exist!!!'.format(file=input_file))


def read_json_file():
    json_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_dir = '{}/{}'.format(json_dir, 'parameters.json')
    if os.path.exists(json_file_dir) and os.path.isfile(json_file_dir):
        with io.open(json_file_dir, encoding='utf-8') as pf:
            try:
                para_dict = json.load(pf)
                return para_dict
            except:
                logging.error('parameters.json load error, reason--<{}>'.format(traceback.format_exc()))
                return None
    else:
        logging.error('请确认json配置文件存在')
        return None


def record_id_parent_id_in_file(i_id, i_parent_id):
    file_name = 'last_id_parent_id.txt'
    record_d = {'id': i_id, 'parent_id': i_parent_id}
    j_str = json.dumps(record_d)
    with open(file_name, mode='w', encoding='utf-8') as pf:
        pf.write(j_str)


def parse_main_entrance(in_param):
    if os.path.isfile(in_param.xml_file[0]):
        xml_file_name = in_param.xml_file[0]
        ret_dict = read_json_file()
        if not ret_dict:
            sys.exit()
        x_p = XmlParser()
        ret_value = x_p.test_xml_file_valid(xml_file_name)
        if not ret_value:
            logging.error('please confirm input big xml')
            sys.exit()
        # 判断路径参数，是否存在及有效
        v_dir_list = list()
        # TODO 检测路径是否正确
        for v_dir in ret_dict['video_dir']:
            if os.path.exists(v_dir) and os.path.isdir(v_dir):
                if v_dir[-1] is '/':
                    v_dir_list.append(v_dir[:-1])
                else:
                    v_dir_list.append(v_dir)

        if len(v_dir_list) == 0:
            logging.error('json文件内的video_dir{}--有问题，请检查'.format(ret_dict['video_dir']))
            sys.exit()

        if os.path.exists(ret_dict['target_dir']) and os.path.isdir(ret_dict['target_dir']):
            if ret_dict['target_dir'][-1] is '/':
                ret_dict['target_dir'] = ret_dict['target_dir'][:-1]
        else:
            mk_dir(ret_dict['target_dir'])

        program_cnt = 0
        for s_node in x_p.get_next_program_serial_node():
            x_p.get_program_serial_info(s_node)
            p_child_list = x_p.get_program_node_list(s_node)
            if p_child_list:
                for c_node in p_child_list:
                    x_p.get_program_info(c_node)
                    name_tuple = x_p.output_parameter()
                    # small_poster_name, medium_poster_name, big_poster_name,\
                    res_yield = yield_target_xml_file(name_tuple, v_dir_list, ret_dict['target_dir'], x_p)
                    x_p.restore_inner_program_variables()
                    if res_yield == 'ok':
                        parent_sign = True
                        program_cnt += 1
                        logging.info('节目计数 {} 节目名：{}'.format(program_cnt, name_tuple.p_program_name))

            x_p.restore_inner_all_variables()

    else:
        logging.error('please confirm input big xml')
        sys.exit()


if __name__ == '__main__':
    start_time = time.time()
    arg_parser = argparse.ArgumentParser(prog='AmendXML.py', usage='%(prog)s [options]',
                                         description='For example: \n\tpython ../path/AmendXML.py --xml_file '
                                                     '../path/xml_file.xml')
    arg_parser.add_argument('--xml_file', type=str, nargs=1, help='get info from xml')
    input_paras = arg_parser.parse_args()
    parse_main_entrance(input_paras)
    end_time = time.time()
    logging.info('time <{used_time}> is used'.format(used_time=end_time-start_time))
