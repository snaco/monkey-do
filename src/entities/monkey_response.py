"""Entity for the mock response"""
from dataclasses import dataclass
from typing import Union


@dataclass
class MonkeyResponse():
    """Object representation of an monkey http response"""
    status: int = 200
    body: Union[str, dict] = None
    script: str = None
    mime_type: str = 'text/plain'
