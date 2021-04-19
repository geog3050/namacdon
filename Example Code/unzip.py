import zipfile
import os

files = "C:/Users/Neal/OneDrive - University of Iowa/Derecho Damage Project/EO Data/EVWHS"
extension = ".zip"

os.chdir(files)

for file in os.listdir(files):
    if file.endswith(extension):
        file_name = os.path.abspath(file)
        zip_ref = zipfile.ZipFile(file_name)
        zip_ref.extractall(files)
        zip_ref.close()
