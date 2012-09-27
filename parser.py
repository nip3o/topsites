from lxml import objectify
from collections import defaultdict

N = 'niclasolofsson.se'
L = 'Loris.local'

LIMIT = 100
sites = []

total_hosts = 0
cheats_with_other_servers = 0
helps_google_rule_the_world = 0


class Site():
    def __init__(self, name):
        self.name = name
        self.servers = set()


class ServerInfo():
    def __init__(self):
        self.name = ''
        self.long = 0.0
        self.lat = 0.0
        self.organization = ''
        self.ip = ''
        self.country = ''

    def fill(self, name, longitude, lat, org, ip, country):
        if org == '-':
            org = name

        self.name = name
        self.long = longitude
        self.lat = lat
        self.organization = org
        self.ip = ip
        self.country = country

    def __repr__(self):
        return u'%s - (%s) %.2f, %.2f' % (self.name, self.organization, self.lat, self.long)


hosts = defaultdict(ServerInfo)

with open('res.xml') as f:
    xml = objectify.parse(f)

for r in xml.getroot().getchildren():
    host = unicode(r.host_name)

    if hasattr(r, 'geolocation_data'):
        hosts[host].fill(name=host,
                         longitude=float(r.geolocation_data.longitude),
                         lat=float(r.geolocation_data.latitude),
                         org=unicode(r.geolocation_data.organization),
                         ip=unicode(r.resolved_ip_address),
                         country=unicode(r.geolocation_data.country_name))


with open("top-1m.csv") as f:
    for i in xrange(LIMIT):
        sites.append(Site(f.readline().split(',')[1].strip()))

i = 0
site = sites[i]
#site.print_heading()

with open('wireshark.out', 'r') as f:
    for line in f:
        _, _, source, dest, http, status = line.split()[:6]

        if not dest == N and not source == N and not dest == L:
            site.servers.add(dest)

        if source == N:
            i += 1
            site = sites[i]
            #site.print_heading()

servers = set()
cheaters = set()
for site in sites:
    servers = servers.union(site.servers)

    googleified = False
    for server in site.servers:
        total_hosts += 1

        if hosts[site.name].organization != hosts[server].organization:
            cheaters.add(server)

        if hosts[server].organization == 'Google' and not googleified:
            helps_google_rule_the_world += 1
            googleified = True
            print site.name

ips = set()
countries = defaultdict(list)
real_servers = []

for server in servers:
    if not hosts[server].ip in ips:
        real_servers.append(server)
        ips.add(hosts[server].ip)
        countries[hosts[server].country].append(server)

for c in countries:
    print "%s %d" % (c, len(countries[c]))

print """
So, the truth is that %d unique servers was contacted. Total %d unique hostnames.
%d of all servers is operated by other company than the site.
%d sites out of 100 helps google rule the world.""" % (len(real_servers), len(servers),
    len(cheaters), helps_google_rule_the_world)
