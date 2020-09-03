# YtBot
Downloads raw audio and video from YouTube, using the [pytube](https://github.com/get-pytube/pytube3) package.

**Important**: This module heavily depends on the pytube module, so check the pytube project page for regular updates.

### Installation
To install this module and its dependencies, run the following commands in your terminal.

```
python -m pip install -r requirements.txt
python -m pip install -e 
```

### Usage
To download a set of videos, create a ``.txt`` file containing the URLs, separated by a new line. Then, you can call the download script from your terminal like so.

```
python ./download.py --target_dir /path/to/save/directory --urls /path/to/text/file --download
```

### Contributing
If you wish to contribute code fork this repo and write your code in a contrib folder, and then make a pull request.

### Bug Reporting
If you encounter any bugs please raise a GitHub issue.