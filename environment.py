import shutil
import tempfile

def before_scenario(context, scenario):
    context.logdir = tempfile.mkdtemp()

def after_scenario(context, scenario):
    shutil.rmtree(context.logdir)
