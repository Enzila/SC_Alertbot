from controller.controller import Controller
from datetime import datetime
from dateutil import tz
import re

class latest_update(Controller):

    final = {}

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.current_time = datetime.now()
        self.from_zone  = tz.tzutc()
        self.to_zone    = tz.tzlocal()
        self.latestupdate()

    def latestupdate(self):
        result = ['\n\n\n*Latest Data IPD \t[{}]*\n'.format(self.current_time.strftime('%d.%m.%Y'))]
        for a in self.config.get('elastic_checker_list', 'ipd_index').split(';'):
            if 'news-online' in a:
                get_res = Controller().elastic_get_count(self.config.get('elastic', 'ipd'), index=a, range_by='pubDate')
                name = re.sub('-[a-z]+-\*$', '', a)
                name = re.sub('^[a-z]+-', '', name)
            else:
                get_res = Controller().elastic_get_count(self.config.get('elastic', 'ipd'), index=a)
                name = re.sub('^[a-z]+-[a-z]+-', '', a)
                name = re.sub('-\*$', '', name)
            try:
                total = get_res['hits']['total']
                if total is 0:
                    last_update = 'No Data Available'
                else:
                    get_time = get_res['hits']['hits'][0]['_source']['created_at']
                    if 'T' in get_time: get_time = re.sub('T', ' ', get_time)
                    utc_to_local = datetime.strptime(get_time, '%Y-%m-%d %H:%M:%S')
                    utc_to_local = utc_to_local.replace(tzinfo=self.from_zone)
                    last_update = str(utc_to_local.astimezone(self.to_zone))
                    last_update = re.sub('\+.*$', '', last_update)
                    if 'news-online' in a:
                        utc_to_local = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
                        utc_to_local = utc_to_local.replace(tzinfo=self.from_zone)
                        last_update = str(utc_to_local.astimezone(self.to_zone))
                last_update = re.sub('\+.*$', '', last_update)
                result.append('{0}\t:\t{1}\t|\t\t{2}'.format(name, total, last_update))
            except Exception as e:
                result.append('{0}\t:\t{1}'.format(name, e))
        print('\n'.join(result))
        self.final['latest_update'] = result
        # return result
if __name__ == '__main__':
    latest_update().final.get('latest_update')