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
from collections import OrderedDict
from lxml import etree
from contextlib import contextmanager

from tools.file_yield_and_move import get_video_and_move_to_dir, get_pic_and_write_json_to_dir
from tools.file_yield_and_move import get_programs_json_file_content, put_programs_json_file_content
from tools.file_yield_and_move import get_video_and_move_to_dir_revise
from tools.XmlParser import XmlParser, XMLParserCategory, XMLParserCateSer
from tools.utils import *

# the following variables just for testing
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
            big_pic = get_http_file_name(child.find('bigPoster').text)

            cat_id = x_cat_ser.big_dict[i_id][1]
            pp_name = x_cat_ser.big_dict[i_id][0]
            try:
                cat_item_name = x_cat.cat_dict[x_cat_ser.big_dict[i_id][1]][1]
            except:
                print('{}--{}--{}'.format(i_id, pp_name, cat_id))
                cat_item_name = x_cat.p_cat_dict[cat_id]

            pf.write('{}+++++total-{}---{}---{}----{}\n'.format(pro_name, total_num,
                                                                cat_id,
                                                                cat_item_name,
                                                                big_pic))
            programs_node = child.find('programs')
            program_node_list = list(programs_node)
            for p in program_node_list:
                p_name = p.find('programName').text
                pp_name = get_date_from_p_name(p_name[4:])
                p_part_num = p.find('partNum').text
                pf.write('\t{}--------{}\n'.format(pp_name, p_part_num))
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


def get_column_name(p_ser_id, cat_obj, cat_ser_obj):
    try:
        cat_item_name = cat_obj.cat_dict[cat_ser_obj.big_dict[p_ser_id][1]][1]
        return cat_item_name
    except KeyError:
        try:
            cat_id_ = cat_ser_obj.big_dict[p_ser_id][1]
            cat_item_name = cat_obj.p_cat_dict[cat_id_]
            return cat_item_name
        except KeyError:
            logging.error('programSerial-id---<{}> cant find column name in catxxxxxxx.xml and cat2serxxxxxxxx.xml'.
                          format(p_ser_id))
            return ''


def fill_json_dict(in_dict, xml_obj, col_name, meta_dict):
    if 'id' not in in_dict:
        in_dict['id'] = '0'
    if 'meta' not in in_dict:
        in_dict['meta'] = meta_dict[col_name][0]
    if 'title' not in in_dict:
        t_dict = {'zh': '', 'zh_hk': '', 'en': ''}
        if judge_contain_chinese_chr(xml_obj.name):
            t_dict['zh'] = xml_obj.name
        else:
            t_dict['en'] = xml_obj.name
        in_dict['title'] = t_dict
    if 'title2' not in in_dict:
        t_dict = {'zh': '', 'zh_hk': '', 'en': ''}
        in_dict['title2'] = t_dict
    if 'type' not in in_dict:
        in_dict['type'] = meta_dict[col_name][1]
    if 'category' not in in_dict:
        in_dict['category'] = xml_obj.program_class
    if 'area' not in in_dict:
        if '中国大陆' in xml_obj.zone:
            in_dict['zone'] = '大陆'
        else:
            in_dict['zone'] = xml_obj.zone
    if 'tag' not in in_dict:
        in_dict['tag'] = ''
    if 'year' not in in_dict:
        in_dict['year'] = xml_obj.years
    if 'releaseTime' not in in_dict:
        in_dict['releaseTime'] = xml_obj.update_time
    if 'score' not in in_dict:
        in_dict['score'] = '100'
    if 'recommendLevel' not in in_dict:
        in_dict['recommendLevel'] = '3'
    if 'limitLevel' not in in_dict:
        in_dict['limitLevel'] = '3'
    if 'totalSerial' not in in_dict:
        in_dict['totalSerial'] = xml_obj.total_count
    if 'price' not in in_dict:
        in_dict['price'] = '0'
    if 'duration' not in in_dict:
        in_dict['duration'] = '24'
    if 'actor' not in in_dict:
        t_dict = {'zh': '', 'zh_hk': '', 'en': ''}
        if judge_contain_chinese_chr(xml_obj.leading_role):
            t_dict['zh'] = xml_obj.leading_role
        else:
            t_dict['en'] = xml_obj.leading_role
        in_dict['actor'] = t_dict
    if 'director' not in in_dict:
        t_dict = {'zh': '', 'zh_hk': '', 'en': ''}
        if judge_contain_chinese_chr(xml_obj.director):
            t_dict['zh'] = xml_obj.director
        else:
            t_dict['en'] = xml_obj.director
        in_dict['director'] = t_dict
    if 'screenwriter' not in in_dict:
        t_dict = {'zh': '无', 'zh_hk': '', 'en': ''}
        in_dict['screenwriter'] = t_dict
    if 'dialogue' not in in_dict:
        t_dict = {'zh': '', 'zh_hk': '', 'en': ''}
        in_dict['dialogue'] = t_dict
    if 'description' not in in_dict:
        t_dict = {'zh': xml_obj.desc, 'zh_hk': '', 'en': ''}
        in_dict['description'] = t_dict
    if 'thumbnail' not in in_dict:
        in_dict['thumbnail'] = ''
    if 'image' not in in_dict:
        in_dict['image'] = 'image.jpg'
    if 'poster' not in in_dict:
        in_dict['poster'] = ''


