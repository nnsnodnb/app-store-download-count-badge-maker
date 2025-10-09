from maker.config import Config


def test_make_index_html_text(config: Config):
    actual = config.make_index_html_text()

    expected = """<!DOCTYPE html>
<html>
<body>
<ul>
<li><a href="./1289764391-month.svg">1289764391-month.svg</a></li>
<li><a href="./1234567890-week.svg">1234567890-week.svg</a></li>
<li><a href="./1234567890-day.svg">1234567890-day.svg</a></li>
<li><a href="./1234567890-year.svg">1234567890-year.svg</a></li>
<li><a href="./1234567890-year.svg">1234567890-year.svg</a></li>
</ul>
</body>
</html>""".replace("\n", "")

    assert actual == expected
