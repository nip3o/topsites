from lxml import objectify
from collections import defaultdict

N = 'niclasolofsson.se'  # used as a mark between requests from different sites
L = 'Loris.local'  # hostname of my local machine

LIMIT = 100
total_hosts = 0


class Site():
    """
    A container for storing which hosts are contaced from which site
    """
    def __init__(self, name):
        self.name = name
        self.servers = set()


class ServerInfo():
    """
    Contains geographic info about a host
    """
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


hosts = defaultdict(ServerInfo)

with open('res.xml') as f:
    xml = objectify.parse(f)

# for each result of the Geo-lookup
for r in xml.getroot().getchildren():
    host = unicode(r.host_name)
    # if result was successful
    if hasattr(r, 'geolocation_data'):
        # store info for the host
        hosts[host].fill(name=host,
                         longitude=float(r.geolocation_data.longitude),
                         lat=float(r.geolocation_data.latitude),
                         org=unicode(r.geolocation_data.organization),
                         ip=unicode(r.resolved_ip_address),
                         country=unicode(r.geolocation_data.country_name))

sites = []

# read the LIMIT most popular sites into a list
with open("top-1m.csv") as f:
    for i in xrange(LIMIT):
        sites.append(Site(f.readline().split(',')[1].strip()))

i = 0
site = sites[i]
#site.print_heading()

with open('wireshark.out', 'r') as f:
    for line in f:
        # get the data from the file and store into variables
        _, _, source, dest, http, status = line.split()[:6]

        # skip all niclasolofsson-requests and all responses to local host
        if not dest == N and not source == N and not dest == L:
            site.servers.add(dest)

        # continue to next site if a niclasolofsson-request is found
        if source == N:
            i += 1
            site = sites[i]

servers = set()
cheaters = set()
helps_google_rule_the_world = []

for site in sites:
    #  save all unique servers in a new variable, thus removing duplicates
    servers = servers.union(site.servers)

    googleified = False
    for server in site.servers:
        total_hosts += 1

        # if owner of site differs from owner of server, add it to list of 3rd party serves
        if hosts[site.name].organization != hosts[server].organization:
            cheaters.add(server)

        # if server is owned by Google and the site hasn't already been
        if hosts[server].organization == 'Google' and not googleified:
            helps_google_rule_the_world.append(site)
            googleified = True

ips = set()
countries = defaultdict(list)
real_servers = []

for server in servers:
    # for each host which has a unique IP
    if not hosts[server].ip in ips:
        # add to a spearate list
        real_servers.append(server)
        ips.add(hosts[server].ip)
        # and create country statistics
        countries[hosts[server].country].append(server)

print """
Total %d contacted hosts. %d unique ip-addresses was contacted. %d unique hostnames.
%d of all servers is operated by other company than the site.
%d sites out of 100 helps google rule the world.""" % (total_hosts, len(real_servers), len(servers),
    len(cheaters), len(helps_google_rule_the_world))


#for h in hosts:
    #print "%s,%s" % (hosts[h].lat, hosts[h].long)

#for c in sorted(countries):
#    print "%s\t&\t%d \\\\ \hline" % (c, len(countries[c]))
