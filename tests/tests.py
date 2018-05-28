import unittest

import pharaoh.pack
import pharaoh.media
import pharaoh.media_tag


def medTags(x: str):
    return {pharaoh.media_tag.MediaTag(t) for t in x.split()}


class PackTest(unittest.TestCase):
    inputs = [
        ['a', 'b', 'c'],
        ['a', ':'],
        ['', '*:*', '', 'arc:', '::*::*:::*:::***::', ':b', 'c', ':*:co:*:rr:*:', ''],
        ['*:*', '', 'arc:', '::*::*:::*:::***::', ':b', 'c', ':*:co:*:rr:*:', ''],
        ['', '*:*', '', 'arc:', '::*::*:::*:::***::', ':b', 'c', ':*:co:*:rr:*:'],
        ['*:*', '', 'arc:', '::*::*:::*:::***::', ':b', 'c', ':*:co:*:rr:*:'],
    ]

    def test_simple(self):
        for i in self.inputs:
            p = pharaoh.pack.Packing()
            p.extend(i)
            code = p.dump()
            u = pharaoh.pack.Unpacking(code)
            decoded = list(u)
            self.assertSequenceEqual(i, decoded)

    def test_recursive(self):
        inputs = [pharaoh.pack.Packing.pack(*i) for i in self.inputs]
        coded = pharaoh.pack.Packing.pack(*inputs)
        decoded = pharaoh.pack.Unpacking.unpack(coded)
        parts = [pharaoh.pack.Unpacking.unpack(i) for i in decoded]
        self.assertSequenceEqual(self.inputs, parts)


class EncodingTest(unittest.TestCase):
    def Trial(self, media: pharaoh.media.Media):
        original_mrl = media.mrl()
        packed = media.to_encoding()
        unpacked = media.from_encoding(packed)
        new_mrl = unpacked.mrl()
        self.assertEqual(original_mrl, new_mrl, str(media))
        self.assertSetEqual(media.tags(), unpacked.tags())
        self.assertEqual(str(media), str(unpacked))

    def test_file(self):
        self.Trial(
            pharaoh.media.FileMedia(r'file:///D:/path/to/file', title='the lonely soldier', tags=medTags('a b c')))

    def test_yt(self):
        med = pharaoh.media.YoutubeMedia(r'https://www.youtube.com/watch?v=ylqEN7J3GLA', title='',
                                         tags=medTags('g q ih'))
        self.Trial(med)
        self.assertTrue(med.title)
