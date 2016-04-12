# -*- coding: utf-8 -*-
#author RogerPuX
import os
import shutil
import sys

segment = sys.argv[1]

source_ini_file_path = r'C:\Users\RogerPuX\AppData\Roaming\VanDyke\Config\Sessions\自动生成V2\10.21.2.22.ini'
dest_ini_path = r'C:\Users\RogerPuX\AppData\Roaming\VanDyke\Config\Sessions\自动生成V2\python-create'

source_vbs_file_path = r'C:\Users\RogerPuX\AppData\Roaming\VanDyke\Config\Sessions\自动生成V2\scripts\10.21.2.22.vbs'
dest_vbs_path = r'C:\Users\RogerPuX\AppData\Roaming\VanDyke\Config\Sessions\自动生成V2\python-create\vbs'

def copy_and_replace(source_file,ip,dest_path,dest_file_name_suffix):

	##copy opration
	source_file_unicode = unicode(source_file,'utf8')
	dest_path_unicode = unicode(dest_path,'utf8')
	dest_file_name = dest_path_unicode + '\\new' + ip + dest_file_name_suffix

	shutil.copyfile(source_file_unicode, dest_file_name)

	##replace opration
	dest_file_name_replaced = dest_path_unicode + '\\' + ip + dest_file_name_suffix
	#print dest_file_name_replaced

	fp1 = open(dest_file_name,'r')
	fp2 = open(dest_file_name_replaced,'w')
	for s in fp1.readlines():
		if dest_file_name_suffix == '.vbs':
			fp2.write(s.replace('10.21.2.22',ip))
		else:
			replace_string = 'python-create\\vbs\\' + bytes(ip)
			fp2.write(s.replace(r'scripts\10.21.2.22',replace_string))
	fp1.close()
	fp2.close()

	if os.path.exists(dest_file_name):
		os.remove(dest_file_name)

for i in range(100,180):
	ip = segment + '.' + bytes(i)
	copy_and_replace(source_ini_file_path,ip,dest_ini_path,'.ini')
	copy_and_replace(source_vbs_file_path,ip,dest_vbs_path,'.vbs')

print "Don't Panic"
	


	

