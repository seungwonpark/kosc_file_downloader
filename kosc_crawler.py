# Multithreaded downloading : http://stackoverflow.com/questions/24216760/multithreaded-file-download-in-python-and-updating-in-shell-with-download-progre

import urllib2
import os
import sys
import time
import threading

urls = [
"http://222.236.46.45/nfsdb/COMS/GOCI/1.0/2011/04/01/L1B/COMS_GOCI_L1B_GA_20110401001641.he5.zip",
"http://222.236.46.45/nfsdb/COMS/GOCI/1.0/2011/04/01/L1B/COMS_GOCI_L1B_GA_20110401011641.he5.zip",
"http://222.236.46.45/nfsdb/COMS/GOCI/1.0/2011/04/01/L1B/COMS_GOCI_L1B_GA_20110401021641.he5.zip",
"http://222.236.46.45/nfsdb/COMS/GOCI/1.0/2011/04/01/L1B/COMS_GOCI_L1B_GA_20110401031641.he5.zip",
"http://222.236.46.45/nfsdb/COMS/GOCI/1.0/2011/04/01/L1B/COMS_GOCI_L1B_GA_20110401041641.he5.zip",
"http://222.236.46.45/nfsdb/COMS/GOCI/1.0/2011/04/01/L1B/COMS_GOCI_L1B_GA_20110401051641.he5.zip",
"http://222.236.46.45/nfsdb/COMS/GOCI/1.0/2011/04/01/L1B/COMS_GOCI_L1B_GA_20110401061641.he5.zip",
"http://222.236.46.45/nfsdb/COMS/GOCI/1.0/2011/04/01/L1B/COMS_GOCI_L1B_GA_20110401071641.he5.zip",
]

url = urls[1]

def downloadFile(url, saveTo=None):
    file_name = url.split('/')[-1]
    if not saveTo:
        saveTo = 'test/'
    try:
        u = urllib2.urlopen(url)
    except urllib2.URLError , er:
        print("%s" % er.reason)
    else:

        f = open(os.path.join(saveTo, file_name), 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            sys.stdout.write('%s\r' % status)
            time.sleep(.2)
            sys.stdout.flush()
            if file_size_dl == file_size:
                print r"Download Completed %s%% for file %s, saved to %s" % (file_size_dl * 100. / file_size, file_name, saveTo,)
        f.close()
        return


def synchronusDownload():
    urls_saveTo = {urls[0]: None, urls[1]: None, urls[2]: None}
    for url, saveTo in urls_saveTo.iteritems():
        th = threading.Thread(target=downloadFile, args=(url, saveTo), name="%s_Download_Thread" % os.path.basename(url))
        th.start()

synchronusDownload()
