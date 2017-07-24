## Lyndor #

* This software can download any [**Lynda.com**](https://www.lynda.com) course
* You will need a Lynda.com Standard or Organisation account inorder to download courses.
* On providing course url, the program will download - Course Folder, Chapters and Videos, sometimes there over 100 videos and arranging them takes time, to solve the issue, the program grabs each video and renames it to arrange all videos in correct order.
* info.txt file is created, containing additional info about the course.
* You can download multiple courses at one time.

### Platforms

* Windows
* MacOS
* Linux

### Requirements

* **Python 2.7**
* Python is free and comes pre-installed in MacOS, Windows users can install python from official [**python**](https://www.python.org/download/releases/2.7/) website
* **NOTE:** Windows users must add python.exe to path 

![**Windows installer**](https://www.howtogeek.com/wp-content/uploads/2017/05/ximg_591a09e55df0e.png.pagespeed.gp+jp+jw+pj+ws+js+rj+rp+rw+ri+cp+md.ic.Sy31NTwaIO.png)

### Install
```bash
   $ cd path/to/lyndor
   $ python install.py
   # Apart from many other processes, install.py creates a Lynda folder inside your Videos or Movies folder
   # all the courses will be downloaded to this (Lynda) folder
   # to change path later, paste your desired path into location.txt
```
Note: **Windows** users can simply double click **install.bat** file to run install.py file alternatively.

### Folder Structure
```
- Course Folder
---- info.txt
---- 0 - Chapter A
-------- 1 - Video A
-------- 2 - Video B
-------- 3 - Video C
---- 1 - Chapter B
-------- 1 - Video A
-------- 2 - Video B
-------- 3 - Video C
-------- 1 - Video D
---- 2 - Chapter C
```

### Usage
* Extract cookies from browser after login to Lynda.com by addon [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg) extension
* Your cookies.txt file must be present in either Downloads or Desktop folder.
```bash
# open terminal or commandline
$ cd path/to/lyndor-folder
$ python run.py
```
* **Windows** users can simply double click **Lynda.bat** to run the program. Lynda.bat file should be located in (Lynda) folder where all courses are downloaded.
```
# Linux and MacOS users can add Lynda keyword as alias
# to launch the program by just typing Lynda in terminal.
$ alias lynda='python2.7/path-to/lyndor/run.py'
```
* [**How to create alias?**](https://www.moncefbelyamani.com/create-aliases-in-bash-profile-to-assign-shortcuts-for-common-terminal-commands/)

* The program will ask now for URL, just paste a course url in the Terminal/CMD - and the download should begin.