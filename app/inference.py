from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import urllib3

model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# url = 'http://ec2-3-19-14-184.us-east-2.compute.amazonaws.com:9200/'
# url = 'https://search-remember-arfkueaizgtcrbhtnynyqihisu.us-east-2.es.amazonaws.com:9200'
# url = 'https://34.64.46.1:9200/'
# url ='http://localhost:9200/'
url = 'https://4d6a-119-194-163-123.jp.ngrok.io'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def loadchat(member_id, we_id, textdata):
    es = Elasticsearch(hosts=[url], http_auth=('elastic', 'bTTMK9r-rH*HRj7hdVwV'), verify_certs=False)
    index = "chat_bot"
    textembeding = model.encode(textdata)
    s_body = {
        "query": {
            "script_score": {
                "query": {
                    "bool": {
                        "should": [
                            {
                                "match_phrase": {
                                    "member_id": member_id
                                }
                            },
                            {
                                "match_phrase": {
                                    "we_id": we_id

                                }
                            }
                        ]
                    },
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'chatvector') + 1.0",
                    "params": {"query_vector": textembeding[0:512]}
                }
            }
        }
    }

    res = es.search(index=index, body=s_body)

    if len(res['hits']['hits']) == 0:
        return {'return_sentence': "챗봇의 데이터가 충분하지 않습니다. 카카오톡 데이터를 넣어주세요!", 'filtering': 1}

    if res['hits']['hits'][0]['_score'] >= 1.7:
        return {'return_sentence': res['hits']['hits'][0]['_source']['A'], 'filtering': 0}
    else:
        return {'return_sentence': '미안해요.. 당신의 말을 이해하지 못했어요.. 다시 한번 말씀해주세요!', 'filtering': 1}
