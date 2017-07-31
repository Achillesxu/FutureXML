#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : FutureXML
@Time : 2017/7/26 16:41
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : XmlWriter.py
@desc :
"""

import logging
from collections import OrderedDict, namedtuple
from tools.XmlParser import XmlParser
from lxml.etree import Element, ElementTree, SubElement, tostring
from tools.utils import *

__author__ = 'achilles_xushy'

sample_file = 'C:\\Users\\admins\\Desktop\\20170215\\sd_xml.xml'

XML_CONTENT_DICT = {
    'MCM_NAVIGATION':
        ['ID', 'PARENT_ID', 'PROVIDER_ID', 'PROPER_TITLE', 'DURATION', 'PROGRAM_CLASS', 'FIELD_1', 'FIELD_2'],
    'MCM_PROGRAM':
        ['PROGRAM_CODE', 'PARALLEL_TITLE', 'SUBORDINATE_TITLE', 'ALTERNATIVE_TITLE', 'TITLE_DESC', 'SUBJECT_TERMS',
         'KEY_WORDS', 'CONTENT_INFO', 'EPISODES_NUMBER', 'SERIES_TITLE', 'SERIES_PARTITLE', 'DATE_EVENT', 'ATTACHMENT',
         'COPYRIGHT_STATE', 'COPYRIGHT_OWNER', 'PRODUCED_DATE', 'FIRBROAD_DATE', 'PUBLISHED_DATE', 'ADDITIONAL_LOGO',
         'ISRC', 'SOURCE_ACQUIRED', 'SOURCE_PROVIDER', 'CHARACTER', 'CROWD_TYPE', 'FIELD_1'],
    'MCM_CREATOR':
        ['TYPE', 'NAME', 'ROLE_MODE'],
    'MCM_FILEGROUP':
        ['FILEGROUPTYPE_ID', 'SUBTITLE_FORM', 'COLOR', 'AUDIO_QUALITY', 'VIDEO_QUALITY', 'MEDIA_TYPE',
         'VIDEO_BITRATE', 'BROWSE_LENGTH', 'BROWSE_WIDTH'],
    'MCM_DATAFILE':
        ['TYPE', 'FILE_MD5', 'DEST_PATH', 'DEST_FILENAME'],
    'MCM_EXTINFO':
        ['FIELD_1'],
    'MCM_MULTIINFO':
        ['TYPE', 'FIELD_1', 'FIELD_2', 'FIELD_3', 'FIELD_4', 'FIELD_5', 'FIELD_6']
}

file_log = logging.getLogger('file_record')


class XmlWriter(object):
    def __init__(self, xml_name):
        self.xml_file_name = xml_name
        self.root_node_name = 'DataSource'
        self.root = Element(self.root_node_name)

    def append_node_to_root(self, next_node):
        """
        在根节点后添加节点
        :param next_node:
        :return:
        """
        self.root.append(next_node)

    @staticmethod
    def add_node_after_target_node(root_node, target_node_name, now_node):
        """
        在当前节点的子节点后添加节点
        :param root_node:
        :param target_node_name:
        :param now_node:
        :return:
        """
        target_node = root_node.find(target_node_name)
        target_node.addnext(now_node)

    @staticmethod
    def yield_node_element(node_name, in_dict):
        """
        生成目标节点元素
        :param root_node_name:
        :param node_name:
        :param in_dict:
        :return:
        """
        root_node = Element(node_name)
        node_list = XML_CONTENT_DICT[node_name]
        for x in node_list:
            if in_dict.get(x):
                e_element = SubElement(root_node, x)
                e_element.text = in_dict[x]
            else:
                SubElement(root_node, x)
        return root_node

    def write_xml_file(self):
        """
        写xml内容到文件
        :return:
        """
        et = ElementTree(self.root)
        with open(self.xml_file_name, 'wb') as f:
            xml_str = tostring(et, encoding='utf-8', method="xml", xml_declaration=True,
                               pretty_print=True, with_tail=True, standalone='no')
            f.write(xml_str)


# def get_target_bit_rate(b_rate):
#     """
#     根据实际码率返回目标码率
#     :param b_rate:
#     :return:800/1500/7500
#     """
#     real_bt = int(b_rate)
#     if 500 <= real_bt <= 1200:
#         return 800
#     elif 1200 < real_bt <= 1800:
#         return 1500
#     elif 1800 < real_bt <= 10000:
#         return 7500
#     else:
#         return real_bt


