import os, json
# read preferences file

real_path = os.path.realpath(__file__)
LYNDOR_PATH = real_path[:real_path.find('read.py')]

def bulk_download():
    ''' Read Bulk Download.txt '''
    os.chdir(settings_json('preferences', 'location'))
    bulk_download = open('Bulk Download.txt', 'r')
    urls = bulk_download.readlines()
    return urls

def settings_json(section, key):
    ''' Read settings.json '''
    os.chdir(LYNDOR_PATH)

    in_file = open('settings.json', 'r')
    data = json.load(in_file)
    in_file.close()
    return data[section][key]

