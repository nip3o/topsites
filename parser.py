from lxml import objectify
from collections import defaultdict

N = 'niclasolofsson.se'
L = 'Loris.local'

LIMIT = 100
sites = []


class Site():
    def __init__(self, name):
        self.name = name
        self.owner = ''
        self.servers = set()

    def print_heading(self):
        print '=================================='
        print '           %s' % self.name
        print '=================================='


class GeoInfo():
    def __init__(self):
        self.name = ''
        self.long = 0.0
        self.lat = 0.0
        self.organization = ''

    def fill(self, name, longitude, lat, org):
        if org == '-':
            org = None

        self.name = name
        self.long = longitude
        self.lat = lat
        self.organization = org

    def __repr__(self):
        return u'%s - (%s) %.2f, %.2f' % (self.name, self.organization, self.lat, self.long)


hosts = defaultdict(GeoInfo)

with open('res.xml') as f:
    xml = objectify.parse(f)

for r in xml.getroot().getchildren():
    host = unicode(r.host_name)

    if not hasattr(r, 'geolocation_data'):
        print host
        print 'has not geo'
    else:
        hosts[host].fill(name=host,
                         longitude=float(r.geolocation_data.longitude),
                         lat=float(r.geolocation_data.latitude),
                         org=unicode(r.geolocation_data.organization))

print 'Finished parsing geo-data'


with open("top-1m.csv") as f:
    for i in xrange(LIMIT):
        sites.append(Site(f.readline().split(',')[1].strip()))

i = 0
site = sites[i]
site.print_heading()

new = True

with open('wireshark.out') as f:
    for line in f:
        _, _, source, dest, http, status = line.split()[:6]

        if not dest == N and not source == N and not dest == L:
            site.servers.add(dest)

        if source == N:
            i += 1
            site = sites[i]
            site.print_heading()
            new = True

servers = set()
for site in sites:
    servers = servers.union(site.servers)

    if not site.name in hosts:
        print site.name

for s in servers:
    print '%s,%s' % (hosts[s].lat, hosts[s].long)
