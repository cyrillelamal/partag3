# Partag3
A utility to massively update mp3 tags with parsing of songs from html


## Getting started
Get core file `partag3.py` or its code and install required modules, e.g. using pip and requirements file
```
pip install -r requirements.txt
```

You have to run the script passing to it `conf.json` file. There are two options to do it:
* Create "conf.json" in the current directory;
* Pass an argument with "conf.json" path to the script, just like that
```
python3 partag3 ../some/dirs/
```
It will be searching for "conf.json" in the "...dirs/" directory  
You can specify path to another .json like that
```
python3 partag3 ../some/dirs/my_album_conf.json
```
### JSON keys and values
The JSON must contain keys:  
- "album": album tag. It is used as directory name for resulting files;
- "songs": CSS selector to the first element of list with songs;
- "url": address of the page that contanins the CSS selector.  

It may not necessarily contain keys:
- "path": path to the directory with original mp3 files. Basically the current directory is used;
- "year": year tag;
- "artist": artist tag;  

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
