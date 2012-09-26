#from collections import defaultdict
#import urllib2
import time

import spynner
from spynner.browser import SpynnerTimeout

LIMIT = 100
RANGE = range(1, 100)

#sites = defaultdict(dict)
sites = []
failed = []

with open("top-1m.csv") as f:
    for i in xrange(LIMIT):
        sites.append("http://%s" % f.readline().split(',')[1].strip())

b = spynner.Browser()

for site in enumerate(sites, start=1):
    count, site = site
    if not count in RANGE:
        continue

    print "Fetching %s (%d of %d)" % (site, count, LIMIT)

    if not count % 20:
        print "Recreating spynner browser object"
        b.close()
        b = spynner.Browser()

    try:
        if count == 49:
            raise SpynnerTimeout

        start = time.time()
        b.load(site, load_timeout=30)
        diff = time.time() - start
        print "Finished in %.2f s\n" % diff

    except SpynnerTimeout:
        failed.append(site)
        print "Failed fetching %s due to timeout error" % site

    finally:
        b.load("http://niclasolofsson.se/mupp")

b.close()

if failed:
    print "\nFailed (%d of %d)" % (len(failed), LIMIT)
    for fail in failed:
        print fail

#b.show()
#raw_input()

#www = urllib2.urlopen(site)
#for line in www:
#    print line
