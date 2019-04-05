from ..core import promise, rule

_context = {
  '@vocab': 'https://schema.org/',
  'fairsharing': 'https://fairsharing.org/',
  'html': 'fairsharing:bsg-s001284',
}

def first_or(l, o):
  if len(l) == 0:
    return o
  else:
    return l[0]

@promise
def resolve_basic_url_meta(html):
  from bs4 import BeautifulSoup
  soup = BeautifulSoup(html)
  title = first_or(soup.select('title'), {'text': ''}).text
  description = first_or(soup.select('meta[name="description"]'), {}).get('content', '')
  keywords = first_or(soup.select('meta[name="keywords"]'), {}).get('content', '')
  image = first_or(soup.select('meta[itemprop="image"]'), {}).get('content', '')
  if image == '':
    image = first_or(soup.select('link[rel="shortcut icon"]'), {}).get('href', '')

  return {
    'title': title,
    'description': description,
    'keywords': keywords,
    'image': image,
  }

@rule({
  '@context': _context,
  '@id': {},
  'html': {},
})
def basic_url_meta_resolver(ld):
  resolved = resolve_basic_url_meta(ld['html'])
  return dict(ld, **{
    'title': resolved['title'],
    'description': resolved['description'],
    'keywords': resolved['keywords'],
    'image': resolved['image'],
  })
