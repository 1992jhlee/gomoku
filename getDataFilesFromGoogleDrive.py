from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))

validation_labels = drive.CreateFile({'id':file_list[0]['id']})
validation_labels.GetContentFile('validation_labels.txt')
validation_inputs = drive.CreateFile({'id':file_list[1]['id']})
validation_inputs.GetContentFile('validation_inputs.txt')
training_labels = drive.CreateFile({'id':file_list[2]['id']})
training_labels.GetContentFile('training_labels.txt')
training_inputs = drive.CreateFile({'id':file_list[3]['id']})
training_inputs.GetContentFile('training_inputs.txt')
test_labels = drive.CreateFile({'id':file_list[4]['id']})
test_labels.GetContentFile('test_labels.txt')
test_inputs = drive.CreateFile({'id':file_list[5]['id']})
test_inputs.GetContentFile('test_inputs.txt')
