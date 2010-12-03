#!/usr/bin/env python

import sys
import os

if len(sys.argv) < 3:
    sys.exit('Usage: backup_sqlite.py [bucket name with path]' +  
             ' [destination path] \n')

def backup(sqlite_path, srcdir, destdir, fn):
    os.system(sqlite_path + ' ' + os.path.join(srcdir, fn) + 
              " '.backup " +  os.path.join(destdir, fn) + " ' ")
    print "Backup of %s done" % fn
    os.system(sqlite_path + ' ' + os.path.join(destdir, fn) +  ' vacuum')
    print "Vacuum of %s done" % fn

def find_sqlite():
    candidates = ['/opt/membase/bin/ep_engine/management/sqlite3',
                  r'c:\Program Files\Membase\Server\bin\ep_engine\management\sqlite3']
    for c in candidates:
        if os.path.exists(c):
            return c
    sys.exit("ERROR:  Cannot find sqlite3 command.")

src_path, dest_path = sys.argv[1:]
sqlite_path = find_sqlite()

for n,p in [('src', src_path), ('dest', dest_path)]:
    if not os.path.exists(p):
        sys.exit("ERROR:  %s does not exist at %s" % (n, p))

dirname, bucket_name = os.path.split(src_path)

backup(sqlite_path, dirname, dest_path, bucket_name)
for i in range(4):
    backup(sqlite_path, dirname, dest_path, '%s-%d.sqlite' % (bucket_name, i))

