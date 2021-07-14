class Meta:
    META_TYPES = ['artist', 'album', 'track', 'song', 'year']

    def __init__(self, meta_type, value):
        if meta_type in Meta.META_TYPES:
            self.meta_type = meta_type
        else:
            raise ValueError

        self.value = value
