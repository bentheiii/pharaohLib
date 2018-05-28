from typing import Dict, Type
from abc import abstractmethod

from functools import lru_cache

import pafy

from .media_tag import MediaTag
from .pack import Packing, Unpacking, p_, u_
from .encoding_hierarchy import Encoded


class Media(Encoded['Media']):
    @abstractmethod
    def tags(self):
        pass

    @abstractmethod
    def mrl(self):
        pass


class StandardMedia(Media):
    def __init__(self, tags, title):
        self._tags = tags
        self.title = title
        super().__init__()

    @classmethod
    @abstractmethod
    def decode_to_dict(cls, kwargs, unpacking: Unpacking, format_prefix):
        part = unpacking.pop()
        tags_raw, title = u_(part)
        kwargs['tags'] = set(MediaTag(t) for t in u_(tags_raw))
        kwargs['title'] = title
        super().decode_to_dict(kwargs, unpacking, format_prefix)

    def tags(self):
        return self._tags

    def encode(self, packing: Packing):
        part = p_(p_(*self._tags), self.title)
        packing.append(part)
        super().encode(packing)

    def __str__(self):
        return self.title


class YoutubeMedia(StandardMedia):
    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        if not self.title:
            self.title = self._pafy().title

    @classmethod
    def decode_to_dict(cls, kwargs, unpacking: Unpacking, format_prefix):
        assert format_prefix in ['y0']
        part = unpacking.pop()
        kwargs['url'] = part
        super().decode_to_dict(kwargs, unpacking, format_prefix)

    def encode(self, packing: Packing):
        packing.append(self.url)
        super().encode(packing)

    @classmethod
    def format_prefix(cls):
        return 'y0'

    @lru_cache(maxsize=None)
    def _pafy(self):
        return pafy.new(self.url)

    def mrl(self):
        best = self._pafy().getbest()
        play_url = best.url
        return play_url

    def __str__(self):
        return super().__str__() + ' (source: youtube)'

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url


class FileMedia(StandardMedia):
    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    @classmethod
    def decode_to_dict(cls, kwargs, unpacking: Unpacking, format_prefix):
        assert format_prefix in ['f0']
        part = unpacking.pop()
        kwargs['path'] = part
        super().decode_to_dict(kwargs, unpacking, format_prefix)

    def encode(self, packing: Packing):
        packing.append(self.path)
        super().encode(packing)

    @classmethod
    def format_prefix(cls):
        return 'f0'

    def mrl(self):
        return self.path

    def __str__(self):
        return super().__str__() + ' (source: file)'


Media.prefix_dict: Dict[str, Type[Media]] = {'y0': YoutubeMedia, 'f0': FileMedia}
