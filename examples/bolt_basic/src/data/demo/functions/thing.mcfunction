from mecha import Mecha
from mecha.contrib.bolt import Runtime

mc = ctx.inject(Mecha)
runtime = ctx.inject(Runtime)

def do_stuff(a, b):
    import math
    return a + math.cos(b)

def call_recursive():
    if score @s loop_again matches 1 function runtime.get_path()

def raw(cmd):
    runtime.commands.append(mc.parse(cmd, using="command"))
