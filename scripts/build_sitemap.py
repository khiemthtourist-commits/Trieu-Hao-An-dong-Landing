"""Generate a stable sitemap from public HTML pages; no synthetic lastmod dates."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

BASE = 'https://www.trieuhaoandong.com/'
ROOT = Path(__file__).resolve().parents[1]

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.noindex = False
        self.canonical = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and a.get('name', '').lower() in ('robots', 'googlebot'):
            self.noindex |= 'noindex' in a.get('content', '').lower()
        if tag == 'link' and 'canonical' in a.get('rel', '').lower().split():
            self.canonical = a.get('href')

def collect(root):
    urls = set()
    for f in sorted(root.rglob('*.html')):
        relative = f.relative_to(root)
        if any(part.startswith('.') or part in ('node_modules', 'scripts', 'tests') for part in relative.parts):
            continue
        meta = Metadata()
        meta.feed(f.read_text(encoding='utf-8'))
        if meta.noindex:
            continue
        path = relative.as_posix()
        url = urljoin(BASE, '' if path == 'index.html' else path)
        if meta.canonical:
            canonical = urljoin(url, meta.canonical)
            if canonical != url:
                continue
        if urlsplit(url).netloc == urlsplit(BASE).netloc:
            urls.add(url)
    return sorted(urls)

def build(root=ROOT):
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    xml = ET.Element('{'+ns+'}urlset')
    for url in collect(root):
        item = ET.SubElement(xml, '{'+ns+'}url')
        ET.SubElement(item, '{'+ns+'}loc').text = url
    ET.indent(xml, space='  ')
    ET.ElementTree(xml).write(root / 'sitemap.xml', encoding='UTF-8', xml_declaration=True)
    print('Sitemap generated:', len(xml), 'public pages')

if __name__ == '__main__':
    build()
