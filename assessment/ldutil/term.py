class Term:
  def __init__(self, value=None, type='IRI', **extra):
    self.value = value
    self.type = type
    self.extra = extra

  def to_dict(self):
    return dict(type=self.type, value=self.value, **self.extra)
  
  def __repr__(self):
    return '{type}({value}{extra})'.format(
      type=self.type,
      value=self.value,
      extra=(', ' + ', '.join(map('='.join, self.extra.items()))) if self.extra else ''
    )

  def __str__(self):
    if self.type == 'IRI' and self.value == 'https://www.w3.org/1999/02/22-rdf-syntax-ns#type':
      return '@type'
    else:
      return str(self.value)

  def __hash__(self):
    return hash((self.value, self.type, str(self.extra)))

  def __lt__(self, other):
    return hash(self) < hash(other)
  
  def __gt__(self, other):
    return hash(self) > hash(other)

  def __eq__(self, other):
    return hash(self) == hash(other)
