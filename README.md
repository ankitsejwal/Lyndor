## Lyndor #

* This software can download any [**Lynda.com**](https://www.lynda.com) course
* You will need a Lynda.com Basic, Premium or Organisation account inorder to download courses.
* On providing course url, the program will download - Course Folder, Chapters, Videos and info files, and will arrange all the videos in correct order by renaming them in a sequence.
* info.txt and CONTENT.md file is created, containing additional info about the course.
* You can download multiple courses at one time by pasting several urls in **Bulk Download.txt**

* **NOTE:** The Basic and Premium account costs about $20 and $30 USD respectively once the 30 day free trial ends, which is not much considering you are investing in your career or following your passion, thus you may get exponential returns from this investment.

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
---- 00 - Chapter A
---- 01 - Chapter B
---- 02 - Chapter C
-- 1 - Video A
-- 2 - Video B
-- 3 - Video C
-- 4 - Video D
-- 5 - Video E
-- 6 - Video F
-- 7 - Video G
```

### Usage
* Extract cookies from browser after login to Lynda.com by addon [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg) extension
* Your cookies.txt file must be downloaded in either Downloads or Desktop folder.
```bash
# open terminal or commandline
$ cd path/to/lyndor-folder
$ python run.py
```
* **Windows** users can simply double click **Run-Lyndor.bat** to run the program. Run-Lyndor.bat file should be located in (Lynda) folder where all courses are downloaded.
```
# Linux and MacOS users can add Lynda keyword as alias to launch the program by just typing Lynda in terminal.
$ alias lynda='python2.7 /path-to/lyndor/run.py'
```
* [**How to create alias?**](https://www.moncefbelyamani.com/create-aliases-in-bash-profile-to-assign-shortcuts-for-common-terminal-commands/)

* The program will ask now for URL, just paste a course url in the Terminal/CMD - and the download should begin.

### Reporting Issues
* Each release of the program is well tested on MacOS, feedback and bug reporting for Windows and Linux operating system is needed and will be greatly appreciated.