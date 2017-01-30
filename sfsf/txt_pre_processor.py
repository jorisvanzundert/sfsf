import fileinput
import re

class TxtPreProcessor:

    def transform( self, text ):
        # remove likely page numbers
        return re.sub( '\[\d+\]', '', text )

# Main
if __name__ == '__main__':
    pre_processor = TxtPreProcessor()
    for line in fileinput.input():
        line = pre_processor.transform( line )
        print( line )
