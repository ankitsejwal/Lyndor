---
name: Report an issue
about: Preview existing content then make changes

---

## Please follow the guide below

- You will be asked some question, please read them **carefully**
- Put an `x` into all the boxes [ ] relevant to your *issue* (like this: `[x]`)
- Use the *Preview* tab to see what your issue will actually look like

---

### Make sure you are using the *latest* version: run `git pull` to update your version from Lyndor directory

### Before submitting an *issue* make sure you have:
- [ ] At least skimmed through the [README](https://github.com/ankitsejwal/Lyndor/blob/master/README.md)

### What is the purpose of your *issue*?
- [ ] Bug report (encountered problems with Lyndor) :beetle: 
- [ ] Feature request (request for a new functionality) :point_up:
- [ ] Question :question:
- [ ] Other

---

### If the purpose of this *issue* is a *bug report*,  or you are not completely sure then provide the full terminal output as follows:
Copy the **whole** output and insert it here. It should look similar to one below (replace it with **your** log inserted between triple ```):

```
Traceback (most recent call last):
  File "/Users/pi/Projects/lyndor/run.py", line 130, in <module>
    main()
  File "/Users/pi/Projects/lyndor/run.py", line 35, in main
    schedule_download(url)
  File "/Users/pi/Projects/lyndor/run.py", line 51, in schedule_download
    download_course(url)
  File "/Users/pi/Projects/lyndor/run.py", line 78, in download_course
    course_folder_path = save.course_path(url, lynda_folder_path)
NameError: global name 'save' is not defined
```
---

### Answer questions related to your Environment which will help in reproducing the issue:

### The issue was encountered on:       :computer:
- [ ] MacOS
- [ ] Windows
- [ ] Linux

### Enter the python version you are using for download. Find your python version by typing in terminal `python -V`
- python (version) [replace (version) with your python version like: python 3.6.3]

---

### If the purpose of this *issue* is a *bug report* please provide all kinds of example URLs where you encountered issues (replace following example URLs by **yours**):
- https://www.lynda.com/Business-Software-tutorials/Time-Management-Tips-Weekly/440668-2.html
- https://www.lynda.com/jQuery-tutorials/jQuery-Creating-Plugins/364350-2.html

---

### Description of your *issue*, suggested a solution and other information

Explanation of your *issue* in arbitrary form goes here. Please make sure the description is worded well enough to be understood. Provide as much context and examples as possible.
