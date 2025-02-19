say hello
say this is a function file augmented with mecha

if score @s tmp matches 1.. as @a:
    for feature in [
        "multiline",
        "nesting",
        "implicit execute",
        "relative location",
    ]:
        say (feature + " is automatically enabled")
    message = "abc" * 5
    say message.upper()

def you_can_make_functions():
    say you_can_make_functions.__name__.replace("_", " ").capitalize()
    tellraw @a [
        "",
        {"text": "yep"},
    ]
    return "and return values"

say you_can_make_functions()

def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

say fib(7)
say fib(8)
say fib(9)

def default_params_are_neat(
    number,
    result=fib(number),
    thing={
        "number": number,
        "result": result,
    },
):
    say Unlike in python default params are evaluated when the function is called
    say number
    say result
    say thing

default_params_are_neat(12)

say this is basically a custom subset of python
say functions are first-class objects just like in python

my_functions = []

for i in "abc":
    def functions_in_loop(value):
        def yo():
            say value.upper()
        return yo
    my_functions.append(functions_in_loop(i * 3))

my_functions[0]()
my_functions[1]()
my_functions[2]()

should_break = False

while True:
    if should_break:
        break
    say just once
    should_break = True

something = '{"text": "Hello", "bold": true}'
as @a at @s if block ~ ~-1 ~ #wool give @s stone{
    display: {
        Name: something
    }
}

with_tuples = ((((())))) + (1,2,3) + (4,)
say with_tuples
say (with_tuples)
say (with_tuples,)
a = f'\\'
say f"f-strings {"work".upper()!r} too {a}"
say f"{{{f"{{{f"{{{7:08}}}\\"}}}\""}}}"

x = 8
if score @s tmp matches (x, None) say wat
if score @s tmp matches f"{x}.." say wat


def copy_items(type, count):
    for i in range(count):
        item replace entity @a f"{type}.{i}" from entity @s f"{type}.{i}"

copy_items('hotbar', 9)
copy_items('inventory', 26)

def f():
    yield 1
    yield 2
    yield 3

for i in f():
    say i

def wow(ok):
    yield from ok()
    yield from ok()

say list(wow(f))

say ctx.generate.id("hello")

import math
say math.cos(math.pi)

import math as m
say (math is m)

from ./thing import do_stuff

say do_stuff(1, math.pi)

import ./thing as thing

say (thing.do_stuff is do_stuff)

for i in range(6):
    if i == 1:
        say 1
    elif i == 2:
        say 2
    elif i == 3:
        say 3
    else:
        say other
    say done

execute
    as @a                        # For each "player",
    at @s                        # start at their feet.
    anchored eyes                # Looking through their eyes,
    facing 0 0 0                 # face perfectly at the target
    anchored feet                # (go back to the feet)
    positioned ^ ^ ^1            # and move one block forward.
    rotated as @s                # Face the direction the player
                                 # is actually facing,
    positioned ^ ^ ^-1           # and move one block back.
    if entity @s[distance=..0.6] function ./abc:
        say foo
        say bar

baz = "demo:xyz"
if predicate foo:bar function baz:
    say foo
    say bar

for node in generate_tree("abcdefghijklmnopqrstuvwxyz0123456789"):
    function node.parent append:
        if node.partition(5):
            if score @s thingy matches node.range function node.children
        else:
            if score @s thingy matches node.range say node.value

data modify entity @e[type=armor_stand,limit=1] NoBasePlate set value 1b

from ./thing import call_recursive
call_recursive()

def try_coordinates():
    a = 1
    setblock a 2 3 stone
    a = "1 2 3"
    setblock a stone
    a = 1
    if block ^ f"^{a}" ^ #planks say 42
    if block ("~", "~", "~") #planks say 42

try_coordinates()

keyword_arguments = dict(foo=1, bar=2, **{"thing": 42})
say keyword_arguments

for node in generate_tree(range(8), name="small_tree"):
    function node.parent append:
        if node.partition():
            if score @s thingy matches node.range function node.children
        else:
            if score @s thingy matches node.range say node.value

def try_unpacking():
    a = [1, *"abc", 2]
    b = dict(zip(a, a))
    c = {**b, "b": "thing"}
    say c

try_unpacking()

def try_set_item():
    try_set_item.data = {}
    try_set_item.data[1] = {}
    try_set_item.data[1][2] = "foo"
    say try_set_item.data

try_set_item()

for node in generate_tree(range(10, 20), key=int):
    function node.parent append:
        if node.partition():
            if score @s thingy matches node.range function node.children
        else:
            if score @s thingy matches node.range say node.value

scoreboard objectives setdisplay list some_score_name
color = "red"
scoreboard objectives setdisplay f"sidebar.team.{color}" some_score_name

weapon = {1: "weapon.offhand", 2: "weapon.mainhand"}
item replace entity @s weapon.offhand from entity @s weapon.mainhand
my_weapon = weapon
item replace entity @s my_weapon.1 from entity @s my_weapon.2

numbers = list(range(12))
say numbers[:]
say numbers[3:]
say numbers[:9]
say numbers[3:9]
say numbers[::]
say numbers[3::]
say numbers[:9:]
say numbers[3:9:]
say numbers[::-1]
say numbers[9::-1]
say numbers[:3:-1]
say numbers[9:3:-1]

execute at @s if block ~ ~ ~ #minecraft:beds:
    teleport @s ~ ~0.56250 ~

del numbers[3:]
say numbers

for loop in loop_info("abcd"):
    say f"==[{loop.current}]=="
    say loop.before
    say loop.after
    say loop.first
    say loop.last
    say loop.cycle("foo", "bar")

from ./thing import raw

raw(f"say hello{'!' * 5}")

run function demo:bbb:
    say 1
run function demo:bbb append:
    say 2
run function demo:bbb prepend:
    say 0
