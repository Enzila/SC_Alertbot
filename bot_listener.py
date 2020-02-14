from get.get_from_beanstalk import from_beanstalk
from get.get_latest_update import latest_update
from get.get_from_kafka import from_kafka
from get.get_from_nsq import from_nsq
from controller.controller import Controller
import logging


bot = Controller().bot_controller()

@bot.message_handler(commands=['cekkafka'])
def cekkafka(message):
    try:
        bot.reply_to(message, '\n'.join(from_kafka().final.get('kafka')), parse_mode='markdown')
    except Exception as e:
        bot.reply_to(message, 'Error!! : {}'.format(e))

@bot.message_handler(commands=['cekbeanstalk'])
def cekbeanstalk(message):
    try:
        bot.reply_to(message, "\n".join(from_beanstalk().final.get('beanstalk')), parse_mode='markdown')
    except Exception as e:
        bot.reply_to(message, "Error!! : {}".format(e))

@bot.message_handler(commands=['ceknsq'])
def ceknsq(message):
    # chatid = update.message.chat_id
    try:
        bot.reply_to(message, "\n".join(from_nsq().final.get('nsq')).replace('_',' '), parse_mode='markdown')
    except Exception as e:
        bot.reply_to(message, "Error!! : {}".format(e))

@bot.message_handler(commands=['cekkafka_w_link'])
def cekkafka(message):
    try:
        bot.reply_to(message, "\n".join(from_kafka().final.get('kafka')), parse_mode='markdown')
    except Exception as e:
        bot.reply_to(message, "Error!! : {}".format(e))

@bot.message_handler(commands=['latest_update'])
def latest_updates(message):
    try:
        bot.reply_to(message, "\n".join(latest_update().final.get('latest_update')), parse_mode='markdown')
    except Exception as e:
        bot.reply_to(message, "Error!! : {}".format(e))



if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] - [%(levelname)s] -  MESSAGE = %(message)s',
        level=logging.INFO)
    try:
        logging.info('Status : Running')
        bot.polling()
    except Exception as  e:
        logging.warn('Status : Error {}'.format(e))