def update_episode_info(in_dict, xml_obj):
    if 'episodes' not in in_dict:
        in_dict['episodes'] = []
    t_dict = dict()
    t_dict['serial'] = xml_obj.p_part_num
    if in_dict['meta'] == 2:
        t_dict['title'] = {'zh': xml_obj.p_part_num, 'zh_hk': xml_obj.p_part_num, 'en': xml_obj.p_part_num}
    elif in_dict['meta'] == 4 or in_dict['meta'] == 1:
        new_p_program_name = get_date_from_p_name(xml_obj.p_program_name)
        t_dict['title'] = {'zh': new_p_program_name, 'zh_hk': '', 'en': ''}
    t_dict['thumbnail'] = ''
    t_dict['image'] = 'image.jpg'
    in_dict['episodes'].append(t_dict)


def parameters_check_and_get():
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
    if os.path.exists(ret_dict['video_dir']) and os.path.isdir(ret_dict['video_dir']):
        video_dir = os.path.normpath(ret_dict['video_dir'])
    else:
        logging.error('json文件内的video_dir{}--有问题，请检查'.format(ret_dict['video_dir']))
        sys.exit()

    if os.path.exists(ret_dict['target_dir']) and os.path.isdir(ret_dict['target_dir']):
        target_dir = os.path.normpath(ret_dict['target_dir'])
    else:
        target_dir = os.path.normpath(ret_dict['target_dir'])
        mk_dir(target_dir)

    return x_p, x_cat, x_cat_ser, video_dir, target_dir, meta_type_dict


def parse_pure_ts_dir_entrance():
    """
    解析工具主入口
    :return:
    """
    x_p, x_cat, x_cat_ser, video_dir, target_dir, meta_type_dict = parameters_check_and_get()
    program_cnt = 0
    for s_node in x_p.get_next_program_serial_node():
        now_json_dict = OrderedDict()  # record xml info in json
        x_p.get_program_serial_info(s_node)
        p_child_list = x_p.get_program_node_list(s_node)
        need_json = False
        if p_child_list:
            column_name = get_column_name(x_p.id, x_cat, x_cat_ser)
            for c_node in p_child_list:
                x_p.get_program_info(c_node)
                name_tuple = x_p.output_parameter()
                if column_name:
                    res_yield = get_video_and_move_to_dir(name_tuple, video_dir, target_dir, column_name, x_p.name)
                    if res_yield == 'ok':
                        need_json = True
                        get_pic_and_write_json_to_dir(x_p.big_poster, target_dir, column_name, x_p.name)
                        fill_json_dict(now_json_dict, x_p, column_name, meta_type_dict)
                        update_episode_info(now_json_dict, x_p)
                        program_cnt += 1
                        logging.info('节目计数 {} 节目名：{}'.format(program_cnt, name_tuple.p_program_name))
                else:
                    logging.error('programSerial--id--<{}>--name--<{}>--programName--<{}>'
                                  ' cant find which column is is belongs to'.
                                  format(x_p.id, x_p.name, x_p.p_program_name))
                x_p.restore_inner_program_variables()
            if need_json:
                json_rec_dict = get_programs_json_file_content(target_dir, column_name, x_p.name)
                if json_rec_dict is None:
                    # first record xml info into json file
                    put_programs_json_file_content(target_dir, column_name, x_p.name, now_json_dict)
                else:
                    # second append some programs into base json file，update total count and episode info
                    json_rec_dict['totalSerial'] = now_json_dict['totalSerial']
                    for i_d in now_json_dict['episodes']:
                        json_rec_dict['episodes'].append(i_d)
                    put_programs_json_file_content(target_dir, column_name, x_p.name, json_rec_dict)

        x_p.restore_inner_all_variables()


