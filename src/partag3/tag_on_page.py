import bs4

from src.partag3.meta import Meta
from src.partag3.utils import load_html


class TagOnPage(Meta):
    SIBLINGS = ['tr', 'li']
    ESCAPABLE = {
        u'\xa0': u'',
        u'\n': u'',
    }

    def __init__(self, meta_type, url, selector=None, value=None):
        super(TagOnPage, self).__init__(meta_type, value)
        self.url = url
        self.selector = selector

        self.__el = None  # Proxy bs4 element for parsing of lists

    def compile(self) -> 'TagOnPage':
        """ Set value attribute. """

        html = load_html(self.url)
        soup = bs4.BeautifulSoup(html, features='html.parser')
        print(f'Parsing {self.meta_type}...')
        try:
            el = soup.select(self.selector)[0]
        except IndexError:
            raise IndexError(f'{self.meta_type} has not been found')
        self.value = TagOnPage.escape(el.get_text())
        self.__el = el  # proxy for list

        return self

    @property
    def list_from_siblings(self):
        """
        Get list of values similar to the value pointed by the CSS-selector.
        The method uses only allowed siblings (TagOnPage::SIBLINGS).
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
    def escape(string: str) -> str:
        """ Escape HTML and/or other symbols """
        for k, v in TagOnPage.ESCAPABLE.items():
            string = string.replace(k, v)
        return string.lstrip().rstrip()

    @staticmethod
    def __get_wrappers(el):
        """
        For element get:
        1. list of parent tags;
        2. the name of sibling for the element;
        3. tag at the siblings level.
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
