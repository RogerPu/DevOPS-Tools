# -*- coding: utf-8 -*-
import os
import shutil
import re


source_ini_file_path = r'C:\Users\RogerPuX\AppData\Roaming\VanDyke\Config\Sessions\自动生成V2\10.21.2.22.ini'
dest_path = r'C:\Users\RogerPuX\AppData\Roaming\VanDyke\Config\Sessions\自动生成V2\python-create'

#print dest_path

segment = '192.168.136'

source_ini_file_unicode = unicode(source_ini_file_path, 'utf8')


#print source_ini_file_unicode


dest_path_unicode = unicode(dest_path,'utf8')
dest_file = dest_path_unicode + '\\' + r'192.168.154.139.ini'


#dest_file_unicode = unicode(dest_file,'utf8')

print dest_file


shutil.copyfile(source_ini_file_unicode,dest_file)
	

