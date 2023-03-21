import os

from elasticsearch import Elasticsearch


# 函数方法
def query_elastics(key: str, start=0, size=1000):
    results = []
    try:
        rel_num_ls = query_elastics_min_fragment(key=key)
        # es = Elasticsearch()  # 默认连接本地elasticsearch
        # es = Elasticsearch([{"host": "127.0.0.1", "port": 9200}])  # 默认连接本地elasticsearch
        es = Elasticsearch([{"host": "43.139.217.160", "port": 9200}])  # 连接云端elasticsearch
        # 获取关键词相关词
        # union_api = "https://recom.cnki.net/api/recommendations/words/union"
        # union_key = requests.get(url=union_api, params={'w': key, 'top': 10})
        # union_key = json.loads(union_key.text)['wordres']
        # key = key + ',' + ','.join(union_key)
        # print(key)
        res = es.search(
            # index=['medocsys'],
            index=['doctxt', 'docimgtxt'],
            query={
                "match": {
                    "text": {
                        "query": key,
                        # "analyzer": "ik_max_word"  # 指定搜索时的分词模式
                    },
                },

            },
            track_total_hits=True,
            from_=start,
            size=size,
            highlight=
            {
                "fragment_size": 100,
                "number_of_fragments": 1000,
                "fields": {
                    "name": {
                        "pre_tags":
                            "<strong>",
                        "post_tags":
                            "</strong>"
                    },
                    "text": {
                        "pre_tags":
                            "<strong>",
                        "post_tags":
                            "</strong>"
                    }
                }
            })
        # print(res)
        # results = []
        old_all_scores = 0
        res = res.get('hits')['hits']
        # print("总共含有关键词的页数", len(res))
        for item in res:
            doc_id = item["_source"]['id']
            rel_score = item["_score"]
            source = "图片" if item["_source"]["django_ct"] == "medocsys.docimgtxt" else "文本"
            name = item["_source"]["doc_name"]
            page_id = item["_source"]["page_id"]
            fragments = item["highlight"]["text"]
            # print(fragments)
            old_all_scores += rel_score
            page_img_num = item["_source"]["page_img_num"] if source == "图片" else 0
            item_dict = {"id": doc_id, "name": name, "rel_score": rel_score, "source": source,
                         "page_img_num": page_img_num,
                         "page_id": page_id,
                         "fragments": fragments}
            results.append(item_dict)
        for i, item in enumerate(rel_num_ls):
            # item['rel_score'] = round((item['rel_score'] / old_all_scores) * 60, 2)
            # item['rel_score'] = round((len(item["fragments"]) / all_num) * 60, 2)
            results[i]['rel_score'] = item
        return results
    except Exception as e:
        print(e)
    finally:
        return results


def query_elastics_min_fragment(key: str, start=0, size=1000):
    all_num = 0
    rel_score_ls = []
    try:
        # es = Elasticsearch([{"host": "127.0.0.1", "port": 9200}])  # 默认连接本地elasticsearch
        es = Elasticsearch([{"host": "43.139.217.160", "port": 9200}])  # 连接云端elasticsearch
        res = es.search(
            # index=['medocsys'],
            index=['doctxt', 'docimgtxt'],
            query={
                "match": {
                    "text": {
                        "query": key,
                        # "analyzer": "ik_max_word"  # 指定搜索时的分词模式
                    },
                },

            },
            track_total_hits=True,
            from_=start,
            size=size,
            highlight=
            {
                "fragment_size": 5,
                "number_of_fragments": 1000,
                "fields": {
                    "text": {
                    }
                }
            })
        res = res.get('hits')['hits']
        # print("总共含有关键词的页数", len(res))
        for item in res:
            fragments = item["highlight"]["text"]
            all_num += len(fragments)
        for item in res:
            print(all_num, len(item["highlight"]["text"]), item["highlight"]["text"])
            rel_score = round((len(item["highlight"]["text"]) / all_num) * 60, 2)
            rel_score_ls.append(rel_score)
            # print(rel_score)
        return rel_score_ls
    except Exception as e:
        print(e)
    finally:
        return rel_score_ls


def query_elastics_fulltext(key):
    try:
        # es = Elasticsearch([{"host": "127.0.0.1", "port": 9200}])  # 默认连接本地elasticsearch
        es = Elasticsearch([{"host": "43.139.217.160", "port": 9200}])  # 连接云端elasticsearch
        print(es)
        res = es.search(
            index='medocsys',
            query={
                "match": {
                    "text": key
                }}
        )
        res = res.get('hits')['hits']
        full_txt = ''
        for item in res:
            if item['_source']['doc_name'] == res[0]['_source']['doc_name']:
                # full_txt += item["_source"]["text"]
                full_txt = os.path.join(full_txt, item["_source"]["text"])
        if res:
            doc_name = res[0]['_source']['doc_name']
            return True, doc_name, full_txt
        else:
            return False, '', ''
    except Exception as e:
        print(e, "发生了错误")
        return False, '', ''

    # 获取关键词相关词
    # union_api = "https://recom.cnki.net/api/recommendations/words/union"
    # union_key = requests.get(url=union_api, params={'w': key, 'top': 10})
    # union_key = json.loads(union_key.text)['wordres']
    # key = key + ',' + ','.join(union_key)
    # print(key)


if __name__ == '__main__':
    print(os.system('python ../../manage.py rebuild_index --noinput'))

#     # query_elastics("细胞培养", start=0, size=100)
#     # print(query_elastics_fulltext(key="fast"))
#     a = [{'id': 2}, {'id': 6}, {'id': 6}, {'id': 1}, ]
#     a7 = []
#     for dictionary in a:
#         if dictionary not in a7:
#             a7.append(dictionary)
#     print('a7 =', a7)
