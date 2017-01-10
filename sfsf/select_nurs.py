import xlrd
import re
import collections
import csv

def find_column_indices( column_indices, sheet, rownum ):
    if column_indices is None:
        for colnum in range( sheet.ncols ):
            cell_value = sheet.cell_value( rownum, colnum )
            if isinstance( cell_value, str ):
                if cell_value.lower() == "titel":
                    column_indices = {}
                    column_indices[ 'title' ] = colnum
                else:
                    if column_indices is not None:
                        maybe_year = re.compile('\d+').match( cell_value )
                        if maybe_year is not None:
                            maybe_year = int( maybe_year.group(0) )
                            if maybe_year > 2000 and maybe_year < 2017:
                                column_indices[ maybe_year ] = colnum
    return column_indices

def select_nurs():

    # JZ_20161117_1322: todo: move this to some config file at some point
    # JZ_20161117_1335: todo: platform independent pathing
    nur_work_book_dir = '../non_disclosed/'
    nur_work_book_extension = '.xlsx'
    nur_work_book_name = 'ebook assortiment 18-10-2016'
    nur_isbn_column = 0
    nur_title_column = 1
    nur_author_column = 2
    nur_column = 7
    select_nurs = [ '285', '300', '301', '302', '305', '311', '330', '340' ]
    sales_work_book_dir = nur_work_book_dir
    sales_work_book_extension = nur_work_book_extension
    sales_work_book_name = 'Totaal verkoop 2010-2016 titels AWB VIB DBB aantal verkocht'
    sales_author_column = 1

    work_book = xlrd.open_workbook( nur_work_book_dir + nur_work_book_name + nur_work_book_extension )
    sheet_names = work_book.sheet_names()
    nur_pattern = re.compile( "(\\d{3})\s{1}" )

    # Create a dictionary of works with the chosen NURs
    selected_works = {}
    for name in sheet_names:
        sheet = work_book.sheet_by_name( name )
        for rownum in range( sheet.nrows ):
            nur_match = nur_pattern.match( sheet.cell_value( rownum, nur_column ) )
            if nur_match is not None:
                if nur_match.group(1) in select_nurs:
                    nur_title = sheet.cell_value( rownum, nur_title_column )
                    # Note: Sheets vary in how they have the author name.
                    # For author_key we abstract/deconstruct to lower case
                    # first part of last name which is inferable for all.
                    # Cases covered:
                    #   Baldacci, David ==> baldacci
                    #   (Geen) ==> geen
                    #   Heerma van Voss, Daan ==> heerma
                    nur_author_name = sheet.cell_value( rownum, nur_author_column )
                    surname_pattern = re.compile( '^\(?([^,\s\)]+)' )
                    nur_author_key = surname_pattern.match( nur_author_name )
                    if nur_author_key is not None:
                        nur_author_key = nur_author_key.group(1).lower()
                    else:
                        nur_author_key = 'geen'
                        print( '.' + nur_author_name )
                    # Note: ( title, author ) isn't actually unique.
                    # A few titles by the same author seem to have printed in
                    # different series. But this shouldn't be a problem as we
                    # are interested in the popularity of the work, not of a
                    # single series
                    if ( nur_title, nur_author_key ) not in selected_works:
                        selected_works[ ( nur_title, nur_author_key ) ] = [ sheet.cell_value( rownum, nur_column ), sheet.cell_value( rownum, nur_isbn_column ), nur_title, nur_author_name ]

    # Find the sales numbers and add them to the dictionary
    work_book = xlrd.open_workbook( sales_work_book_dir + sales_work_book_name + sales_work_book_extension )
    sheet_names = work_book.sheet_names()
    count = 0
    for name in sheet_names:
        sheet = work_book.sheet_by_name( name )
        # Note: unfortunately the title column is not in the same place in each
        # sheet. So we have to look it up
        column_indices = None
        for rownum in range( sheet.nrows ):
            # Todo: Idealy now, we want to match on (author, title), then gather sales numbers
            # Note reg. regepx: Sales sheets have it as 'Heerma van Voss Daan' OR 'HEERMA*DAAN'
            if column_indices is not None:
                sales_title = sheet.cell_value( rownum, column_indices[ 'title' ] )
                if column_indices[ 'title' ] != 0:
                    sales_author_name = sheet.cell_value( rownum, 0 )
                    surname_pattern = re.compile( '(^[^\*\s]*)\*?' )
                else:
                    sales_author_name = sheet.cell_value( rownum, sales_author_column )
                    surname_pattern = re.compile( '(^[^\s]*)\s?' )
                sales_author_key = surname_pattern.match( sales_author_name ).group(1).lower()
                if ( sales_title, sales_author_key ) in selected_works:
                    sales_numbers = {}
                    for column_name in column_indices.keys():
                        if column_name != 'title':
                            number = sheet.cell_value( rownum, column_indices[ column_name ] )
                            if number == '':
                                number = 0
                            else:
                                number = int( number )
                            sales_numbers[ column_name ] = number
                    selected_works[ (sales_title, sales_author_key ) ].append( sales_numbers )
            else:
                column_indices = find_column_indices( column_indices, sheet, rownum )


    selected_having_sales = {}
    for key in selected_works:
        if len( selected_works[ key ] ) >= 5:
            if len( selected_works[ key ] ) > 5:
                sales_left = selected_works[ key ][ 4 ]
                sales_right = selected_works[ key ][ 5 ]
                for year in sales_left:
                    sales_left[ year ] = float( sales_left[ year ] ) + float( sales_right[ year ] )
                selected_works[ key ][ 4 ] = sales_left
                selected_works[ key ].pop()
            selected_having_sales[ key ] = selected_works[ key ]

    with open( '../non_disclosed/nurs.csv', 'w' ) as csvfile:
        fieldnames = [ 'NUR', 'ISBN', 'Titel', 'Auteur', '2010', '2011', '2012', '2013', '2014', '2015', '2016' ]
        writer = csv.writer(csvfile, delimiter=',' )
        writer.writerow( fieldnames )
        for key in selected_having_sales:
            sales_numbers = collections.OrderedDict( sorted( selected_having_sales[ key ][4].items() ) ).values()
            selected_having_sales[ key ].pop()
            selected_having_sales[ key ].extend( sales_numbers )
            writer.writerow( selected_having_sales[key] )

    csvfile.close()


