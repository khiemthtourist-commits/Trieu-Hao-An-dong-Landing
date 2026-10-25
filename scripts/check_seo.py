"""Offline pre-publication checks for public pages and the finite content plan."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote, parse_qs
import json
from build_sitemap import BASE, ROOT, Metadata

class Page(Metadata):
    def __init__(self):
        super().__init__(); self.h1=0; self.titles=0; self.descriptions=[]; self.links=[]; self.schema=None
    def handle_starttag(self,tag,attrs):
        super().handle_starttag(tag,attrs); a=dict(attrs)
        if tag=='h1': self.h1+=1
        if tag=='title': self.titles+=1
        if tag=='meta' and a.get('name')=='description': self.descriptions.append(a.get('content',''))
        if tag in ('a','link','script','img'):
            value=a.get('href',a.get('src',''))
            if value: self.links.append(value)
        if tag=='script' and a.get('type')=='application/ld+json': self.schema=''
    def handle_data(self,text):
        if self.schema is not None: self.schema+=text
    def handle_endtag(self,tag):
        if tag=='script' and self.schema is not None:
            json.loads(self.schema); self.schema=None

def check(root=ROOT):
    paths=[*root.glob('*.html'),*(root/'tour').glob('*.html')]
    count=0
    for path in paths:
        page=Page(); page.feed(path.read_text())
        if page.noindex: continue
        rel=path.relative_to(root).as_posix()
        assert page.h1==1, f'{rel}: expected one H1'
        assert page.titles==1, f'{rel}: expected one title'
        assert len(page.descriptions)==1 and page.descriptions[0].strip(), f'{rel}: missing description'
        expected=BASE+('' if rel=='index.html' else rel)
        assert page.canonical==expected, f'{rel}: incorrect canonical'
        for link in page.links:
            u=urlsplit(link)
            if path.parent == root and path.name != 'index.html' and u.path == 'index.html':
                source = parse_qs(u.query).get('from')
                if source:
                    assert source == ['/' + path.name], f'{rel}: incorrect lead-source attribution {link}'
            if u.scheme or u.netloc or not u.path: continue
            target=path.parent/unquote(u.path)
            assert target.exists(), f'{rel}: broken local link {link}'
        count+=1
    plan=json.loads((root/'content/seo-plan-30-days.json').read_text())
    assert len(plan['articles'])==plan['maximum_articles']==12
    assert len({a['slug'] for a in plan['articles']})==12
    for article in plan['articles']:
        assert plan['start'] <= article['scheduled_date'] <= plan['end']
        if article['status'] in ('published','awaiting_verification'):
            assert (root/(article['slug']+'.html')).exists(), 'Ledger refers to missing article'
    print(f'PASS: {count} public pages, local resources, canonical metadata and 12-slot plan.')

if __name__=='__main__': check()
