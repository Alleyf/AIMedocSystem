import os

from elasticsearch import Elasticsearch


def query_elastics(key):
    es = Elasticsearch()  # 默认连接本地elasticsearch
    # 获取关键词相关词
    # union_api = "https://recom.cnki.net/api/recommendations/words/union"
    # union_key = requests.get(url=union_api, params={'w': key, 'top': 10})
    # union_key = json.loads(union_key.text)['wordres']
    # key = key + ',' + ','.join(union_key)
    # print(key)
    res = es.search(
        index='medocsys',
        query={
            "match": {
                "text": key
            }},
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
    results = []
    old_all_scores = 0
    res = res.get('hits')['hits']
    # print(res, type(res))
    for item in res:
        doc_id = item["_source"]['id']
        rel_score = item["_score"]
        source = "图片" if item["_source"]["django_ct"] == "medocsys.docimgtxt" else "文本"
        name = item["_source"]["doc_name"]
        page_id = item["_source"]["page_id"]
        fragments = item["highlight"]["text"]
        old_all_scores += rel_score
        page_img_num = item["_source"]["page_img_num"] if source == "图片" else 0
        item_dict = {"id": doc_id, "name": name, "rel_score": rel_score, "source": source, "page_img_num": page_img_num,
                     "page_id": page_id,
                     "fragments": fragments}
        results.append(item_dict)
    for item in results:
        item['rel_score'] = round((item['rel_score'] / old_all_scores) * 60, 2)
    return results


def query_elastics_fulltext(key):
    es = Elasticsearch()  # 默认连接本地elasticsearch
    # 获取关键词相关词
    # union_api = "https://recom.cnki.net/api/recommendations/words/union"
    # union_key = requests.get(url=union_api, params={'w': key, 'top': 10})
    # union_key = json.loads(union_key.text)['wordres']
    # key = key + ',' + ','.join(union_key)
    # print(key)
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


if __name__ == '__main__':
    # print(query_elastics("Fuzzy"))
    print(query_elastics_fulltext(key="fuzzy"))
# id,name,page_id,relscore
