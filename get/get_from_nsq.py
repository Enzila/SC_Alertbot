from controller.controller import Controller
import requests, json

class from_nsq(Controller):

    final = {}

    def __init__(self,**kwargs):
        Controller.__init__(self, **kwargs)
        self.nsq()

    def nsq(self):
        try:
            result = []
            PH = ['sc_instagram', 'sc_facebook', 'sc_youtube']
            NDC = ['online-news', 'printed-news', 'tv-news']
            channel_list2 = self.config.get('consumer_list', 'list_topic_nsq2').split(',')
            a = 0
            result.append("\n--\t*NSQ*\t--")
            while True:
                if a == 0:
                    for b in PH:
                        check_list = self.config.get('api_nsq', 'api_nsq_ph').format(b)
                        req = json.loads((requests.get(check_list)).content)
                        try:
                            depth = req['depth']
                            if req['clients'] is None: conektion = 'No clients connected to this channel'
                            else: conektion = len(req['clients'])
                        except:
                            conektion = 'Timed Out'
                            depth = 'Timed Out'
                        if depth != 0:
                            botmesseg = "\n*{0}*\ndepth : {2}\nconnection : {3}\nchannel_name : {1}".format(
                                req['topic_name'], req['channel_name'], depth, conektion)
                            result.append(botmesseg)
                    #print "PH DONE"
                elif a == 1:
                    for b in NDC:
                        check_list = self.config.get('api_nsq', 'api_nsq_ndc').format(b)
                        req = json.loads((requests.get(check_list)).content)
                        try:
                            depth = req['depth']
                            if req['clients'] is None: conektion = 'No clients connected to this channel'
                            else: conektion = len(req['clients'])
                        except:
                            conektion = 'Timed Out'
                            depth = 'Timed Out'
                        if depth != 0:
                            botmesseg = "\n*{0}*\ndepth : {2}\nconnection : {3}\nchannel_name : {1}".format(
                                req['topic_name'], req['channel_name'], depth, conektion)
                            result.append(botmesseg)
                    # print "NDC DONE"
                elif a == 2:
                    check_list = self.config.get('api_nsq', 'api_nsq_bint')
                    req = json.loads((requests.get(check_list)).content)
                    try:
                        depth = req['depth']
                        if req['clients'] is None: conektion = 'No clients connected to this channel'
                        else: conektion = len(req['clients'])
                    except:
                        conektion = 'Timed Out'
                        depth = 'Timed Out'
                    if depth != 0:
                        botmesseg = "\n*{0}*\ndepth : {2}\nconnection : {3}\nchannel_name : {1}".format(
                            req['topic_name'], req['channel_name'], depth, conektion)
                        result.append(botmesseg)
                elif a == 3:
                    for b in PH:
                        check_list = self.config.get('api_nsq', 'api_nsq_ndc_profiling').format(b)
                        req = json.loads((requests.get(check_list)).content)
                        try:
                            depth = req['depth']
                            if req['clients'] is None: conektion = 'No clients connected to this channel'
                            else: conektion = len(req['clients'])
                            channel = req['channel_name']
                            topic_name = req['topic_name']
                        except:
                            topic_name = 'Timed Out'
                            channel = 'Timed Out'
                            conektion = 'Timed Out'
                            depth = 'Timed Out'
                        if depth != 0:
                            botmesseg = "\n*{0}*\ndepth : {2}\nconnection : {3}\nchannel_name : {1}".format(
                                topic_name,channel,depth,conektion)
                            result.append(botmesseg)
                elif a == 4:
                    for b in channel_list2:
                        check_list = self.config.get('api_nsq', 'api_nsq_req2').format(b)
                        req = json.loads((requests.get(check_list)).content)
                        for c in range(req['channels'].__len__()):
                            try:
                                depth = req['channels'][c]['depth']
                                if req['channels'][c]['clients'].__len__() is None: conektion = 'No clients connected to this channel'
                                else: conektion = len(req['channels'][c]['clients'])
                                channel = req['channels'][c]['channel_name']
                            except:
                                channel = 'Timed Out'
                                conektion = 'Timed Out'
                                depth = 'Timed Out'
                            if depth != 0:
                                botmesseg = "\n*{0}*\ndepth : {2}\nconnection : {3}\nchannel_name : {1}".format(
                                    b,channel,depth,conektion)
                                result.append(botmesseg)
                else: break
                a += 1
            if result.__len__() <= 1: result.append("\nNSQ Safe.")
            print ("\n".join(result).replace('_', ' '))
            self.final['nsq'] = result
            # return result
        except Exception as e: self.final['nsq'] = e

if __name__ == '__main__':
    print(from_nsq().final.get('nsq'))