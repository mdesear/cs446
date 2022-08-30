'''
Misha Desear
CS 446 PA 3

COMPARE/CONSTRAST

* Both the single level and the hierarchical file systems share the same average file size. This is 
  because all files generated are empty, therefore the average file size will always be zero. 
  
* The single level file system does not provide an average directory size as only one directory is used.
  This is the same reason why the single level file system doesn't provide a number of directories.
  On the other hand, the hierarchical file system has an average directory size of 4096 bytes. This is
  because all directories in Linux/Unix require this amount of space to be allocated for metadata. 
 
* The single level file system consistently has a smaller traversal time than the hierarchical system.
  This is because the single level file system has only one directory which must be traversed in order
  to retrieve information from all files. The hierarchical system has multiple subdirectories which 
  must be traversed in order to retrieve all relevant information, which takes up more time.

APPROXIMATING A HIERARCHICAL FILE SYSTEM

In a simple file system with a single-level architecture, we can roughly approximate paths using file
names. Since it is known that file names can be arbitrarily long, we can append "directory" names to the
name of a file (ex. the directory "/home/[username]/file.txt" could be represented in a file name as 
"home-[username]-file.txt" or with a similar convention). The root directory could then be organized by
file name. Though the files themselves aren't contained within their own subdirectories, this makes it
easier for a user to locate the files that they need.
  
'''

import os, sys, glob, time

def main():
	makeSingleRoot()
	makeHierarchicalRoot()	
	
	traversal("singleRoot")
	traversal("hierarchicalRoot")	
		
def makeSingleRoot():
	path = "singleRoot"
	os.chdir(os.getenv("HOME"))
	os.mkdir(path)
	os.chdir(path)
	for i in range (100):
		f = open("file" + str(i+1) + ".txt", "x")	
		
	os.chdir("..")
	
def makeHierarchicalRoot():
	path = "hierarchicalRoot"
	os.chdir(os.getenv("HOME"))
	os.mkdir(path)
	os.chdir(path)
	
	for i in range (10):
		if i == 0:
			newDir = "files1-10"
			os.mkdir(newDir)
			os.chdir(newDir)
			for i in range (10):
				f = open("file" + str(i+1) + ".txt", "x")
			os.chdir("..")
		else:
			newDir = "files" + str((i * 10) + 1) + "-" + str((i * 10) + 10)
			os.mkdir(newDir)
			os.chdir(newDir)
			for i in range ((i * 10), (i * 10) + 10):
				f = open("file" + str(i+1) + ".txt", "x")
			os.chdir("..")
	os.chdir("..")
	
def traversal(rootDir):
	root = os.path.join(os.getenv("HOME"), rootDir)
	os.chdir(root)
	
	startTime = time.time()
	
	directories = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
	dirSizes = [(os.stat(file_path).st_size) for file_path in directories]
	fileNames = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
	fileSizes = [(os.stat(file_path).st_size) for file_path in fileNames]
	
	singleTraversal = time.time() - startTime
	
	if (rootDir == "hierarchicalRoot"):
		for dirs in directories:
			cwd = os.path.join(root, dirs)
			os.chdir(cwd)
			fileNames.extend(f for f in os.listdir(cwd))
			os.chdir("..")
			for files in fileNames:
				try:
					fullpath = os.path.join(cwd, files)
					fileSizes.append((os.stat(fullpath).st_size))
				except:
					continue
		hierarchicalTraversal = time.time() - startTime
	
	fileNames.sort()
	
	if (rootDir == "singleRoot"):
		print ("Single Level File System")
		print ("Number of files: " + str(len(fileNames)))
		print ("Average file size: " + str(sum(fileSizes) / len(fileSizes)))
		print ("Traversal time: " + str(singleTraversal * 1000))
		
		os.chdir(root)
		singleFile = open("singleLevelFiles.txt", "w")
		for i in range(len(fileNames)):
			singleFile.write("File name: " + fileNames[i] + "\n")
			singleFile.write("File size: " + str(fileSizes[i]) + "\n")
			i += 1
		singleFile.close()
		os.chdir("..")
			
	elif (rootDir == "hierarchicalRoot"): 
		print ("\nHierarchical File System")
		print ("Number of files: " + str(len(fileNames)))
		print ("Number of directories: " + str(len(directories)))
		print ("Average file size: " + str(sum(fileSizes) / len(fileSizes)))
		print ("Average directory size: " + str(sum(dirSizes) / len(dirSizes)))
		print ("Traversal time: " + str(hierarchicalTraversal * 1000))
		
		os.chdir(root)
		hierarchicalFile = open("hierarchicalFiles.txt", "w")
		for i in range(len(dirSizes)):
			hierarchicalFile.write("Directory name: " + directories[i] + "\n")
			hierarchicalFile.write("Directory size: " + str(dirSizes[i]) + "\n")
		for i in range(len(fileSizes)):
			hierarchicalFile.write("File name: " + (fileNames[i]) + "\n")
			hierarchicalFile.write("File size: " + str(fileSizes[i]) + "\n")
		hierarchicalFile.close()
		os.chdir("..")

if __name__ == "__main__":
	main()
