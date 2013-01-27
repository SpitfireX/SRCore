import os, shutil, zipfile

def getCodeFiles(path, filelist, recursive):
    for f in os.listdir(path):
        full = os.path.join(path, f)
        rel = full.split(code_path)[1]
        
        if f.endswith(".py"):
            filelist.append([full, rel, f])
        elif recursive:
            if os.path.isdir(full):
                getCodeFiles(full, filelist, recursive)

def prepCodeFiles(files, tempdir, string, replacement):
    output = []
    
    for i in range(len(files)):
        temp_path = os.path.join(tempdir, files[i][1].strip(os.sep))
        subdir = files[i][1].split(files[i][2])[0]
        files[i].append(subdir) #for later use in packFiles()
        subdir = subdir.strip(os.sep)
        subdir = os.path.join(tempdir, subdir)
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        
        temp_file = open(temp_path, "a")
        for line in open(files[i][0]):
            line = line.replace(string, replacement)
            temp_file.write(line)
        temp_file.close()
        
        output.append(temp_path)
        print "->",temp_path
        
    return output

def packFiles(output_path, file_paths, files):
    zip = zipfile.ZipFile(output_path, "a")
    for i in range(len(files)):
        zip.write(files[i], "user"+file_paths[i][3]+file_paths[i][2])
    zip.testzip()
    zip.close()

def cleanup(tempfiles):
    for f in tempfiles:
        os.remove(f)

def cleanupFolders(path):
    for f in os.listdir(path):
        temp = os.path.join(path, f)
        if os.path.isdir(temp):
            cleanupFolders(temp)
            os.rmdir(temp)

packer_path = os.path.dirname(__file__) #path of the directory containing packer.py
base_path = os.path.dirname(packer_path) #path of the base directory
code_path = os.path.join(base_path, "main") #path of the directory containing the user code
temp_path = os.path.join(packer_path, "res") #temporary working directory

print "Base directory:", base_path
print "Packer directory:", packer_path
print "Code directory:", code_path
print "Temporary directory:", temp_path

print "Scanning for code files..."

code_files = []

getCodeFiles(code_path, code_files, True)
print "Code files found:"
for f in code_files:
    print f

print "Preparing code files..."
code_files_prep = prepCodeFiles(code_files, temp_path, "sr_emulator", "sr")

print "Preparing packing..."
output_path = os.path.join(packer_path, "robot.zip")
shutil.copy(os.path.join(temp_path, "master.zip"), output_path)

print "Packing files..."
packFiles(output_path, code_files, code_files_prep)

print "Cleaning up temporary files.."
cleanup(code_files_prep)
cleanupFolders(temp_path)