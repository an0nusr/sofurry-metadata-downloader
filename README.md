# SoFurry Author Metadata Downloader
A tool to download info about an an author's works on SoFurry.

Have you ever wanted to find a specific story from an author on
SoFurry, but had trouble locating it? SoFurry search doesn't allow
you to search by author - your only option is to page through all
of their work (in all of their folders) to try to find it.

That's what this tool solves - just run the tool on your favorite 
author and it will dump all the *metadata* for their stories (such
as titles, descriptions, tags, and links to the actual work)! 

## Usage
You'll need Python (>3.7) to run this tool, along with some additional
dependencies. You can install all the required libraries by running
`pip install -r requirements.txt` from this directory.

You'll also likely want to provide the tool with your SoFurry cookies so it can
see adult works. There are extensions like
[Ganbo for Firefox](https://addons.mozilla.org/en-US/firefox/addon/ganbo/) and
[Get Cookies.txt for Chrome](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid?hl=en)
that will export your SoFurry cookies to a `cookies.txt` file.

Once you're ready, you can run the tool like this:
```bash
python sf-userstories-dl.py -c cookies.txt -o stories.json USERNAME
```

Just replace `USERNAME` with your preferred author and you're good to go!

The output will be a JSON file you can easily read and search with a text editor (or jq).