# Lyndor

[![Build Status](https://travis-ci.org/ankitsejwal/Lyndor.svg?branch=master)](https://travis-ci.org/ankitsejwal/Lyndor)

* This software can download any [**Lynda.com**](https://www.lynda.com) course
* You will need a Lynda.com Basic, Premium or Organisation account inorder to download courses.
* On providing course url, the program will download - Course Folder, Chapters, Videos, Subtitles and Info files, and will arrange all the videos in correct order by renaming them in a sequence.
* info.txt and CONTENT.md file is created, containing additional info about the course.
* You can download multiple courses at one time by pasting several urls in **Bulk Download.txt**

* **NOTE:** The Basic and Premium account costs about $20 and $30 USD respectively once the 30 day free trial ends, which is not much considering you are investing in your career or following your passion, thus you may get exponential returns.

```
  Features:

- Bulk download                         - Creates Course & Chapter folders
- Subtitles download                    - Videos and subtitles renaming
- Username + Password combination       - Adjust preferences (settings.json)
- cookies.txt(Organizational login)     - Info files for each course
- Schedule download time                - Cross platform support
- Runs on both python2 and python3      - aria2 downloader(for faster downloads)
```

```python
#supports multiple platforms :)
def Operating_Systems():
    Windows = true
    MacOS   = true
    Linux   = true

    if Windows or MacOs or Linux:
        print 'Have fun!!!'
```

### Requirements

* **Python 2 or Python 3**
* Python is free and comes pre-installed in MacOS and most Linux distributions, Windows users can install python from official [**python**](https://www.python.org/download/releases/2.7/) website
* **NOTE:** Windows users must add python.exe to path

![**Windows installer**](https://www.howtogeek.com/wp-content/uploads/2017/05/ximg_591a09e55df0e.png.pagespeed.gp+jp+jw+pj+ws+js+rj+rp+rw+ri+cp+md.ic.Sy31NTwaIO.png)

### Install
```bash
   $ cd path/to/lyndor
   $ python install.py
   # Apart from many other processes, install.py creates a Lynda folder inside your Videos or Movies folder
   # all the courses will be downloaded to Lynda folder
   # to change path later, paste your desired path into settings.json
```
Note: **Windows** users can simply double click **install.bat** file to run install.py file alternatively.

### Lynda Folder Structure
```
- Lynda Folder          (Here goes all your downloaded courses)
---- Course1
---- Course2
---- Course3
---- Course4
-- Bulk Download.txt    (Paste multiple urls for bulk download)
-- Run-Lyndor.bat       (For windows user only, double click to launch program)
```

### Course Folder Structure
```
- Course1 Folder
---- CONTENT.md
---- info.txt
---- 00 - Chapter A     // chapter folder
---- 01 - Chapter B     // ...
---- 02 - Chapter C
-- 1 - Video A          // video file
-- 2 - Video B          // video file
-- 3 - Video C          // ...
-- 1 - Video A.srt      // subtitle file
-- 2 - Video B.srt      // subtitle file
-- 3 - Video C.srt      // ...
```

### Lyndor Folder Structure
```
- Lyndor Folder
---- LICENSE
---- settings.json      (edit settings here)
-- run.py               (main file - execute the file, to run the program)
-- chapters.py
-- download.py
-- ...
-- ...
-- ...
-- install.py
```

### Usage

* Lynda course can be downloaded in two ways, either with username + password combination or with cookies.txt file
* Add your username and password to settings.json and set ["use_cookie_for_download": false]
* For organization login - use cookie method, set ["use_cookie_for_download": true] in settings.json

```javascript
// settings.json - File

{
    "credentials": {
        "username": "",                         // username and password combination will 
        "password": "",                         // only work when "use_cookie_for_download": false
        "use_cookie_for_download": true         // if false, username + password will be used instead
    },
    "requirements": {
        "dependencies": ["youtube-dl", "lxml", "beautifulsoup4", "colorama"]
    },
    "preferences": {
        "download_subtitles": true,
        "ext-downloader-aria2-installed": false, // set true after installing aria2 (faster downloads)
        "location": "/path/to/folder/Lynda",
        "download_time": ""                      // set time to schedule download (ex: "01:00" for 1am)
    }
}
```

#### To run the program:

```bash
# open terminal or commandline
$ python path/to/lyndor-folder/run.py
```
* **Windows** users can simply double click **Run-Lyndor.bat** to run the program. Run-Lyndor.bat file should be located in (Lynda) folder where all courses are downloaded.
```
# Linux and MacOS users can add Lynda keyword as alias to launch the program by just typing Lynda in terminal.
$ alias lynda='python2.7 /path-to/lyndor/run.py'
```
* [**How to create alias?**](https://www.moncefbelyamani.com/create-aliases-in-bash-profile-to-assign-shortcuts-for-common-terminal-commands/)

* The program will ask now for URL, just paste a course url in the Terminal/CMD - and the download should begin.

#### If you wish to download via cookies (Recommended for Organizational login):
* Extract cookies from browser after login to Lynda.com by addon [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg) extension
* Your cookies.txt file must be downloaded in either Downloads or Desktop folder.

### Reporting Issues
* Each release of the program is well tested on MacOS, feedback and bug reporting for Windows and Linux operating system is needed and will be greatly appreciated.

### Requesting Features
* New features are being requested constantly, you are encouraged to ask for a new feature from the Issues tab <img src="https://assets-cdn.github.com/favicon.ico" alt="octocat icon" width="18">