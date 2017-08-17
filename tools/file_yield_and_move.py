#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : FutureXML
@Time : 2017/8/7 13:57
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : file_yield_and_move.py
@desc :
"""
import logging
from collections import OrderedDict, namedtuple
from tools.XmlParser import XmlParser

from tools.utils import *

file_log = logging.getLogger('file_record')


def get_video_and_move_to_dir(name_tuple, video_dir, target_dir, col_name, p_name):
    """
    :param name_tuple:
    :param video_dir:
    :param target_dir:
    :param col_name:
    :param p_name:
    :return:
    """

    if name_tuple.p_m_src_url:
        video_name = get_http_file_name(name_tuple.p_m_src_url)
    else:
        file_log.error('{}-{}-{}-{} 找不到视频文件链接'.
                       format(name_tuple.id,
                              name_tuple.name,
                              name_tuple.p_part_num,
                              name_tuple.p_program_name))
        return 'ng'

    video_path_name = '{}/{}'.format(video_dir, video_name)

    new_p_program_name = get_date_from_p_name(name_tuple.p_program_name)
    if os.path.exists(video_path_name) and os.path.isfile(video_path_name):
        ret_video_name, video_width, video_height, video_bit_rate = \
            get_resolution_bit_rate_new_name(video_path_name, new_p_program_name, name_tuple.p_program_id)
        if ret_video_name == video_width == video_height == video_bit_rate:
            file_log.error('解析--{}--出错'.format(video_path_name))
            return 'ng'
    else:
        file_log.info('{}-{}-{} 找不到视频文件'.format(name_tuple.name, name_tuple.p_part_num, name_tuple.p_program_name))
        return 'ng'

    f_media_path = os.path.join(target_dir, col_name, p_name, 'media')

    mk_dir(f_media_path)

    if mv_files_to_dir(video_path_name,
                       os.path.join(f_media_path, ret_video_name)):
        return 'ok'
    else:
        file_log.info('{}-{}-{} 视频文件重复，不能移动'.format(name_tuple.name, name_tuple.p_part_num, name_tuple.p_program_name))
        return 'ng'


def get_video_and_move_to_dir_revise(name_tuple, video_dir, ts_name, target_dir, col_name, p_name):
    """
    :param name_tuple:
    :param video_dir:
    :param ts_name:
    :param target_dir:
    :param col_name:
    :param p_name:
    :return:
    """

    video_path_name = '{}/{}'.format(video_dir, ts_name)
    new_p_program_name = get_date_from_p_name(name_tuple.p_program_name)
    if os.path.exists(video_path_name) and os.path.isfile(video_path_name):
        ret_video_name, video_width, video_height, video_bit_rate = \
            get_resolution_bit_rate_new_name(video_path_name, new_p_program_name, name_tuple.p_program_id)
        if ret_video_name == video_width == video_height == video_bit_rate:
            file_log.error('解析--{}--出错'.format(video_path_name))
            return 'ng'
    else:
        file_log.info('{}-{} 找不到视频文件'.format(name_tuple.name, video_path_name))
        return 'ng'

    f_media_path = os.path.join(target_dir, col_name, p_name, 'media')

    mk_dir(f_media_path)

    if mv_files_to_dir(video_path_name,
                       os.path.join(f_media_path, ret_video_name)):
        return 'ok'
    else:
        file_log.info('{}-{}-{} 视频文件重复，不能移动'.format(name_tuple.name, name_tuple.p_part_num, name_tuple.p_program_name))
        return 'ng'


def get_pic_and_write_json_to_dir(pic_url, target_dir, col_name, p_name):
    """
    check
    :param pic_url:
    :param target_dir:
    :param col_name:
    :param p_name:
    :return:
    """
    f_pic_path = os.path.join(target_dir, col_name, p_name, 'image')
    if os.path.exists(os.path.join(f_pic_path, 'image.jpg')):
        return
    # get pic download record to store in json file
    if not os.path.exists(os.path.join(f_pic_path, PIC_JSON_FILE)):
        mk_dir(f_pic_path)
        pic_suffix = os.path.splitext(pic_url)[1]
        download_dict = dict()
        download_dict['image{}'.format(pic_suffix)] = pic_url
        pic_file_download_txt(download_dict, f_pic_path)


def get_programs_json_file_content(target_dir, col_name, p_name):
    """
    :param target_dir:
    :param col_name:
    :param p_name:
    :return:
    """
    json_path = os.path.join(target_dir, col_name, p_name, 'xml', XML_JSON_FILE)
    if os.path.exists(json_path) and os.path.isfile(json_path):
        with open(json_path, mode='r', encoding='utf-8') as pf:
            j_dict = json.load(pf, object_pairs_hook=OrderedDict)
            return j_dict
    else:
        return None


def put_programs_json_file_content(target_dir, col_name, p_name, in_j_dict):
    """
    :param target_dir:
    :param col_name:
    :param p_name:
    :param in_j_dict:
    :return:
    """
    json_path = os.path.join(target_dir, col_name, p_name, 'xml', XML_JSON_FILE)
    if not os.path.exists(os.path.dirname(json_path)):
        mk_dir(os.path.dirname(json_path))
    with open(json_path, mode='w', encoding='utf-8') as pf:
        json.dump(in_j_dict, pf, ensure_ascii=False)
