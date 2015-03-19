from sensors import test_sensor, hc_sr04

CONFIG = {
    'max_dp': 5,
    'logdir': 'logs',
    'collect-res': 1,
    'send-res': 5,
    'server': 'localhost',
    'site': 'raspberry-land',
    'credentials': ['dotslashrobot', 'dotslashrobot'],
    'sensors': [
        {'name': 'x',
         'sensor': test_sensor,
         'kwargs': {},
         'res': 1},
        #{'name': 'y',
        # 'sensor': hc_sr04,
        # 'kwargs': {'trigger': 17, 'echo': 18},
        # 'res': 10}],
    ],
}
