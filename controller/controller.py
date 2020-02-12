from configparser import ConfigParser
from elasticsearch import Elasticsearch
from datetime import datetime
import telebot

class Controller:

    def __init__(self, config_file='config.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

    def bot_controller(self):
        bot = telebot.TeleBot(self.config.get('api_telegram','token'))
        return bot

    def elastic_get_count(self, from_path, index, range_by='created_at'):
        current_time = datetime.now()
        es = Elasticsearch(from_path)
        gte = current_time.strftime('%Y-%m-%d')
        lte = current_time.strftime('%Y-%m-%d %H:%M:%S')
        query = es.search(index=index, body={
            "sort":
                [
                    {range_by: {"order": "desc"}}
                ],
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                range_by: {
                                    "gte": "{} 00:00:00".format(gte),
                                    "lte": lte,
                                    "format": "yyyy-MM-dd HH:mm:ss",
                                    "time_zone": "+07:00"
                                }
                            }
                        }
                    ]
                }
            },
            "size": 1
        }, request_timeout=100)
        return query

    # def from_mysql(self, host,user,passw,db):
    #     conek = pymysql.connect(
    #         host=host,user=user,password=passw,db=db,
    #         charset='utf8mb4', cursorclass= pymysql.cursors.DictCursor)
    #     return conek



