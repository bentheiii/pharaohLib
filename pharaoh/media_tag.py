class MediaTag(str):
    def __new__(cls, *args, **kwargs):
        ret = super().__new__(cls, *args, **kwargs)
        if ret.isspace() or ret == '':
            raise Exception('tag cannot be empty')  # todo better exception type
        return ret
