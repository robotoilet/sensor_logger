from datetime import datetime
import os.path
import re
import time

import sensor_config

from transmit import send_data

SENSOR_CFG = sensor_config.CONFIG

def create_logfilepath(datapoint, logdir):
    """
    Find the first occurrence of a 10digit unix timestamp in a string,
    return a filepath (string) of format "<logdir>/L<timestamp>"
    """
    timestamp = re.findall('\d{10}', datapoint)[0]
    return os.path.join(logdir, 'L%s' % timestamp)

def tracked(log_function):
    """
    Decorator to start writing to a new logfile after max_datapoints
    """
    track = {
        'count': 0,
        'logfile': None,
    }
    def tracked_log(datapoint, max_datapoints=5, logdir='.'):
        lf = track.get('logfile')
        if not lf or logdir.split('/') != lf.split('/')[:-1]:
            track['logfile'] = create_logfilepath(datapoint, logdir)
            track['count'] = 0
        log_function(datapoint, track['logfile'])
        count = track['count'] + 1
        track['count'] = (count < max_datapoints) and count or 0
        if not track['count']:
            print("closing logfile %s.." % track['logfile'])
            os.rename(track['logfile'],
                      re.sub('L(?=\d{10})', 'C', track['logfile']))
            track['logfile'] = None
    return tracked_log

@tracked
def log_datapoint(datapoint, logfile):
    print('logging datapoint %s to file %s' % (datapoint, logfile))
    with open(logfile, 'a') as f:
        f.write(datapoint)

def run():
    sensors = [{'name': sr['name'], 'res': sr['res'],
                'kwargs': sr['kwargs'], 'sense': sr['sensor'].setup()}
               for sr in SENSOR_CFG['sensors']]
    prev = None

    logdir = SENSOR_CFG['logdir']
    closed_logfiles = (f for f in os.listdir(logdir) if f.startswith('C'))
    while True:
        ts = datetime.now()
        if ts.second == prev:
            continue
        #if ts.second % SENSOR_CFG['collect-res'] == 0:
        #    for sr in sensors:
        #        if ts.second % sr['res'] == 0:
        #            dp = '(%s %s %s)' % (sr['name'], ts.strftime('%s'),
        #                                 sr['sense'](**sr['kwargs']))
        #            try:
        #              log_datapoint(dp, SENSOR_CFG['max_dp'], logdir)
        #            except Exception as e:
        #              msg = "could not get data for sensor {}, exeption was {}"
        #              print(msg.format(sr['name'], e))
        if ts.second % SENSOR_CFG['send-res'] == 0:
            try:
                next_file = closed_logfiles.next()
            except StopIteration: # last filelist used? try to create new one
                closed_logfiles = (f for f in os.listdir(logdir)
                                   if f.startswith('C'))
                try:
                    next_file = closed_logfiles.next()
                except StopIteration:
                    continue # nothing to send
            try:
                send_data(next_file)
            except Exception as e:
                msg = "Could not send data, exception was: {}"
                print(msg.format(e))

        prev = ts.second

if __name__ == '__main__':
    run()
