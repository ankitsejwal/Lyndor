import os

#change this tempfolder path on every computer
temp_folder_path = "C:/Users/vipin/Videos/Lynda/temp/"
os.chdir(temp_folder_path)
path = os.getcwd()

for f in os.listdir(path):
    if not (f.endswith('.txt') or f.startswith('.')):
        f_name, f_ext = os.path.splitext(f)
        print f
        f_no = f_name[-3:]
        f_title = f_name[:-7]
        print f_no
        # new_file = '{}-{}{}'.format(f_no, f_title, f_ext)
        # print (new_file)
