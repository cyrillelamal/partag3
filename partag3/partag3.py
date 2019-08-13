import os
import sys
import json
import requests
import bs4
import shutil
from mp3_tagger import MP3File



class Meta:
    """ Meta value """
    META_TYPES = ['artist', 'album', 'track', 'song', 'year']

    def __init__(self, meta_type, value):
        if meta_type in Meta.META_TYPES:
            self.meta_type = meta_type
        else:
            raise IncorrectMetaTypeException
        self.value = value


class TagOnPage(Meta):
    """ Meta value on page can be parsed """
    SIBLINGS = ['tr', 'li']
    ESCAPABLE = {u'\xa0': u'', u'\n': u''}

    def __init__(self, meta_type, url, selector=None, value=None):
        super(TagOnPage, self).__init__(meta_type, value)
        self.url = url
        self.selector = selector

        self.__el = None  # Proxy bs4 element for parsing of lists

    def compile(self):
        """ Set value attribute. """
        html = get_html_by_url(self.url)
        soup = bs4.BeautifulSoup(html, features='html.parser')
        print(f'Parsing {self.meta_type}...')
        try:
            el = soup.select(self.selector)[0]
        except IndexError:
            message = f'{self.meta_type} has not been found'
            raise ElementNotFoundException(message)
        self.value = TagOnPage.escape(el.get_text())
        self.__el = el  # proxy for list
        return self

    @property
    def list_from_siblings(self):
        """
        Get list of values similar to the value obtain with selector.
        The method uses method parameter "SIBLINGS" for limitation of parsing.
        """
        if self.__el is None:
            self.compile()
        el = self.__el
        tag_list = [el.get_text()]
        wrappers, sibling, el = TagOnPage.__get_wrappers(el)
        wrappers.reverse()
        el = el.find_next_sibling(sibling)
        while el is not None:
            el, txt = TagOnPage.__next_sibling_and_val(el, sibling, wrappers)
            tag_list.append(txt)
        return tag_list

    @staticmethod
    def escape(string):
        """ Escape HTML and other symbols """
        for k, v in TagOnPage.ESCAPABLE.items():
            string = string.replace(k, v)
        return string.lstrip().rstrip()

    @staticmethod
    def __get_wrappers(el):
        """
        For element get:
        list of parent tags, the name of sibling for the element, tag at siblings' level
        """
        wrappers = []
        while el.name not in TagOnPage.SIBLINGS:
            if el.name != 'a':
                wrappers.append(el.name)
            el = el.parent
        return wrappers, el.name, el

    @staticmethod
    def __next_sibling_and_val(el, sibling, wrappers):
        """ Get next sibling and its deepest value """
        # Going down
        # Base deep
        for i in range(len(wrappers)):
            el = el.find(wrappers[i])
        txt = el.get_text()
        # Additional tags in sibling
        if len(el.contents) > 1:
            txt = el.contents[0]
            while isinstance(txt, bs4.element.Tag):
                txt = txt.contents[0]
        # Going up
        for i in range(len(wrappers)):
            el = el.parent
        el = el.find_next_sibling(sibling)
        return el, TagOnPage.escape(txt)


class IncorrectMetaTypeException(Exception):
    """ Raised when user tries to set incorrect meta type to Meta-object """
    pass


class ElementNotFoundException(Exception):
    """ Raised when use of a css selector doesn't return one element """
    def __init__(self, message):
        super(ElementNotFoundException, self).__init__(message)


class NoPathException(Exception):
    """ Raised when user hasn't defined path with files """
    pass


def get_html_by_url(url):
    """ Download html from url. Raises errors when can't get html """
    res = requests.get(url)
    res.raise_for_status()
    return res.text


def track_sort(e):
    digits = '0123456789'
    num = ''
    for sym in e:
        if sym not in digits:
            break
        if sym in digits:
            num += sym
    return int(num)


def main():
    # Get config
    conf_path = "./conf.json"
    if len(sys.argv) > 1:
        conf_path = sys.argv[1]
        if not conf_path.endswith('.json'):
            conf_path += 'conf.json'
    with open(conf_path) as f:
        conf = json.loads(f.read())

    # Get tag values.
    url = conf.pop('url', None)
    path = conf.pop('path', None)
    if path is None:
        raise NoPathException
    album = conf.pop('album', None)
    artist = conf.pop('artist', None)
    song_selector = conf.pop('songs', None)
    year = conf.pop('year', None)

    # Get original files
    files = [f for f in os.listdir(path) if f.endswith('.mp3')]
    files.sort(key=track_sort)

    # Parse songs
    songs = TagOnPage('song', url, selector=song_selector).list_from_siblings
    # Make dir
    album_path = os.path.join(path, album)
    os.makedirs(album_path)

    # Copy files and set tags
    for i in range(len(files)):
        src = os.path.join(path, files[i])
        track = i + 1
        ext = os.path.splitext(src)[1]
        new_file_name = f'{track} {songs[i]}{ext}'
        dst = os.path.join(album_path, new_file_name)
        print(f'Setting {new_file_name}')
        mp3 = MP3File(shutil.copy(src, dst))
        if artist is not None:
            mp3.artist = artist
        mp3.album = album
        mp3.track = track
        mp3.song = songs[i]
        if year is not None:
            mp3.year = year
        mp3.save()


if __name__ == '__main__':
    main()
