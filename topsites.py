import time

import spynner
from spynner.browser import SpynnerTimeout

LIMIT = 100
RANGE = range(1, 100)

sites = []
failed = []

# create a list of URL:s to visit
with open("top-1m.csv") as f:
    for i in xrange(LIMIT):
        sites.append("http://%s" % f.readline().split(',')[1].strip())

b = spynner.Browser()

# for each URL
for count, site in enumerate(sites, start=1):
    if not count in RANGE:
        continue

    print "Fetching %s (%d of %d)" % (site, count, LIMIT)

    try:
        # visit the URL
        start = time.time()
        b.load(site, load_timeout=30)
        diff = time.time() - start
        print "Finished in %.2f s\n" % diff

    except SpynnerTimeout:
        # create a list of failing sites
        failed.append(site)
        print "Failed fetching %s due to timeout error" % site

    finally:
        # regardless of fail or success, make a niclasolofsson-request
        b.load("http://niclasolofsson.se/mupp")

b.close()

if failed:
    print "\nFailed (%d of %d)" % (len(failed), LIMIT)
    for fail in failed:
        print fail
