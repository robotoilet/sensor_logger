from sensors import test_sensor, hc_sr04

CONFIG = {
    'max_dp': 5,
    'logdir': 'logs',
    'collect-res': 1,
    'send-res': 5,
    'server': 'ec2-54-154-18-166.eu-west-1.compute.amazonaws.com',
    'site': 'siteX',
    'credentials': ['punterX', 'punterX'],
    'sensors': [
        {'name': 'x',
         'sensor': test_sensor,
         'kwargs': {},
         'res': 1},
#        {'name': 'y',
#         'sensor': hc_sr04,
#         'kwargs': {'trigger': 17, 'echo': 18},
#         'res': 3},
    ],
}
