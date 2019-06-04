import strictdom.tags_1 as tags
import dominate.tags as dom

"""


print(tags.button("Hello world",
    aria=tags.Aria(pressed="true"),
    class_="hello",
    # some_invalid_tag="hello",
    custom={"foo": "bar"},
    disabled=True,
    events=tags.Events(click="alert('Hello world');")
))

# Commented-out line gives:
# TypeError: __init__() got an unexpected keyword argument 'some_invalid_tag'

"""


def print_foo():

    print(tags.button("Hello world",
        class_="hello",
        # some_invalid_tag="hello",
        events=tags.Events(click="alert('Hello world');")
    ))


print_foo()


print(dom.button("Hello world",
    cls="hello",
    some_invalid_tag="hello",
    onclick="alert('Hello world');"
))
