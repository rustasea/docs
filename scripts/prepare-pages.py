import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SOURCE = Path(".docu/dist")
PAGES = Path(".pages")


class Rewrite(HTMLParser):
    def __init__(self, depth):
        super().__init__(convert_charrefs=False)
        self.depth, self.out = depth, []

    def handle_starttag(self, tag, attrs):
        attrs = [
            (
                n,
                self.url(v)
                if n in {"href", "src"}
                or (
                    n == "content"
                    and any(a == "property" and b == "og:url" for a, b in attrs)
                )
                else v,
            )
            for n, v in attrs
        ]
        rendered = " ".join(n if v is None else f'{n}="{v}"' for n, v in attrs)
        self.out.append(f"<{tag}" + (f" {rendered}" if rendered else "") + ">")

    def url(self, value):
        if value is None:
            return value
        parsed = urlparse(value)
        internal = not parsed.scheme and not parsed.netloc
        if parsed.netloc == "rustasea.github.io":
            internal = True
        if parsed.netloc == "github.com" and parsed.path.startswith("/rustasea/docs/"):
            internal = True
        if not internal:
            return value
        if self.depth == 0:
            prefixes, replacement = ("../docs/assets/", "../assets/"), "assets/"
        else:
            prefixes, replacement = (
                ("../../docs/assets/", "../../assets/"),
                "../assets/",
            )
        value = value.replace(prefixes[0], replacement).replace(
            prefixes[1], replacement
        )
        value = value.replace("/docs/docs", "/docs").replace("docs/docs/", "docs/")
        return "/docs" + value if value.startswith("/assets/") else value

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.out[-1] = self.out[-1][:-1] + "/>"

    def handle_endtag(self, tag):
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        self.out.append(data)

    def handle_entityref(self, name):
        self.out.append(f"&{name};")

    def handle_charref(self, name):
        self.out.append(f"&#{name};")

    def handle_comment(self, data):
        self.out.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.out.append(f"<!{decl}>")

    def handle_pi(self, data):
        self.out.append(f"<?{data}>")


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, tag, attrs):
        self.values += [
            v.split("#", 1)[0] for n, v in attrs if n in {"href", "src"} and v
        ]


def local_target(page, ref):
    if ref in {"/docs", "/docs/"}:
        return PAGES / "index.html"
    if ref.startswith("/docs/"):
        return PAGES / ref.removeprefix("/docs/")
    return (page.parent / ref).resolve()


# Publish dist/docs as the artifact root. dist/index.html belongs to the
# separate project landing page and is intentionally not included.
shutil.rmtree(PAGES, ignore_errors=True)
(PAGES / "assets").mkdir(parents=True)
shutil.copytree(SOURCE / "docs", PAGES, dirs_exist_ok=True)
shutil.copytree(SOURCE / "assets", PAGES / "assets", dirs_exist_ok=True)
for name in (".nojekyll", "404.html", "_headers"):
    source = SOURCE / name
    if source.exists():
        shutil.copy2(source, PAGES / name)
for page in PAGES.rglob("*.html"):
    parser = Rewrite(len(page.relative_to(PAGES).parents) - 1)
    parser.feed(page.read_text())
    page.write_text("".join(parser.out))
for page in PAGES.rglob("*.html"):
    parser = References()
    parser.feed(page.read_text())
    for ref in parser.values:
        parsed = urlparse(ref)
        if parsed.scheme or parsed.netloc or not ref or ref.startswith("#"):
            continue
        target = local_target(page, ref)
        if not target.exists():
            raise SystemExit(f"missing {target} referenced by {page}")
if any("/docs/docs" in page.read_text() for page in PAGES.rglob("*.html")):
    raise SystemExit("artifact contains /docs/docs")
print(f"prepared {len(list(PAGES.rglob('*.html')))} pages")
