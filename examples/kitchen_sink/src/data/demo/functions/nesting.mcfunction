as @a at @s
    say hello
    say world

as @a at @s
    if score @s tmp matches 1
        say hello
        say world

function ./nesting/foo
    say
        this
        is
        a
        test

as @a at @s expand
    say 1
    say 2

as @a at @s
    if score @s tmp matches 1
        expand
            say 1
            say 2



if data storage imp:temp iter.words.remaining[] function ./nesting/loop
    say wow
    if data storage imp:temp iter.words.remaining[] function ./nesting/loop
