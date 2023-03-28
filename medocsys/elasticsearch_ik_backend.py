from haystack.backends.elasticsearch7_backend import Elasticsearch7SearchBackend, Elasticsearch7SearchEngine

"""
分析器主要有两种情况会被使用：
第一种是插入文档时，将text类型的字段做分词然后插入倒排索引，
第二种就是在查询时，先对要查询的text类型的输入做分词，再去倒排索引搜索
如果想要让 索引 和 查询 时使用不同的分词器，ElasticSearch也是能支持的，只需要在字段上加上search_analyzer参数
在索引时，只会去看字段有没有定义analyzer，有定义的话就用定义的，没定义就用ES预设的
在查询时，会先去看字段有没有定义search_analyzer，如果没有定义，就去看有没有analyzer，再没有定义，才会去使用ES预设的
"""

DEFAULT_FIELD_MAPPING = {
    "type": "text",
    "analyzer": "ik_max_analyzer",
    "search_analyzer": "ik_smart_analyzer",
    "similarity": "BM25",
    "term_vector": "with_positions_offsets",
    # "index_options": "offsets"
}


class Elasticsearc7IkSearchBackend(Elasticsearch7SearchBackend):
    def __init__(self, *args, **kwargs):
        self.DEFAULT_SETTINGS['settings']['analysis']['filter']['len'] = {
            "type": "length",
            "min": 2
        }
        self.DEFAULT_SETTINGS['settings']['analysis']['analyzer']['ik_smart_analyzer'] = {
            "type": "custom",
            "tokenizer": "ik_smart",  # 这个自定义的分析器必须要
            "filter": ["len"]  # 最小分词个数为2
        }
        self.DEFAULT_SETTINGS['settings']['analysis']['analyzer']['ik_max_analyzer'] = {
            "type": "custom",
            "tokenizer": "ik_max_word",  # 这个自定义的分析器必须要
            "filter": ["len"]  # 最小分词个数为2
        }

        super(Elasticsearc7IkSearchBackend, self).__init__(*args, **kwargs)


class Elasticsearch7IkSearchEngine(Elasticsearch7SearchEngine):
    backend = Elasticsearc7IkSearchBackend
