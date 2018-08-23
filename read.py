import os, json

real_path = os.path.realpath(__file__)
LYNDOR_PATH = real_path[:real_path.find('read.py')]

def bulk_download():
    ''' Read Bulk Download.txt '''
    os.chdir(settings_json('preferences', 'location'))
    bulk_download = open('Bulk Download.txt', 'r')
    urls = bulk_download.readlines()
    return urls

def settings_json(section, *args):
    ''' Read settings.json '''
    os.chdir(LYNDOR_PATH)

    in_file = open('./settings/static/js/settings.json', 'r')
    data = json.load(in_file)
    in_file.close()
    try:
        return data[section][args[0]][args[1]]
    except:
        return data[section][args[0]]

try:
    # read credentials
    username                = settings_json('credentials', 'regular_login', 'username')
    password                = settings_json('credentials', 'regular_login', 'password')
    card_number             = settings_json('credentials', 'library_login', 'card_number')
    card_pin                = settings_json('credentials', 'library_login', 'card_pin')
    organization_url        = settings_json('credentials', 'library_login', 'organization_url')
    course_download_pref    = settings_json('credentials', 'course_download_pref')
    exfile_download_pref    = settings_json('credentials', 'exfile_download_pref')
    # read preferences
    location                = settings_json('preferences', 'location')
    exfile_download_method  = settings_json('preferences', 'exfile_download_method')
    download_subtitles      = settings_json('preferences', 'download_subtitles')
    download_exercise_file  = settings_json('preferences', 'download_exercise_file')
    web_browser_for_exfile  = settings_json('preferences', 'web_browser_for_exfile')
    external_downloader     = settings_json('preferences', 'aria2_installed')
    download_time           = settings_json('preferences', 'download_time')
    redownload_course       = settings_json('preferences', 'redownload_course')
except Exception as e:
    print(e)