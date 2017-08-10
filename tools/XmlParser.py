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
@File : XmlParser.py
@desc :
"""
import os
import sys
import time
import logging
import traceback
from collections import namedtuple
from lxml.etree import iterparse, ElementTree

from tools.utils import *

__author__ = 'achilles_xushy'

INPUT_FILE = 'C:\\Users\\admins\\Desktop\\20170721\\fullData20170721.xml'


class XmlParser(object):
    """
    解析big xml
    """
    def __init__(self):
        self.xml_file_name = ''

        self.id = ''
        self.name = ''
        self.program_class = ''
        self.desc = ''
        self.tag = ''
        self.director = ''
        self.leading_role = ''
        self.years = ''
        self.zone = ''
        self.small_poster = ''
        self.medium_poster = ''
        self.big_poster = ''
        self.update_time = ''
        self.total_count = ''

        self.p_program_series_id = ''
        self.p_program_id = ''
        self.p_program_name = ''
        self.p_program_definition = ''
        self.p_program_desc = ''
        self.p_part_num = ''
        self.p_program_length = ''

        self.p_m_src_url = ''

        self.programs_dict = {}

    def check_xml_file_valid(self, xml_file):
        self.xml_file_name = xml_file
        is_exist = os.path.exists(self.xml_file_name)
        suffix = os.path.basename(self.xml_file_name).split('.')[1]
        if is_exist and suffix == 'xml':
            return True
        else:
            return False

    def get_next_program_serial_node(self):
        context = iterparse(self.xml_file_name, tag='programSerial')
        for _, i_node in context:
            yield i_node
            i_node.clear()

    def get_program_serial_info(self, i_node):
        """
        :param i_node:
        :return:
        """
        if i_node.find('id') is not None:
            self.id = i_node.find('id').text
        if i_node.find('name') is not None:
            self.name = i_node.find('name').text
        if i_node.find('programClass') is not None:
            self.program_class = i_node.find('programClass').text
        if i_node.find('desc') is not None:
            self.desc = i_node.find('desc').text
        if i_node.find('tag') is not None:
            self.tag = i_node.find('tag').text
        if i_node.find('director') is not None:
            self.director = i_node.find('director').text
        if i_node.find('leadingRole') is not None:
            self.leading_role = i_node.find('leadingRole').text
        if i_node.find('years') is not None:
            self.years = i_node.find('years').text
        if i_node.find('zone') is not None:
            self.zone = i_node.find('zone').text
        if i_node.find('smallPoster') is not None:
            self.small_poster = i_node.find('smallPoster').text
        if i_node.find('poster') is not None:
            self.medium_poster = i_node.find('poster').text
        if i_node.find('bigPoster') is not None:
            self.big_poster = i_node.find('bigPoster').text
        if i_node.find('updateTime') is not None:
            self.update_time = i_node.find('updateTime').text
        if i_node.find('programTotalCount') is not None:
            self.total_count = i_node.find('programTotalCount').text

    @staticmethod
    def get_program_node_list(i_node):
        """
        :param i_node:
        :return: []
        """
        programs_node = i_node.find('programs')
        if programs_node is not None:
            et = ElementTree(programs_node)
            root = et.getroot()
            children1 = list(root)
            return children1
        else:
            return []

    def get_program_info(self, i_node):
        """
        :param i_node:
        :return:
        """
        if i_node.find('programSeriesId') is not None:
            self.p_program_series_id = i_node.find('programSeriesId').text
        if i_node.find('programId') is not None:
            self.p_program_id = i_node.find('programId').text
        if i_node.find('programName') is not None:
            self.p_program_name = i_node.find('programName').text
        if i_node.find('partNum') is not None:
            self.p_part_num = i_node.find('partNum').text
        if i_node.find('programDesc') is not None:
            self.p_program_desc = i_node.find('programDesc').text
        if i_node.find('programLength') is not None:
            self.p_program_length = i_node.find('programLength').text
        if i_node.find('definition') is not None:
            self.p_program_definition = i_node.find('definition').text

        medias_node = i_node.find('medias')
        if medias_node is not None:
            media_node = medias_node.find('media')
            if media_node is not None:
                self.p_m_src_url = media_node.find('srcUrl').text

    def output_parameter(self):
        program = namedtuple('program', ['p_program_series_id', 'p_program_id', 'p_program_name',
                                         'p_program_desc', 'p_part_num', 'p_program_length', 'p_m_src_url'])

        if self.p_program_definition:
            if self.p_program_definition in self.p_program_name:
                self.p_program_name = self.p_program_name[len('[' + self.p_program_definition + ']'):]

        # self.p_program_name = self.p_program_name.replace('/', '-')
        self.p_program_name = get_date_from_p_name(self.p_program_name)
        self.update_time = self.update_time.split(' ')[0].replace('-', '')

        out_put = program(self.p_program_series_id, self.p_program_id, self.p_program_name,
                          self.p_program_desc, self.p_part_num, self.p_program_length, self.p_m_src_url)

        return out_put

    def restore_inner_program_variables(self):
        """
        将program相关的变量恢复原始状态
        :return:
        """
        self.p_program_series_id = ''
        self.p_program_id = ''
        self.p_program_name = ''
        self.p_program_desc = ''
        self.p_part_num = ''
        self.p_program_length = ''
        self.p_program_definition = ''

        self.p_m_src_url = ''

    def restore_inner_all_variables(self):
        """
        将存储的变量恢复原始状态
        :return:
        """
        self.id = ''
        self.name = ''
        self.program_class = ''
        self.desc = ''
        self.tag = ''
        self.director = ''
        self.leading_role = ''
        self.years = ''
        self.zone = ''
        self.small_poster = ''
        self.medium_poster = ''
        self.big_poster = ''
        self.update_time = ''
        self.total_count = ''

        self.p_program_series_id = ''
        self.p_program_id = ''
        self.p_program_name = ''
        self.p_program_desc = ''
        self.p_part_num = ''
        self.p_program_length = ''
        self.p_program_definition = ''

        self.p_m_src_url = ''


class XMLParserCategory(object):
    def __init__(self):
        self.xml_file_name = ''
        self.cat_dict = {}
        self.p_cat_list = []
        self.p_cat_dict = {}
        self.c_cat_list = []

    def check_xml_file_valid(self, xml_file):
        self.xml_file_name = xml_file
        is_exist = os.path.exists(self.xml_file_name)
        suffix = os.path.basename(self.xml_file_name).split('.')[1]
        if is_exist and suffix == 'xml':
            return True
        else:
            return False

    def get_next_cate_item_node(self):
        context = iterparse(self.xml_file_name, tag='catgItem')
        for _, i_node in context:
            yield i_node
            i_node.clear()

    def get_cate_item_node(self, in_node):
        if in_node.find('id') is not None:
            c_id = in_node.find('id').text
        else:
            c_id = ''
        if in_node.find('name') is not None:
            c_name = in_node.find('name').text
        else:
            c_name = ''
        if in_node.find('parentId') is not None:
            c_parent_id = in_node.find('parentId').text
        else:
            c_parent_id = ''

        cat_item = namedtuple('cat_item', ['id', 'name', 'parent_id'])
        one_item = cat_item(c_id, c_name, c_parent_id)
        if int(one_item.parent_id) == 1:
            self.p_cat_list.append(one_item)
        elif int(one_item.parent_id) > 1:
            self.c_cat_list.append(one_item)
        else:
            pass

    def get_cat_dict(self):
        for it in self.get_next_cate_item_node():
            self.get_cate_item_node(it)
        for i in self.c_cat_list:
            for j in self.p_cat_list:
                self.p_cat_dict[j.id] = j.name
                if i.parent_id == j.id:
                    self.cat_dict[i.id] = (j.id, j.name)


class XMLParserCateSer(object):
    def __init__(self):
        self.xml_file_name = ''
        self.big_dict = {}

    def check_xml_file_valid(self, xml_file):
        self.xml_file_name = xml_file
        is_exist = os.path.exists(self.xml_file_name)
        suffix = os.path.basename(self.xml_file_name).split('.')[1]
        if is_exist and suffix == 'xml':
            return True
        else:
            return False

    def get_next_cate_item_node(self):
        context = iterparse(self.xml_file_name, tag='catgItem')
        for _, i_node in context:
            yield i_node
            i_node.clear()

    def get_cate_item_node(self, in_node):
        if in_node.find('catgItemId') is not None:
            c_id = in_node.find('catgItemId').text
        else:
            c_id = ''

        p_series = in_node.find('programSeries')
        p_serial_list = list(p_series)
        for i_n in p_serial_list:
            if i_n.find('programSeriesId') is not None:
                i_id = i_n.find('programSeriesId').text
            else:
                i_id = ''
            if i_n.find('programSeriesName') is not None:
                i_name = i_n.find('programSeriesName').text
            else:
                i_name = ''
            self.big_dict.update({i_id: (i_name, c_id)})

    def get_cat_dict(self):
        for it in self.get_next_cate_item_node():
            self.get_cate_item_node(it)


if __name__ == '__main__':
    # x_p = XmlParser()
    # ret = x_p.test_xml_file_valid(INPUT_FILE)
    # if ret:
    #     for node in x_p.get_next_program_serial_node():
    #         x_p.get_program_serial_info(node)
    #         children = x_p.get_program_node_list(node)
    #         node_cnt = 0
    #         if children:
    #             for child in children:
    #                 x_p.get_program_info(child)
    #                 name_t = x_p.output_parameter()
    #                 print(name_t)
    #                 node_cnt += 1
    #                 print(node_cnt)
    #         sys.exit()
    # else:
    #     print('file invalid')

    start_time = time.perf_counter()
    file_in = 'C:\\Users\\admins\\Desktop\\20170721\\cat20170721.xml'
    x_pc = XMLParserCategory()
    ret_v = x_pc.check_xml_file_valid(file_in)
    if ret_v:
        x_pc.get_cat_dict()
        for k, v in x_pc.cat_dict.items():
            print('key-<{}>, value-<{}-{}>'.format(k, v[0], v[1]))
        print('item list len <{}>'.format(len(x_pc.cat_dict)))
        # for k, v in x_pc.big_dict.items():
        #     print('key-<{}>, value-<{}-{}>'.format(k, v[0], v[1]))
        # print('item list len <{}>'.format(len(x_pc.big_dict)))
    else:
        print('bad op!')
    end_time = time.perf_counter()
    print('used time {}'.format(end_time - start_time))
