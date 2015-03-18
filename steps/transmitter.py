from behave import matchers
from should_dsl import should, should_not

from transmit import checksum

@given(u'a data string {s}')
def step_impl(context, s):
    context.s = s

@when(u'the checksum is being calculated')
def step_impl(context):
    context.cs = checksum(context.s)

@then(u'the result should be {expected}')
def step_impl(context, expected):
    context.cs |should| equal_to(expected)
