import urllib2


def lookup(host):
    r = urllib2.urlopen('http://services.ipaddresslabs.com/iplocation/locatehostname?key=SAK3C32MU66275UV29QZ&hostname=%s' % host)
    r.readline()
    return r.read()

with open('some_hosts.txt') as f:
    with open('res2.xml', 'a') as res:
        for count, host in enumerate(f, start=1):
            print '%d \t %s' % (count, host)
            r = lookup(host)
            res.write(r + '\n')
            print r
