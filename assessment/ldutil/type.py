from typing import NewType, List, Dict, Union

JSONLD = NewType('JSONLD', Union[str, int, float, bool, List['JSONLD'], Dict[str, 'JSONLD']])
JSONLDFrame = NewType('JSONLDFrame', JSONLD)
