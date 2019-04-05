from unittest import TestCase
from .expansion import frame_matches_framed, expand, deep_expand
from .ld import LD
from .rule import Rule

_context = 'https://example.com/'

class ExpansionTest(TestCase):
  def test_frame_matches_framed(self):
    self.assertTrue(frame_matches_framed({
      'hello': 'world',
      'goobye': {
        'cruel': {},
        'okay': {
          '@default': None,
        }
      }
    }, {
      'hello': 'world',
      'goobye': {
        'cruel': {
          'world': '!'
        },
        'okay': None,
      }
    }))
    self.assertFalse(frame_matches_framed({
      'hello': 'world',
      'goobye': {
        'cruel': {},
        'okay': {
          '@default': None,
        }
      }
    }, {
      'hello': 'world',
      'goobye': None,
    }))

  def test_expand(self):
    result = expand({
      '@context': { '@vocab': _context },
      '@graph': [
        {
          '@id': _context + '1',
          '@type': 'Hello'
        },
        {
          '@id': _context + '2',
          '@type': 'World'
        },
      ]
    }, [
      Rule(
        { '@context': { '@vocab': _context }, '@id': {}, '@type': _context + 'Hello' },
        lambda arg: { '@context': { '@vocab': _context }, '@id': arg['@id'], 'value': 'world' }
      )
    ])
    expectation = {
      '@context': { '@vocab': _context },
      '@graph': [
        {
          '@id': _context + '1',
          '@type': 'Hello',
          'value': 'world',
        },
        {
          '@id': _context + '2',
          '@type': 'World'
        },
      ]
    }

    if not (LD.from_jsonld(result) == LD.from_jsonld(expectation)):
      self.fail(result)

  def test_deep_expand(self):
    result = expand({
      '@context': { '@vocab': _context },
      '@graph': [
        {
          '@id': _context + '1',
          '@type': 'Hello'
        },
        {
          '@id': _context + '2',
          '@type': 'World'
        },
      ]
    }, [
      Rule(
        { '@context': { '@vocab': _context }, '@id': {}, '@type': _context + 'Hello' },
        lambda arg: { '@context': { '@vocab': _context }, '@id': arg['@id'], 'value': 'world' }
      ),
      Rule(
        { '@context': { '@vocab': _context }, '@id': {}, '@type': _context + 'Hello', 'value': {} },
        lambda arg: { '@context': { '@vocab': _context }, '@id': arg['@id'], '@type': 'World' }
      ),
    ])
    expectation = {
      '@context': { '@vocab': _context },
      '@graph': [
        {
          '@id': _context + '1',
          '@type': ['Hello', 'World'],
          'value': 'world',
        },
        {
          '@id': _context + '2',
          '@type': 'World',
        },
      ]
    }

    if not (LD.from_jsonld(result) == LD.from_jsonld(expectation)):
      self.fail(result)
