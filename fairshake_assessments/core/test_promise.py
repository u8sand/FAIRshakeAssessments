from unittest import TestCase
from .promise import Promise, promise

@promise
def test1(a, b, c=None):
  return a + b + c

@promise
def test2():
  return 3

class PromiseTest(TestCase):
  def test_promise(self):
    p1 = test1(1, 2, c=str(test2()))

    self.assertEqual(Promise.resolve(str(p1)), 6)