def parse_mixed_ts_dir_entrance():
    x_p, x_cat, x_cat_ser, video_dir, target_dir, meta_type_dict = parameters_check_and_get()
    file_list = get_dir_file_list(video_dir)
    f_list_len = len(file_list)
    p_name_list = [t['name'] for t in file_list]
    program_cnt = 0
    for s_node in x_p.get_next_program_serial_node():
        now_json_dict = OrderedDict()  # record xml info in json
        x_p.get_program_serial_info(s_node)
        p_child_list = x_p.get_program_node_list(s_node)
        need_json = False
        if p_child_list and x_p.name in p_name_list:
            column_name = get_column_name(x_p.id, x_cat, x_cat_ser)
            for c_node in p_child_list:
                for ts_d in file_list:
                    x_p.get_program_info(c_node)
                    name_tuple = x_p.output_parameter()
                    if column_name and ts_d['p_name'] == name_tuple.p_program_name and ts_d['name'] == x_p.name:
                        res_yield = get_video_and_move_to_dir_revise(name_tuple, ts_d['path'], ts_d['ts'],
                                                                     target_dir, column_name, x_p.name)
                        if res_yield == 'ok':
                            need_json = True
                            get_pic_and_write_json_to_dir(x_p.big_poster, target_dir, column_name, x_p.name)
                            fill_json_dict(now_json_dict, x_p, column_name, meta_type_dict)
                            update_episode_info(now_json_dict, x_p)
                            program_cnt += 1
                            f_list_len -= 1
                            logging.info('节目计数 {} 节目名：{}'.format(program_cnt, name_tuple.p_program_name))
                    else:
                        if not column_name:
                            logging.error('programSerial--id--<{}>--name--<{}>--programName--<{}>'
                                          ' cant find which column is is belongs to'.
                                          format(x_p.id, x_p.name, x_p.p_program_name))
                        else:
                            pass
                x_p.restore_inner_program_variables()
            if need_json:
                json_rec_dict = get_programs_json_file_content(target_dir, column_name, x_p.name)
                if json_rec_dict is None:
                    # first record xml info into json file
                    put_programs_json_file_content(target_dir, column_name, x_p.name, now_json_dict)
                else:
                    # second append some programs into base json file，update total count and episode info
                    json_rec_dict['totalSerial'] = now_json_dict['totalSerial']
                    for i_d in now_json_dict['episodes']:
                        json_rec_dict['episodes'].append(i_d)
                    put_programs_json_file_content(target_dir, column_name, x_p.name, json_rec_dict)

        if f_list_len == 0:
            logging.info('amazing, all ts file complete!!!')
            sys.exit()

        x_p.restore_inner_all_variables()


@contextmanager
def count_app_run_time():
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        logging.info('time <{used_time}> is used'.format(used_time=end_time - start_time))


if __name__ == '__main__':
    arg_p = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                    usage='python3 %(prog)s mode'
                                          ' \n----mode(pure ts in video dir if mode=0, or mode=1)',
                                    description='For example: \n\tpython3 {} mode'
                                                ' \n----mode(pure ts in video dir if mode=0, or mode=1)'
                                    .format(os.path.basename(sys.argv[0])))
    arg_p.add_argument('mode', type=int, nargs=1, choices=[0, 1],
                       help='select mode for pure ts in video directory or mixed directory')
    input_paras = arg_p.parse_args()
    if int(input_paras.mode[0]) == 0:
        with count_app_run_time():
            parse_pure_ts_dir_entrance()
    elif int(input_paras.mode[0]) == 1:
        with count_app_run_time():
            parse_mixed_ts_dir_entrance()

    # test_open_xml_read_element(INPUT_FILE)

