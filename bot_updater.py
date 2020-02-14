from controller.controller import Controller
from get.get_from_beanstalk import from_beanstalk
from get.get_latest_update import latest_update
from get.get_from_kafka import  from_kafka
from get.get_from_nsq import from_nsq
from get.get_from_csv import from_csv

class updater(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self ,**kwargs)
        self.bot = Controller().bot_controller()
        self.updaters()

    def updaters(self):
        result = '\n'.join(from_beanstalk().final.get('beanstalk') +
                           from_nsq().final.get('nsq') +
                           from_kafka().final.get('kafka') +
                           latest_update().final.get('latest_update') +
                           from_csv().final.get('token'))
        for a in self.config.get('telegram', 'chatid1').split(','):
            self.bot.send_message(chat_id=a, text=result.replace('_', ' '), parse_mode='markdown')

if __name__ == '__main__':
    updater()