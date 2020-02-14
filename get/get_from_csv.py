from controller.controller import Controller
import csv


class from_csv(Controller):

    final = {}

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.fromcsv()

    def fromcsv(self):
        result = []
        result.append('\n*--\tToken\t--*')
        for a in self.config.get('csv','file').split(';'):
            base = csv.reader(open('src/{1}.csv'.format(self.config.get('csv','path'), a),'r'))
            next(base)
            normal = 0
            error = 0
            length = 0
            for b in base:
                if b[0] == '200' or b[0] == 'active': normal += 1
                else: error += 1
                length+=1
            result.append('\n*{3}Token*\n{2} Normal, {0} Error, From {1} Token'.format(error,length,normal,str(a).capitalize()))
            self.final['token']= result
        print ('\n'.join(self.final))

if __name__ == '__main__':
    from_csv()

