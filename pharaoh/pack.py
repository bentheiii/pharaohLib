from typing import List, Iterable


def _append_size(x: str):
    x = str(x)
    length = len(x)
    prefix = str(length) + ':'
    return prefix + x


class Packing:
    def __init__(self):
        self.parts: List[str] = []

    def append(self, part):
        self.parts.append(_append_size(part))

    def extend(self, parts):
        for p in parts:
            self.append(p)

    def dump(self):
        return ''.join(self.parts)

    @classmethod
    def pack(cls, *parts: Iterable[str]) -> str:
        p = cls()
        p.extend(parts)
        return p.dump()


class Unpacking:
    def __init__(self, whole: str):
        self.whole = whole

    def pop(self):
        if not self.whole:
            raise Exception('the string has been fully unpacked')
        size, whole = self.whole.split(':', maxsplit=1)
        size = int(size)
        ret, whole = whole[:size], whole[size:]

        self.whole = whole
        return ret

    def __bool__(self):
        return bool(self.whole)

    def pop_many(self, count):
        for _ in range(count):
            yield self.pop()

    def __iter__(self):
        while self:
            yield self.pop()

    @classmethod
    def unpack(cls, whole: str) -> List[str]:
        p = cls(whole)
        return list(p)


p_ = Packing.pack
u_ = Unpacking.unpack