def remove_number_in_name(p_name):
    res_list = p_name.split('_')
    try:
        int(res_list[0])
        r_p_name = res_list[1]
    except:
        r_p_name = p_name
    return r_p_name


def write_xml_to_target_dir(name_tuple, a_id, ret_video_name, video_width, video_height, video_bit_rate, program_dir,
                            i_p_program_name, big_ext):
    xml_file_dir_name = '{}/{}.xml'.format(program_dir, i_p_program_name)

    m_navigation = {x: '' for x in XML_CONTENT_DICT['MCM_NAVIGATION']}
    m_navigation['ID'] = str(a_id)
    m_navigation['PARENT_ID'] = str(name_tuple.parent_id)
    m_navigation['PROVIDER_ID'] = str(name_tuple.provider_id)
    m_navigation['PROPER_TITLE'] = '{}#{}'.format(str(i_p_program_name), str(name_tuple.p_part_num))
    m_navigation['DURATION'] = str(int(name_tuple.p_program_length) * 60)
    m_navigation['PROGRAM_CLASS'] = str(name_tuple.program_class)
    m_navigation['FIELD_1'] = str(name_tuple.tag)

    m_program = {x: '' for x in XML_CONTENT_DICT['MCM_PROGRAM']}
    m_program['CONTENT_INFO'] = str(name_tuple.p_program_desc)
    m_program['EPISODES_NUMBER'] = str(name_tuple.p_part_num)
    m_program['SERIES_TITLE'] = str(name_tuple.name)

    m_creator1 = {x: '' for x in XML_CONTENT_DICT['MCM_CREATOR']}
    m_creator1['TYPE'] = str(0)
    if name_tuple.director:
        m_creator1['NAME'] = str(name_tuple.director)
    else:
        m_creator1['NAME'] = '无'
    m_creator1['ROLE_MODE'] = '导演'

    m_creator2 = {x: '' for x in XML_CONTENT_DICT['MCM_CREATOR']}
    m_creator2['TYPE'] = str(0)
    if name_tuple.director:
        m_creator2['NAME'] = str(name_tuple.leading_role)
    else:
        m_creator2['NAME'] = '无'
    m_creator2['ROLE_MODE'] = '主演'

    m_creator3 = {x: '' for x in XML_CONTENT_DICT['MCM_CREATOR']}
    m_creator3['TYPE'] = str(0)
    m_creator3['NAME'] = '不详'
    m_creator3['ROLE_MODE'] = '主持人'

    m_creator4 = {x: '' for x in XML_CONTENT_DICT['MCM_CREATOR']}
    m_creator4['TYPE'] = str(0)
    m_creator4['NAME'] = '不详'
    m_creator4['ROLE_MODE'] = '嘉宾'

    m_filegroup1 = {x: '' for x in XML_CONTENT_DICT['MCM_FILEGROUP']}
    m_filegroup1['VIDEO_BITRATE'] = str(video_bit_rate)
    m_filegroup1['BROWSE_WIDTH'] = str(video_width)
    m_filegroup1['BROWSE_LENGTH'] = str(video_height)

    m_datafile1 = {x: '' for x in XML_CONTENT_DICT['MCM_DATAFILE']}
    m_datafile1['TYPE'] = str(50)
    m_datafile1['DEST_PATH'] = '/home/'
    m_datafile1['DEST_FILENAME'] = str(ret_video_name)  # 视频名字

    m_filegroup2 = {x: '' for x in XML_CONTENT_DICT['MCM_FILEGROUP']}
    m_filegroup2['VIDEO_BITRATE'] = '1'
    m_filegroup2['BROWSE_WIDTH'] = '1'
    m_filegroup2['BROWSE_LENGTH'] = '1'

    m_datafile2 = {x: '' for x in XML_CONTENT_DICT['MCM_DATAFILE']}
    m_datafile2['DEST_PATH'] = '/home/'
    m_datafile2['DEST_FILENAME'] = str(ret_video_name)  # 视频名字

    m_filegroup3 = {x: '' for x in XML_CONTENT_DICT['MCM_FILEGROUP']}

    m_datafile3 = {x: '' for x in XML_CONTENT_DICT['MCM_DATAFILE']}
    m_datafile3['TYPE'] = str(100)
    m_datafile3['DEST_PATH'] = '/home/'
    m_datafile3['DEST_FILENAME'] = str('h_{}.{}'.format(i_p_program_name, big_ext))  # 图片名字

    m_extinfo = {x: '' for x in XML_CONTENT_DICT['MCM_EXTINFO']}

    m_multinfo1 = {x: '' for x in XML_CONTENT_DICT['MCM_MULTIINFO']}
    m_multinfo1['TYPE'] = str(102)
    m_multinfo1['FIELD_3'] = str(name_tuple.years)

    m_multinfo2 = {x: '' for x in XML_CONTENT_DICT['MCM_MULTIINFO']}
    m_multinfo2['TYPE'] = str(105)
    m_multinfo2['FIELD_2'] = str(name_tuple.zone)

    x_writer = XmlWriter(xml_file_dir_name)
    n_navigation = x_writer.yield_node_element('MCM_NAVIGATION', m_navigation)
    x_writer.append_node_to_root(n_navigation)

    n_program = x_writer.yield_node_element('MCM_PROGRAM', m_program)
    x_writer.append_node_to_root(n_program)

    n_creator1 = x_writer.yield_node_element('MCM_CREATOR', m_creator1)
    x_writer.append_node_to_root(n_creator1)

    n_n_creator2 = x_writer.yield_node_element('MCM_CREATOR', m_creator2)
    x_writer.append_node_to_root(n_n_creator2)

    n_creator3 = x_writer.yield_node_element('MCM_CREATOR', m_creator3)
    x_writer.append_node_to_root(n_creator3)

    n_creator4 = x_writer.yield_node_element('MCM_CREATOR', m_creator4)
    x_writer.append_node_to_root(n_creator4)

    n_filegroup1 = x_writer.yield_node_element('MCM_FILEGROUP', m_filegroup1)
    n_filegroup2 = x_writer.yield_node_element('MCM_FILEGROUP', m_filegroup2)
    n_filegroup3 = x_writer.yield_node_element('MCM_FILEGROUP', m_filegroup3)
    n_datafile1 = x_writer.yield_node_element('MCM_DATAFILE', m_datafile1)
    n_datafile2 = x_writer.yield_node_element('MCM_DATAFILE', m_datafile2)
    n_datafile3 = x_writer.yield_node_element('MCM_DATAFILE', m_datafile3)

    x_writer.add_node_after_target_node(n_filegroup1, 'BROWSE_WIDTH', n_datafile1)
    x_writer.add_node_after_target_node(n_filegroup2, 'BROWSE_WIDTH', n_datafile2)
    x_writer.add_node_after_target_node(n_filegroup3, 'BROWSE_WIDTH', n_datafile3)
    x_writer.append_node_to_root(n_filegroup1)
    x_writer.append_node_to_root(n_filegroup2)
    x_writer.append_node_to_root(n_filegroup3)

    n_extinfo = x_writer.yield_node_element('MCM_EXTINFO', m_extinfo)
    x_writer.append_node_to_root(n_extinfo)
    n_multinfo1 = x_writer.yield_node_element('MCM_MULTIINFO', m_multinfo1)
    x_writer.append_node_to_root(n_multinfo1)
    n_multinfo2 = x_writer.yield_node_element('MCM_MULTIINFO', m_multinfo2)
    x_writer.append_node_to_root(n_multinfo2)

    x_writer.write_xml_file()


