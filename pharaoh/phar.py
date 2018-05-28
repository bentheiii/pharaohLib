from typing import List

from .media import Media


class Phar:
    encoding_version = 0

    def __init__(self):
        self.medias: List[Media] = []
        self.media_sources = []