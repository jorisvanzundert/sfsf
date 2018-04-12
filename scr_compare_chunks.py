import csv
import string
from nltk import word_tokenize
from sfsf import training_data_factory
from sfsf import sfsf_config
from collections import defaultdict, Counter
from nltk.probability import FreqDist

def read_chunk_scores( score_file ):
    top_chunk_scores = defaultdict(list)
    bottom_chunk_scores = defaultdict(list)
    with open(score_file, 'rt') as fh:
        csv_reader = csv.reader(fh, delimiter=",")
        headers = next(csv_reader)
        for row in csv_reader:
            if row[0][:8] == "training":
                continue
            isbn = row[2]
            score = float(row[6])
            if row[0] == "testing_bottom":
                bottom_chunk_scores[isbn].append(score)
            else:
                top_chunk_scores[isbn].append(score)
    return top_chunk_scores, bottom_chunk_scores

def compute_doc_freq( top_text_chunks ):
    doc_freq = defaultdict( list )
    for isbn, text_chunks in top_text_chunks:
        terms = set([term for text_chunk in text_chunks for term in tokenize_chunk( text_chunk )])
        for term in terms:
            doc_freq[term] += [isbn]
    return doc_freq

def get_isbn_title(isbn, isbn_data):
    for isbn_row in isbn_data:
        if isbn_row[1] == isbn:
            return isbn_row[2]


def do_sample( top_chunk_scores, bottom_chunk_scores, wpg_data_file ):
    training_factory = training_data_factory.TrainingDataFactory()
    isbn_data = training_factory.get_isbn_data( wpg_data_file ) # returns data sorted by sales
    top_isbn_data = [isbn_row for isbn_row in isbn_data if isbn_row[1] in top_chunk_scores]
    bottom_isbn_data = [isbn_row for isbn_row in isbn_data if isbn_row[1] in bottom_chunk_scores]
    return top_isbn_data, bottom_isbn_data

def get_text_chunks( sample_data ):
    training_factory = training_data_factory.TrainingDataFactory()
    return training_factory.sample_txts( sample_data, sample_size=5000 )

def filter_chunks( chunk_tuples, chunk_scores, threshold, bigger_than ):
    if bigger_than:
        print("filtering bigger than")
        return [ chunk for isbn, chunks in chunk_tuples for chunk, score in zip(chunks, chunk_scores[isbn]) if score >= threshold ]
    else:
        print("filtering smaller than")
        return [ chunk for isbn, chunks in chunk_tuples for chunk, score in zip(chunks, chunk_scores[isbn]) if score < threshold ]

def tokenize_chunk( chunk_as_string ):
    more_punctuation = string.punctuation + '“”‘’«»'
    return word_tokenize( chunk_as_string.lower().translate( str.maketrans( "", "", more_punctuation ) ) )

def make_dist( chunks, doc_freq ):
    return Counter([term for chunk in chunks for term in tokenize_chunk( chunk ) if len(doc_freq[term]) > 1])

def get_most_frequent_terms( isbn_data, chunk_scores, threshold, bigger_than=True ):
    text_chunks = get_text_chunks( isbn_data )
    doc_freq = compute_doc_freq( text_chunks )
    chunks = filter_chunks( text_chunks, chunk_scores, threshold, bigger_than )
    fdist = make_dist( chunks, doc_freq )
    top_terms = [term for term, freq in fdist.most_common(1000)]
    return top_terms, fdist, doc_freq

if __name__ == "__main__":
    wpg_data_file = "wpg_data.csv"
    score_file = "./data/non_disclosed/remote_volume_20170406/report_20170404_0951.csv"
    total_size = 120
    top_chunk_scores, bottom_chunk_scores = read_chunk_scores( score_file )
    top_isbn_data, bottom_isbn_data = do_sample( top_chunk_scores, bottom_chunk_scores, wpg_data_file )
    bottom_terms, bottom_fdist, bottom_doc_freq = get_most_frequent_terms( bottom_isbn_data, bottom_chunk_scores, 0.5, bigger_than=False )
    top_terms, top_fdist, top_doc_freq = get_most_frequent_terms( top_isbn_data, top_chunk_scores, 0.8, bigger_than=True )
    print(bottom_fdist.most_common(100))
    print(top_fdist.most_common(100))
    top_only = [term for term in top_terms[:100] if term not in bottom_terms]
    bottom_only = [term for term in bottom_terms[:100] if term not in top_terms]
    for term in top_only:
        titles = [get_isbn_title(isbn, top_isbn_data) for isbn in top_doc_freq[term]]
        print("top only:", term, top_fdist[term], titles)
    for term in bottom_only:
        titles = [get_isbn_title(isbn, bottom_isbn_data) for isbn in bottom_doc_freq[term]]
        print("bottom only:", term, bottom_fdist[term], titles)
