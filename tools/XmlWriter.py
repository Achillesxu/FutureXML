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

from lxml.etree import Element, ElementTree, SubElement, tostring, fromstring, parse

from tools.utils import *


sample_file = 'C:\\Users\\admins\\Desktop\\20170215\\sd_xml.xml'

LAN_LIST = ['zh', 'zh_hk', 'en']


file_log = logging.getLogger('file_record')


class XmlWriter(object):
    def __init__(self, xml_name, root_name):
        self.xml_file_name = xml_name
        self.root_node_name = root_name
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
        :param node_name:
        :param in_dict:
        :return:
        """
        root_node = Element(node_name)
        for x in in_dict.keys():
            if in_dict.get(x):
                e_element = SubElement(root_node, x)
                e_element.text = in_dict[x]
            else:
                e_element = SubElement(root_node, x)
                e_element.text = ''
        return root_node

    @staticmethod
    def yield_one_node_element(node_name, node_value=None):
        element_node = Element(node_name)
        if node_value:
            element_node.text = node_value
        return element_node

    def write_xml_file(self):
        """
        写xml内容到文件
        :return:
        """
        et = ElementTree(self.root)
        with open(self.xml_file_name, 'wb') as f:
            xml_str = tostring(self.root, encoding='utf-8', method="xml", xml_declaration=True,
                               pretty_print=True, with_tail=True, standalone='no')
            f.write(xml_str)

    def get_xml_str(self):
        """
        获取生成的xml
        :return:
        """
        et = ElementTree(self.root)
        xml_str = tostring(et, encoding='utf-8', method="xml", xml_declaration=True,
                           pretty_print=True, with_tail=True, standalone='no')
        return xml_str


def write_future_xml(xml_dir, p_dict):
    xml_file_dir_name = '{}/{}.xml'.format(xml_dir, 'metadata')
    x_writer = XmlWriter(xml_file_dir_name, 'media')
    id_node = x_writer.yield_one_node_element('id')
    id_node.text = p_dict['id']
    x_writer.append_node_to_root(id_node)

    meta_node = x_writer.yield_one_node_element('meta')
    meta_node.text = p_dict['meta']
    x_writer.append_node_to_root(meta_node)

    drm_node = x_writer.yield_one_node_element('drm')
    drm_node.text = '0'
    x_writer.append_node_to_root(drm_node)

    m_title = {x: '' for x in LAN_LIST}
    m_title.update(p_dict['title'])
    title_node = x_writer.yield_node_element('title', m_title)
    x_writer.append_node_to_root(title_node)

    m_title2 = {x: '' for x in LAN_LIST}
    title_node2 = x_writer.yield_node_element('title2', m_title2)
    x_writer.append_node_to_root(title_node2)

    type_node = x_writer.yield_one_node_element('type')
    type_node.text = p_dict['type']
    x_writer.append_node_to_root(type_node)

    category_node = x_writer.yield_one_node_element('category')
    category_node.text = p_dict['program_class']
    x_writer.append_node_to_root(category_node)
    #
    area_node = x_writer.yield_one_node_element('area')
    area_node.text = p_dict['zone']
    x_writer.append_node_to_root(area_node)

    tag_node = x_writer.yield_one_node_element('tag')
    tag_node.text = p_dict['tag']
    x_writer.append_node_to_root(tag_node)

    year_node = x_writer.yield_one_node_element('year')
    year_node.text = p_dict['years']
    x_writer.append_node_to_root(year_node)

    release_time_node = x_writer.yield_one_node_element('releaseTime')
    release_time_node.text = p_dict['update_time']
    x_writer.append_node_to_root(release_time_node)

    score_node = x_writer.yield_one_node_element('score')
    score_node.text = p_dict['score']
    x_writer.append_node_to_root(score_node)

    recommend_level_node = x_writer.yield_one_node_element('recommendLevel')
    recommend_level_node.text = p_dict['recommendLevel']
    x_writer.append_node_to_root(recommend_level_node)

    limit_level_node = x_writer.yield_one_node_element('limitLevel')
    limit_level_node.text = p_dict['limitLevel']
    x_writer.append_node_to_root(limit_level_node)

    total_serial_node = x_writer.yield_one_node_element('totalSerial')
    total_serial_node.text = p_dict['totalSerial']
    x_writer.append_node_to_root(total_serial_node)

    cur_serial_node = x_writer.yield_one_node_element('curSerial')
    cur_serial_node.text = p_dict['curSerial']
    x_writer.append_node_to_root(cur_serial_node)

    price_node = x_writer.yield_one_node_element('price')
    price_node.text = p_dict['price']
    x_writer.append_node_to_root(price_node)

    duration_node = x_writer.yield_one_node_element('duration')
    duration_node.text = p_dict['duration']
    x_writer.append_node_to_root(duration_node)

    m_actor = {x: '' for x in LAN_LIST}
    m_actor.update(p_dict['actor'])
    actor_node = x_writer.yield_node_element('actor', m_actor)
    x_writer.append_node_to_root(actor_node)

    m_director = {x: '' for x in LAN_LIST}
    m_director.update(p_dict['director'])
    director_node = x_writer.yield_node_element('director', m_director)
    x_writer.append_node_to_root(director_node)

    m_screen_writer = {x: '' for x in LAN_LIST}
    m_screen_writer.update(p_dict['screenwriter'])
    screen_writer_node = x_writer.yield_node_element('screenwriter', m_screen_writer)
    x_writer.append_node_to_root(screen_writer_node)

    m_dialogue = {x: '' for x in LAN_LIST}
    m_dialogue.update(p_dict['dialogue'])
    dialogue_node = x_writer.yield_node_element('dialogue', m_dialogue)
    x_writer.append_node_to_root(dialogue_node)

    m_description = {x: '' for x in LAN_LIST}
    m_description['zh'] = p_dict['desc']
    description_node = x_writer.yield_node_element('description', m_description)
    x_writer.append_node_to_root(description_node)

    thumbnail_node = x_writer.yield_one_node_element('thumbnail')
    thumbnail_node.text = 'thumbnail.jpg'
    x_writer.append_node_to_root(thumbnail_node)

    image_node = x_writer.yield_one_node_element('image')
    image_node.text = 'image.jpg'
    x_writer.append_node_to_root(image_node)

    poster_node = x_writer.yield_one_node_element('poster')
    poster_node.text = p_dict['poster']
    x_writer.append_node_to_root(poster_node)

    episodes_node = x_writer.yield_one_node_element('episodes')

    for i_e in p_dict['episodes']:
        epi_node = SubElement(episodes_node, 'episode')
        ser_node = SubElement(epi_node, 'serial')
        ser_node.text = i_e['serial']

        tit_node = SubElement(epi_node, 'title')
        zh_node = SubElement(tit_node, 'zh')
        zh_node.text = i_e['serial']
        zh_hk_node = SubElement(tit_node, 'zh_hk')
        zh_hk_node.text = i_e['serial']
        en_node = SubElement(tit_node, 'en')
        en_node.text = i_e['serial']

        thu_node = SubElement(epi_node, 'thumbnail')
        thu_node.text = ''
        img_node = SubElement(epi_node, 'image')
        img_node.text = 'image.jpg'
    x_writer.append_node_to_root(episodes_node)

    x_writer.write_xml_file()


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
    program_dict = {
        'i_p_program_name': 'test',
        'cur_serial': str(1),
        'programs': [
            {'serial': '2', 'title': 'show_time', 'image': 'x.jpg'},
            {'serial': '3', 'title': 'show_time1', 'image': 'x1.jpg'},
            {'serial': '4', 'title': 'show_time1', 'image': 'x1.jpg'},
        ]
    }
    in_xml_dir = 'C:\\Users\\admins\\Desktop\\20170721'
    write_future_xml(in_xml_dir, program_dict)

