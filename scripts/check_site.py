"""Read-only production checks. Never submit forms or create test leads."""
from urllib.request import Request, urlopen
from urllib.parse import urlsplit, urljoin
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import time

BASE = 'https://www.trieuhaoandong.com/'

def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'TrieuHaoWebsiteHealthCheck/1.0'}), timeout=25) as response:
                if response.status != 200:
                    raise ValueError('Unexpected HTTP status: '+str(response.status))
                if urlsplit(response.url).hostname != urlsplit(BASE).hostname:
                    raise ValueError('Unexpected redirect outside website')
                return response.read().decode('utf-8')
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.scripts=[]; self.noindex=False; self.h1=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='script' and a.get('src'): self.scripts.append(a['src'])
        if tag=='meta' and a.get('name','').lower() in ('robots','googlebot'):
            self.noindex |= 'noindex' in a.get('content','').lower()

def main():
    robots=fetch(BASE+'robots.txt')
    assert 'Sitemap: '+BASE+'sitemap.xml' in robots, 'Missing sitemap in robots.txt'
    assert not any(line.strip().lower()=='disallow: /' for line in robots.splitlines()), 'robots blocks crawling'
    root=ET.fromstring(fetch(BASE+'sitemap.xml'))
    urls=[n.text for n in root.findall('{*}url/{*}loc')]
    assert urls and len(urls)==len(set(urls)), 'Empty or duplicate sitemap'
    for url in urls:
        assert url.startswith(BASE), 'Unexpected sitemap domain'
        page=Page(); page.feed(fetch(url))
        assert not page.noindex, 'noindex URL in sitemap: '+url
        assert page.h1==1, 'Missing or multiple H1: '+url
        if url==BASE or '/tour/' in url:
            assert {'leadForm','in-name','in-phone','in-note'} <= page.ids, 'Lead form missing: '+url
            assert any('lead-submit.js' in s for s in page.scripts), 'Lead delivery script missing: '+url
    script=fetch(BASE+'assets/lead-submit.js')
    assert 'window.submitLead' in script and 'script.google.com/macros/' in script, 'Lead endpoint configuration missing'
    print('PASS:', len(urls), 'public pages reachable; sitemap, indexing directives and lead form wiring checked.')
    print('Does not verify Google indexing, Apps Script writes, emails or real customer submissions.')

if __name__=='__main__': main()
