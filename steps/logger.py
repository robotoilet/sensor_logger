import os
import re

from behave import matchers
from should_dsl import should, should_not

from sensor_logger import log_datapoint

matchers.register_type(integer=lambda s: int(s))


@given(u'a maximal amount of {number:integer} of datapoints per file')
def step_impl(context, number):    
    context.max_datapoints = number

@when(u'I log these datapoints: {string}')
def step_impl(context, string):
    for datapoint in re.findall('\([^\)]+\)', string):
        log_datapoint(datapoint, max_datapoints=context.max_datapoints,
                logdir=context.logdir) 

@then(u'the total number of logfiles is {number:integer}')
def step_impl(context, number):
    context.logfiles = [os.path.join(context.logdir, f)
                        for f in os.listdir(context.logdir)
                        if os.path.isfile(os.path.join(context.logdir, f))]
    len(context.logfiles) |should| equal_to(number)

@then(u'the file(s) content is: {string}')
def step_impl(context, string):
    expected_content = set(s.strip() for s in string.split(','))
    real_content = set()
    for logfile in context.logfiles:
        with open(logfile, 'r') as lf:
            real_content.add(lf.read())
    real_content |should| equal_to(expected_content)

@then(u'the name of each logfile contains the timestamp of its first datapoint ({content})')
def step_impl(context, content):
    expected = [re.findall('\d{10}', c)[0] for c in content.split(',')]
    # NOTE: this test only works because the datapoints and hence filenames are
    #       sorted, as in the first datapoint is the oldest.
    for i, logfile in enumerate(sorted(context.logfiles)):
        re.findall('\d{10}', logfile)[0] |should| equal_to(expected[i])

@then(u'the older logfile has been renamed to start with a "C" instead of a T')
def step_impl(context):
    sorted(context.logfiles)[0].split('/')[-1] |should| start_with("C")
