# Microsoft Download URL Extractor
Retrieve download links from Microsoft downloads

## This script cannot 
- ❌ Retrieve links of contents which Microsoft removed from downloads site
- ⚠️ Ensure the download URL given is still available
- ❌ Activate any paid softwares
- ❌ Bypass the limitation of evaluation

## Implantations
Currently this project have 2 implantations.
### Python

Download the script and install the dependency
```
pip install requests
```
Follow the usage
```
Usage:
  ./msdl.py [--lang LANGUAGES] --getlang id
  ./msdl.py --lang LANGUAGES --getlink id

Options:
  --help          Show this help message and exit
  --getlang       Retrieve all available languages
  --getlink       Retrieve download link(s) starting with https://download.microsoft.com/
  --lang          Specify language(s) (Required for --getlink, Troubleshooting-only for --getlang)

Examples:
  ./msdl.py --getlang 12345
  ./msdl.py --lang en-us --getlink 12345
  ./msdl.py --lang "en-us,zh-cn" --getlink 12345
```

### Tampermonkey
GreasyFork: [https://greasyfork.org/scripts/534090-microsoft-download-url-extractor](https://greasyfork.org/scripts/534090-microsoft-download-url-extractor)

Install: [https://update.greasyfork.org/scripts/534090/Microsoft%20Download%20URL%20Extractor.user.js](https://update.greasyfork.org/scripts/534090/Microsoft%20Download%20URL%20Extractor.user.js)
