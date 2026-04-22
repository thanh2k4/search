from elasticsearch import Elasticsearch, helpers
import json
import hashlib

client = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "m4WR0L9DOXdhCQoKxEGG"), verify_certs=False ,ssl_show_warn=False) 


def create_index(index_name="demo"):
    index_body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "vi_no_diacritics_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding"],
                        "preserve_original": True
                    }
                }
            },
            "similarity": {
                "okapi_bm25" : {
                    "type" : "BM25",
                    "k1" : 1,
                    "b" : 0.8
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                "type": "text",
                "similarity": "okapi_bm25",
                "fields": {
                    "folded": {
                    "type": "text",
                    "analyzer": "vi_no_diacritics_analyzer",
                    "similarity": "okapi_bm25"
                    }
                }
                },
                "description": {
                "type": "text",
                "similarity": "okapi_bm25",
                "fields": {
                    "folded": {
                    "type": "text",
                    "analyzer": "vi_no_diacritics_analyzer",
                    "similarity": "okapi_bm25"
                    }
                }
                },
                "content": {
                "type": "text",
                "similarity": "okapi_bm25",
                "fields": {
                    "folded": {
                    "type": "text",
                    "analyzer": "vi_no_diacritics_analyzer",
                    "similarity": "okapi_bm25"
                    }
                }
                },
                "time": {
                    "type": "keyword"
                },
                "link": {
                    "type": "keyword"
                }
    }
    }

    }

    client.options(ignore_status=[400]).indices.create(index=index_name, body=index_body)

def delete_index(index_name="demo"):
    client.options(ignore_status=[400, 404]).indices.delete(index=index_name)

def delete_document(link, index_name="demo"):
    doc_id = hashlib.md5(link.encode('utf-8')).hexdigest()
    client.delete(index=index_name, id=doc_id, ignore=[404])

def fetch_articles_batch(last_time=None, batch_size=50):
    must_clause = []
    if last_time:
        must_clause.append({
            "range": {
                "time": {
                    "gt": last_time 
                }
            }
        })

    query_body = {
        "size": batch_size,
        "query": {
            "bool": {
                "must": must_clause
            }
        },
        "sort": [
            {"time": "asc"} 
        ]
    }
    resp = client.search(index="demo", body=query_body)
    return resp["hits"]["hits"]

def insert_document(doc, index_name="demo"):
    doc_id = hashlib.md5(doc["link"].encode('utf-8')).hexdigest()
    client.index(index=index_name, id=doc_id, document=doc)

def get_all_documents(index_name="demo" , size = 100):
    query_body = {
        "query": {
            "match_all": {}
        },
        "size": size
    }
    return client.search(index=index_name, body=query_body)

def check_link_exists(link, index_name="demo"):
    query_body = {
        "size": 0,
        "query": {
            "term": {
                "link.keyword": link
            }
        }
    }

    resp = client.search(index=index_name, body=query_body)
    return resp["hits"]["total"]["value"] > 0


def search_many_fields(index_name="demo", keyword="" , page=1, size=10):
    query_body = {
        "from": (page - 1) * size,
        "size": size,
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "title": {
                                "query": keyword,
                                "boost": 5
                            }
                        }
                    },
                    {
                        "match": {
                            "title.folded": {
                                "query": keyword,
                                "boost": 2
                            }
                        }
                    },
                    {
                        "match": {
                            "description": {
                                "query": keyword,
                                "boost": 3
                            }
                        }
                    },
                    {
                        "match": {
                            "description.folded": {
                                "query": keyword,
                                "boost": 1.5
                            }
                        }
                    },

                    {
                        "match": {
                            "content": {
                                "query": keyword,
                                "boost": 1.5
                            }
                        }
                    },
                    {
                        "match": {
                            "content.folded": {
                                "query": keyword,
                                "boost": 0.7
                            }
                        }
                    }
                ],
                "minimum_should_match": 0
            }
        }
    }

    return client.search(index=index_name, body=query_body)
