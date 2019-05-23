Strictdom
=========

Stictdom is a strongly-typed front-end to
[Dominate](https://github.com/Knio/dominate/pull/111), a Python library for
creating and manipulating HTML documents.

Compared to using Dominate directly, strictdom offers:

* Type hints for code-completion / IntelliSense / IDE hints

* Type hints and explicit arguments for [HTML5](https://html.spec.whatwg.org/multipage/)
  & [ARIA](https://w3c.github.io/aria/) conformance at runtime, or at
  compile-time with [mypy](http://mypy-lang.org/).

Features:

* Nothing new to learn - mostly the same interface as vanilla.
* Stable versioned interface e.g. `strictdom.tags_1` is a frozen view of the spec


Example: Vanilla vs Strict
--------------------------

### "Vanilla" Dominate

    import dominate.tags as dom

    print(dom.button("Hello world",
        cls="hello",
        some_invalid_tag="hello",
        onclick="alert('Hello world');"
    ))


### Strictdom

    import strictdom.tags_1 as tags

    print(tags.button("Hello world",
        class_="hello",
        # some_invalid_tag="hello",
        events=tags.Events(click="alert('Hello world');")
    ))


`some_invalid_tag` will raise a runtime error if not removed:

    TypeError: __init__() got an unexpected keyword argument 'some_invalid_tag'



TODO
----

* Tests
* Fix handling of booleans at the Strictdom layer to avoid mypy complaining
  about mixing string and bool values in a dict.
* Fix handling of booleans at the Strictdom layer so that weird
  "true"|"false", "yes"|"no" attributes can be simple booleans.