def yield_target_xml_file(name_tuple, video_dir_list, target_dir, xml_p):
    """

    :param name_tuple:
    :param video_dir_list: 可能的情况，单个文件夹，或者是多个目录
    :param target_dir:
    :param xml_p:
    :return:
    """

    small_poster_pic = get_http_file_name(name_tuple.small_poster)
    medium_poster_pic = get_http_file_name(name_tuple.medium_poster)
    big_poster_pic = get_http_file_name(name_tuple.big_poster)

    pic_set = {small_poster_pic, medium_poster_pic, big_poster_pic}
    # have_same_pic = 0

    if len(pic_set) < 3 and small_poster_pic == medium_poster_pic == big_poster_pic:
        small_poster_pic = 's_' + small_poster_pic
        medium_poster_pic = 'm_' + medium_poster_pic
        big_poster_pic = 'h_' + big_poster_pic
        # have_same_pic = 1

    i_p_program_name = remove_number_in_name(name_tuple.p_program_name)

    if name_tuple.p_m_src_url:
        video_name = get_http_file_name(name_tuple.p_m_src_url)
    else:
        file_log.error('{}-{}-{} 找不到视频文件链接'.format(name_tuple.name, name_tuple.p_part_num, name_tuple.p_program_name))
        return 'ng'

    program_dir_dict = OrderedDict()

    for video_dir in video_dir_list:
        video_path_name = '{}/{}'.format(video_dir, video_name)

        if os.path.exists(video_path_name) and os.path.isfile(video_path_name):
            ret_video_name, video_width, video_height, video_bit_rate = \
                get_resolution_bit_rate_new_name(video_path_name, i_p_program_name)
            if ret_video_name == video_width == video_height == video_bit_rate:
                file_log.error('解析--{}--出错'.format(video_path_name))
                continue
            else:
                suffix_d = os.path.basename(video_dir)
                program_dir_dict['{}/{}_{}'.format(target_dir, suffix_d, name_tuple.p_program_name)] = \
                    tuple((video_path_name, ret_video_name, video_width, video_height, video_bit_rate))
        else:
            file_log.error('{}-{}-{} 找不到视频文件'.format(name_tuple.name, name_tuple.p_part_num, name_tuple.p_program_name))
            continue

    if len(program_dir_dict) == 0:
        return 'ng'

    for program_dir in program_dir_dict.keys():
        if os.path.exists(program_dir):
            pass
        else:
            mk_dir(program_dir)
        # move video to dst_dir
        # TODO 测试稳定后方可打开下面的注释
        mv_files_to_dir(program_dir_dict[program_dir][0],
                        '{}/{}'.format(program_dir, program_dir_dict[program_dir][1]))

    small_ext = small_poster_pic.split('.')[1]
    medium_ext = medium_poster_pic.split('.')[1]
    big_ext = big_poster_pic.split('.')[1]

    for program_dir in program_dir_dict.keys():
        download_dict = OrderedDict()
        download_dict['{}/s_{}.{}'.format(program_dir, i_p_program_name, small_ext)] = name_tuple.small_poster
        download_dict['{}/m_{}.{}'.format(program_dir, i_p_program_name, medium_ext)] = name_tuple.medium_poster
        download_dict['{}/h_{}.{}'.format(program_dir, i_p_program_name, big_ext)] = name_tuple.big_poster
        pic_file_download_txt(download_dict, program_dir)

        write_xml_to_target_dir(name_tuple, 'test', program_dir_dict[program_dir][1],
                                program_dir_dict[program_dir][2], program_dir_dict[program_dir][3],
                                program_dir_dict[program_dir][4], program_dir, i_p_program_name, big_ext)

    return 'ok'


