#script per testare l'import module via url di python:
#!/usr/bin/python
import urllib, sys
def import_URL(URL):
    exec urllib.urlopen(URL).read() in globals()

"""
from urllib2 import urlopen
r = urlopen('http://urlHere/fileHere')  
f = open('filenameToWrite', 'w')
f.write(r.read())
f.close()
import filenameWithout.PyInIt  
"""
def import_path(fullpath):
    """ 
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do. 
    """
    import os,sys
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) # Might be out of date
    del sys.path[-1]
    return module

#import_path("/var/www/Kickstart/boot/python/mount.py")
#module.list_media_devices
#sys.path.append(/var/www/Kickstart/boot/python/)

sys.path.append("/root/scripts/util/")
#to add later
#sys.path.insert(0, "/var/www/Kickstart/boot/python/")
#print(sys.path)
import mount

#return list of block devices
listdevices = mount.list_media_devices()
print(len(listdevices))
if (len(listdevices) > 0):
    for device in listdevices:
        print(device.device)
        print(device.drive)
        print(device.mounted)
        print(device.size)
        print(device.model)
        print(device.vendor)



#prova = Device(test)

#print(prova)
print ["hello word"]
