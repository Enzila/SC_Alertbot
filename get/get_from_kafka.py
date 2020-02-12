from controller.controller import Controller
from bs4 import BeautifulSoup
import requests, re

class from_kafka(Controller):

    final = {}

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.kafka()

    def kafka(self):
        try:
            resultfinal = []
            check_list = self.config.get('consumer_list', 'list_checker_kafka').split(',')
            resultfinal.append("\n--\t*Kafka*\t--")
            for a in check_list:
                result = []
                url = self.config.get('consumer_list', 'url_source_kafka').format(a)
                geturl = requests.get(url)
                soup = BeautifulSoup(geturl.content, 'html.parser')
                get_consumer = soup.find_all('tr')
                for b in range(get_consumer.__len__() - 1):
                    b += 1
                    filter1 = re.sub('<.*?>', '', str(get_consumer[b]))
                    filter2 = re.sub(' ', '', filter1)
                    splitter = filter2.split("\n")
                    for c in range(4):
                        if splitter[c] is '':
                            splitter.pop(c)
                            continue
                    try:
                        if int(splitter[2]) <= 0: continue
                        else: result.append("{0} : {1}".format(splitter[0], splitter[2]))
                    except: result.append("{0} : {1}".format(splitter[0], splitter[2]))
                if result.__len__() is 0: continue
                else: resultfinal.append("\n*{0}*\n{1}".format(a, "\n".join(result)))
            if resultfinal.__len__() <= 1: resultfinal.append("Kafka Safe.")
            print ("\n".join(resultfinal))
            self.final['kafka'] = resultfinal
            # return resultfinal
        except Exception as e: self.final['kafka'] = e

if __name__ == '__main__':
    print (from_kafka().final.get('kafka'))
