from typing import Dict, Any, Generic, TypeVar, Type
from abc import ABC, abstractmethod

import warnings
from .pack import Packing, Unpacking

T = TypeVar('T', bound='Encoded')


class Encoded(ABC, Generic[T]):
    prefix_dict: Dict[str, Type[T]]

    @classmethod
    @abstractmethod
    def decode_to_dict(cls, kwargs: Dict[str, Any], unpacking: Unpacking, format_prefix: str):
        """
        each layer is to parse it's share of the string and pass the rest to its super.
        """
        if unpacking:
            warnings.warn('leftover string: ' + repr(unpacking.whole))
        pass

    @classmethod
    def from_encoding(cls, line: str) -> T:
        try:
            format_prefix, rest = line.split('|', 1)
        except TypeError as e:
            raise TypeError('could not split line by "|"') from e
        handler = cls.prefix_dict.get(format_prefix, None)
        if not handler:
            raise ValueError('cannot handle media kind: ' + format_prefix)
        kwargs = {}
        handler.decode_to_dict(kwargs, Unpacking(rest), format_prefix)
        return handler(**kwargs)

    def to_encoding(self):
        ret = Packing()
        self.encode(ret)
        return self.format_prefix() + '|' + ret.dump()

    @abstractmethod
    def encode(self, packing: Packing):
        pass

    @classmethod
    @abstractmethod
    def format_prefix(cls):
        pass
