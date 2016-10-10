import sys, getopt
import os.path
import epub
from bs4 import BeautifulSoup

ifile = ''
ofile = ''

try:
    myopts, args = getopt.getopt(sys.argv[1:], "i:o:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -i epub_file_in -o txt_file_out" % sys.argv[0])
    sys.exit(2)

for o, a in myopts:
    if o == '-i':
        ifile = a
    elif o == '-o':
        ofile = a

if os.path.isfile(ifile):
    book = epub.open_epub(ifile)
    print(ifile)
    for item in book.opf.manifest.values():
        # read the content
        data = book.read_item(item)

        # create initial file
        try:
            os.remove(ifile)
        except OSError:
            pass

        # append the blocks of text to the output file
        if 'xhtml' in item.href:
            soup = BeautifulSoup(data, "lxml")
            raw_text = soup.get_text()
            print item.href, raw_text.encode('utf-8')
            with open(ofile, "a") as f:
                f.write(raw_text.encode('utf-8'))