if __name__ == '__main__':
    # x_w = XmlWriter(sample_file)
    # MCM_NAVIGATION = {
    #     'ID': '123',
    #     'PARENT_ID': '456',
    #     'PROVIDER_ID': '678',
    #     'PROPER_TITLE': '09-03跨界喜剧王完整版：周杰孙楠卖萌说相声（高清收录）',
    #     'DURATION': '6619',
    #     'PROGRAM_CLASS': '综艺',
    #     'FIELD_1': '真人秀',
    #     'FIELD_2': ''}
    # MCM_DATAFILE = {x: '' for x in XML_CONTENT_DICT['MCM_DATAFILE']}
    # MCM_FILEGROUP = {x: '' for x in XML_CONTENT_DICT['MCM_FILEGROUP']}
    # MCM_FILEGROUP['BROWSE_LENGTH'] = str(1920)
    # MCM_FILEGROUP['BROWSE_WIDTH'] = str(1080)
    # file_group_node = x_w.yield_node_element('MCM_FILEGROUP', MCM_FILEGROUP)
    # data_file_node = x_w.yield_node_element('MCM_DATAFILE', MCM_DATAFILE)
    # x_w.add_node_after_target_node(file_group_node, 'BROWSE_WIDTH', data_file_node)
    # navigation_node = x_w.yield_node_element('MCM_NAVIGATION', MCM_NAVIGATION)
    # x_w.append_node_to_root(navigation_node)
    # x_w.append_node_to_root(file_group_node)
    # x_w.write_xml_file()
    pass
