#encoding: utf-8
"""
@Auther: husan
@Date: 2019/9/2 15:09
es工具
"""
from  elasticsearch import Elasticsearch
class ElasticScroll(object):

    def __init__(self, host, auth=None):
        self.__es = Elasticsearch(host, http_auth=auth)

    def scroll(self, index, query):
        res = None
        if not hasattr(self, '_scroll_id'):
            res = self.__es.search(index=index, body=query, search_type="query_then_fetch", scroll="1m")
            scroll_id = res.get('_scroll_id')
            if scroll_id :
                self._scroll_id = scroll_id
        else:
            res = self.__es.scroll({'scroll': '1m', 'scroll_id': self._scroll_id})
        hits = res.get('hits')
        if hits:
            return hits.get('hits')
        else:
            return []

