#!/usr/bin/python
# -*- coding: utf-8 -*-

class checks_keeper:
    def __init__(self):
        self._current_list = {} # List[(goods_id, goods_cnt)]

    def add_record(self, id, cnt):
        id, cnt = int(id), int(cnt)
        if not self._current_list.has_key(id):
            self._current_list[id] = cnt
        else:
            self._current_list[id] += cnt

    def rem_record(self, id):
        if self._current_list.has_key(id):
            self._current_list.pop(id, None)


    def get_all_records(self):
        crnt_list = []
        for key, value in self._current_list.iteritems():
            crnt_list.append((key, value))
        return crnt_list

    @staticmethod
    def get_str_view(g_list, id, count):
        return str(id) + ":" + str(count)
        pass #TODO