def compare_royal_library_eisbn():
    rl_work_book_dir = '../non_disclosed/'
    rl_work_book_extension = '.xls'
    rl_work_book_name = 'KB Kopie van CB-ebooks per uitgever -20161228'
    rl_isbn_column = 2

    work_book = xlrd.open_workbook( rl_work_book_dir + rl_work_book_name + rl_work_book_extension )
    sheet = work_book.sheet_by_name( 'Blad1' )
    rl_eisbns = []
    for cell in sheet.col( rl_isbn_column ):
        if isinstance( cell.value, float ):
            rl_eisbns.append( '%d' % cell.value )

    nur_isbns = []
    with open( '../non_disclosed/royal_nurs.csv', 'w' ) as csv_outfile:
        fieldnames = [ 'ISBN', 'Titel', 'Auteur', 'Sales 2010-2016' ]
        csv_writer = csv.writer(csv_outfile, delimiter=',' )
        csv_writer.writerow( fieldnames )

        with open( '../non_disclosed/nurs.csv', 'r' ) as csv_infile:
            csv_reader = csv.reader( csv_infile, delimiter=',', quotechar='"')
            for row in csv_reader:
                if row[1] in rl_eisbns:
                    total_sales = 0
                    for column_index in range( 4, 11 ):
                        # Some sale numbers are given as e.g. 456.0
                        # hence: int(float(number)), or it errors out the int()
                        total_sales += int( float( row[ column_index ] ) )
                    csv_writer.writerow( [ row[1], row[2], row[3], total_sales ] )

        csv_infile.close()
    csv_outfile.close()

#select_nurs()
compare_royal_library_eisbn()
print( 'done' )
