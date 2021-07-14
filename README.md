# Partag3

A utility to massively update mp3-tags by parsing them from html.

## How to use

1. As library

Use the `TagOnPage` class to parse sibling songs.

```python
from src.partag3.tag_on_page import TagOnPage

# parse 'songs' from 'url' using the 'css-selector'
parser = TagOnPage('song', 'http://url.com', selector='.css-selector')
songs = parser.list_from_siblings  # type: List[str]
```

2. As script

> Install dependencies: `pip3 install -r requirements.txt`

You have to run the `main.py` pointing to your `conf.json` file. There are two options to do that:

* Create "conf.json" in the current directory;
* Pass an argument with the "conf.json" path to the script, just like that

```
python3 main.py ../some/dirs/
```

It´s going to search for "conf.json" in the "...dirs/" directory  
You can specify path to another json file like that

```
python3 main.py ../some/dirs/my_album_conf.json
```

### JSON keys and values

The JSON file must contain following keys:

- "album": album tag. It is used as directory name for resulting files;
- "songs": CSS selector to the first element of list with songs;
- "url": address of the page that contains the CSS selector.

It may not necessarily contain keys:

- "path": path to the directory with original mp3 files. Basically the current directory is used;
- "year": year tag;
- "artist": artist tag.

**All values in the JSON are string literals!**

### JSON example

```
{
    "url": "https://some_address",
	"album": "My new favourite album",
	"songs": "#mw-content-text > div > table:nth-child(15) ... > i",

	"path": "directory_with_original_files/",
	"artist": "Some artist",
	"year": "2019"
}
```
