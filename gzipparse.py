import re


def mb(bytes):
    return bytes / 1024.0 ** 2.0

N = 'niclasolofsson.se'  # used as a mark between requests from different sites
L = 'Loris.local'  # hostname of my local machine

R = ur'Content-encoded entity body \(gzip\): (\d+) bytes -> (\d+) bytes'
ignore = False
gzippers = {}
total_data = 0.0
gzip_data = 0.0

with open('data.out', 'r') as f:
    for line in f:
        if line.startswith('No.'):
            line = f.next()  # skip the info-line
            # get the data from the file and store into variables
            frame, time, source, dest, http, status = line.split()[:6]
            line = f.next()  # and skip the newline before header

            if source == L:  # only get the server responses
                ignore = True
                continue

        elif len(line) == 1:  # empty row
            ignore = False

        elif ignore:
            continue

        # if we actually are in the middle of an interesting header
        else:
            if 'Content-Encoding: gzip' in line:
                gzippers[source] = True

            sizes = re.findall(R, line)
            if len(sizes) > 0:
                gzip_data += float(sizes[0][0])  # findall returns list of str-tuples...
                total_data += float(sizes[0][1])

diff = total_data - gzip_data

print "%d hosts are wise enought to use gzip" % len(gzippers)
print "Gzip used %.2f Mb and has saved Bredbandsbolaget and a couple of others %.2f Mb (%.f %%) of %.2f Mb data!" % (
            mb(gzip_data), mb(diff), (diff / total_data) * 100, mb(total_data))
