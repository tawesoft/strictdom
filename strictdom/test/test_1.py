import pytest
import strictdom.tags_1 as tags


def test_empty_attributes():
    tags.div().render() == """<div></div>"""
    tags.div("Hello world").render() == """<div>Hello world</div>"""


def test_boolean_attributes_true():

    el = tags.button("Hello world",
        translate=True,         # translate="yes|no"
        spellcheck=True,        # spellcheck="true|false"
        disabled=True,          # disabled="disabled" or omitted entirely
    )

    assert el.render() == \
           """<button disabled="disabled" spellcheck="true" translate="yes">Hello world</button>"""


def test_boolean_attributes_false():

    el = tags.button("Hello world",
        translate=False,        # translate="yes|no"
        spellcheck=False,       # spellcheck="true|false"
        disabled=False,         # disabled="disabled" or omitted entirely
    )

    assert el.render() == \
           """<button spellcheck="false" translate="no">Hello world</button>"""


def test_reserved_keyword_attributes():

    el = tags.div("Hello world",
        class_="class_name"
    )

    assert el.render() == \
           """<div class="class_name">Hello world</div>"""


def test_keyword_attributes():
    el = tags.div("Hello world",
        autocapitalize="sentences"
    )

    assert el.render() == \
           """<div autocapitalize="sentences">Hello world</div>"""


def test_void():

    assert tags.br().render() == """<br>"""
    assert tags.br().render(xhtml=True) == """<br />"""


def test_any():

    assert tags.embed(foo="bar").render() == """<embed foo="bar">"""
    assert tags.math(foo="bar").render() == """<math foo="bar"></math>"""


def test_aria():

    el = tags.div("Hello world",
        role="button",
        aria=tags.Aria(pressed="true")
    )

    assert el.render() == """<div aria-pressed="true" role="button">Hello world</div>"""


def test_data():

    el = tags.div("Hello world",
        custom={"foo": "bar", "color": "red"}
    )

    assert el.render() == """<div data-color="red" data-foo="bar">Hello world</div>"""


def test_events():

    el = tags.div("Hello world",
        events=tags.Events(
            drag="""alert("Drag Event!");""",
            click="""alert("Click Event!");""",
        )
    )

    assert el.render() == """<div onclick="alert(&quot;Click Event!&quot;);" ondrag="alert(&quot;Drag Event!&quot;);">Hello world</div>"""


def test_raw_text_elements():

    # e.g. <script>, <style>
    assert tags.script().render() == """<script></script>"""
    assert tags.script(src="foo.js").render() == """<script src="foo.js"></script>"""

    assert tags.script("""
    foo();
    if (a > b) ...
""").render() == """<script>
    foo();
    if (a > b) ...
</script>"""

    with pytest.raises(Exception):
        tags.script("""</sCrIpT>""").render() == "anything"

    with pytest.raises(Exception):
        tags.style("""</sTyLe>""").render() == "anything"


def test_escapable_raw_text_elements():
        # e.g. <textarea>, <title>
        assert tags.textarea().render() == """<textarea></textarea>"""
        assert tags.textarea("Hi<b>!", class_="hello").render() == \
           """<textarea class="hello">Hi&lt;b&gt;!</textarea>"""

