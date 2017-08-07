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
from collections import OrderedDict
from lxml import etree

from tools.XmlWriter import yield_target_xml_file
from tools.XmlParser import XmlParser, XMLParserCategory, XMLParserCateSer
from tools.utils import *

INPUT_FILE = 'C:\\Users\\admins\\Desktop\\20170721\\fullData20170721.xml'
INPUT_FILE1 = 'C:\\Users\\admins\\Desktop\\20170721\\cat20170721.xml'
INPUT_FILE2 = 'C:\\Users\\admins\\Desktop\\20170721\\cat2ser20170721.xml'

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
    pf = open('C:\\Users\\admins\\Desktop\\20170721\\reco_name.txt', mode='w', encoding='utf-8')
    if os.path.exists(input_file):
        print('{file} exist'.format(file=input_file))
        try:
            doc = etree.ElementTree(file=input_file)
        except:
            logging.error('{}'.format(traceback.format_exc()))
            sys.exit()

        x_cat = XMLParserCategory()
        x_cat_ser = XMLParserCateSer()
        ret_value = x_cat.check_xml_file_valid(INPUT_FILE1)
        if not ret_value:
            logging.error('please confirm {}'.format(INPUT_FILE1))
            sys.exit()
        ret_value = x_cat_ser.check_xml_file_valid(INPUT_FILE2)
        if not ret_value:
            logging.error('please confirm {}'.format(INPUT_FILE2))
            sys.exit()
        try:
            x_cat.get_cat_dict()
        except:
            logging.error('category <{}> yield failed, error <{}>'.format(INPUT_FILE1, traceback.format_exc()))
            sys.exit()
        try:
            x_cat_ser.get_cat_dict()
        except:
            logging.error('category <{}> yield failed, error <{}>'.format(INPUT_FILE2, traceback.format_exc()))
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
            i_id = child.find('id').text
            pro_name = child.find('name').text
            total_num = child.find('programTotalCount').text

            cat_id = x_cat_ser.big_dict[i_id][1]
            pp_name = x_cat_ser.big_dict[i_id][0]
            try:
                cat_item_name = x_cat.cat_dict[x_cat_ser.big_dict[i_id][1]][1]
            except:
                print('{}--{}--{}'.format(i_id, pp_name, cat_id))
                cat_item_name = x_cat.p_cat_dict[cat_id]

            pf.write('{}+++++total-{}---{}---{}\n'.format(pro_name, total_num,
                                                          cat_id,
                                                          cat_item_name))
            programs_node = child.find('programs')
            program_node_list = list(programs_node)
            for p in program_node_list:
                p_name = p.find('programName').text
                p_part_num = p.find('partNum').text
                pf.write('\t{}--------{}\n'.format(p_name, p_part_num))
    else:
        print('{file} not exist!!!'.format(file=input_file))
    pf.close()


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


def parse_main_entrance():
    """
    解析工具主入口
    :return:
    """
    ret_dict = read_json_file()
    if not ret_dict:
        sys.exit()
    xml_file_name = ret_dict.get('full_data_xml', '')
    cat_xml_name = ret_dict.get('category_xml', '')
    cat_ser_xml_name = ret_dict.get('category_serial_xml', '')
    meta_type_dict = ret_dict.get('META_TYPE_DICT', '')
    if not all((xml_file_name, cat_xml_name, cat_ser_xml_name, meta_type_dict)):
        logging.error('please confirm xml path in json config file')
        sys.exit()

    x_p = XmlParser()
    x_cat = XMLParserCategory()
    x_cat_ser = XMLParserCateSer()
    ret_value = x_p.check_xml_file_valid(xml_file_name)
    if not ret_value:
        logging.error('please confirm {}'.format(xml_file_name))
        sys.exit()
    ret_value = x_cat.check_xml_file_valid(cat_xml_name)
    if not ret_value:
        logging.error('please confirm {}'.format(cat_xml_name))
        sys.exit()
    ret_value = x_cat_ser.check_xml_file_valid(cat_ser_xml_name)
    if not ret_value:
        logging.error('please confirm {}'.format(cat_ser_xml_name))
        sys.exit()
    try:
        x_cat.get_cat_dict()
    except:
        logging.error('category <{}> yield failed, error <{}>'.format(cat_xml_name, traceback.format_exc()))
        sys.exit()
    try:
        x_cat_ser.get_cat_dict()
    except:
        logging.error('category <{}> yield failed, error <{}>'.format(cat_ser_xml_name, traceback.format_exc()))
        sys.exit()

    # 判断路径参数，是否存在及有效
    v_dir_list = list()
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
        json_rec_dict = OrderedDict()
        now_json_dict = OrderedDict()
        x_p.get_program_serial_info(s_node)
        p_child_list = x_p.get_program_node_list(s_node)
        if p_child_list:
            for c_node in p_child_list:
                x_p.get_program_info(c_node)
                name_tuple = x_p.output_parameter()
                res_yield = yield_target_xml_file(name_tuple, v_dir_list)
                if res_yield == 'ok':
                    program_cnt += 1
                    logging.info('节目计数 {} 节目名：{}'.format(program_cnt, name_tuple.p_program_name))
        x_p.restore_inner_all_variables()


if __name__ == '__main__':
    start_time = time.time()
    # parse_main_entrance()
    test_open_xml_read_element(INPUT_FILE)
    end_time = time.time()
    logging.info('time <{used_time}> is used'.format(used_time=end_time-start_time))
