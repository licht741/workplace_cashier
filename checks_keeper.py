#!/usr/bin/python
# -*- coding: utf-8 -*-

class checks_keeper:
    def __init__(self):
        self._current_list = [] # List[(goods_id, goods_cnt]

    def add_record(self, id, cnt):
        self._current_list.append((id, cnt))

    def reset(self):
        self._current_list = []

    def get_all_records(self):
        return self._current_list
