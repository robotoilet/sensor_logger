from sensors import test_sensor, hc_sr04

CONFIG = {
    'max_dp': 5,
    'logdir': 'logs',
    'collect-res': 1,
    'send-res': 5,
    'server': 'localhost',
    'site': 'siteX',
    'credentials': ['punterX', 'punterX'],
    'sensors': [
        {'name': 'a',
         'sensor': test_sensor,
         'kwargs': {},
         'res': 1},
        #{'name': 'usage',
        # 'sensor': hc_sr04,
        # 'kwargs': {'trigger': 17, 'echo': 18},
        # 'res': 10}],
    ],
}
