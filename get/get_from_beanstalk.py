from controller.controller import Controller
from pystalk import BeanstalkClient
import re

class from_beanstalk(Controller):

    final = {}

    def __init__(self, **kwargs):
        Controller.__init__(self,**kwargs)
        self.frombeanstalk()

    def frombeanstalk(self):
        try:
            result  = []
            a = 0
            result.append("\n--\t*Beanstalk*\t--")
            while True:
                tw = re.compile('sc_twitter_')
                fb = re.compile('sc_fb_')
                ig = re.compile('sc_ig_')
                yt = re.compile('sc_youtube_')
                if a == 1:
                    tube_list_fb    = []
                    tube_list_ig    = []
                    tube_list_yt    = []
                    client = BeanstalkClient(self.config.get('ip_beanstalk','ip_ph'),self.config.get('ip_beanstalk','port_ph'))
                    list_tube = client.list_tubes()
                    for b in range(list_tube.__len__()):
                        if fb.findall(list_tube[b]): tube_list_fb.append(list_tube[b])
                        if ig.findall(list_tube[b]): tube_list_ig.append(list_tube[b])
                        if yt.findall(list_tube[b]): tube_list_yt.append(list_tube[b])
                    tube_list   = tube_list_fb + tube_list_ig + tube_list_yt
                    for c in tube_list:
                        data = client.stats_tube(c)
                        if data['current-jobs-urgent'] >= 3000 or data['current-jobs-ready'] >= 3000:
                            res = "\n*{0}*\nworker : {1}\njobs-urgent : {2}\njobs-ready : {3}\njobs-buried : {4}\njobs-reserved: {5}" \
                                .format(data['name'], data['current-watching'], data['current-jobs-urgent'],
                                        data['current-jobs-ready'], data['current-jobs-buried'], data['current-jobs-reserved'])
                            result.append(res)
                        else: continue
                elif a == 0 :
                    tube_list = []
                    client  = BeanstalkClient(self.config.get('ip_beanstalk','ip_bintaro'),self.config.get('ip_beanstalk','port_bintaro'))
                    list_tube   = client.list_tubes()
                    for b in range(list_tube.__len__()):
                        if tw.findall(list_tube[b]): tube_list.append(list_tube[b])
                    for c in tube_list:
                        data    = client.stats_tube(c)
                        if data['current-jobs-urgent'] >= 3000 or data['current-jobs-ready'] >= 3000:
                            res = "\n*{0}*\nworker : {1}\njobs-urgent : {2}\njobs-ready : {3}\njobs-buried : {4}\njobs-reserved: {5}" \
                                .format(data['name'], data['current-watching'], data['current-jobs-urgent'],
                                        data['current-jobs-ready'], data['current-jobs-buried'], data['current-jobs-reserved'])
                            result.append(res)
                        else: continue
                else: break
                a+=1
            if result.__len__() <= 1: result.append("\nBeanstalk Safe.")
            print ("\n".join(result))
            self.final['beanstalk'] = result
            # return result
        except ValueError as e: self.final['beanstalk'] = e

if __name__ == '__main__':
    from_beanstalk().final.get('beanstalk')