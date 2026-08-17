import pandas as pd
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

os.environ['JAVA_HOME'] = '/opt/homebrew/opt/openjdk'

review_df = pd.read_csv('/Users/shim/DA/movie_data_analysis/data/pre_processed/review.csv')
master_df = pd.read_csv('/Users/shim/DA/movie_data_analysis/data/pre_processed/movie_master.csv')

okt = Okt()
def extract_nouns_okt(text):
    if not isinstance(text, str):
        return []
    nouns = okt.nouns(text)
    nouns = [noun for noun in nouns if len(noun) > 1]
    return nouns

font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'

def generate_wordcloud(word_counts, title):
    wc = WordCloud(
        font_path=font_path,
        width=800,
        height=400,
        background_color='white',
        colormap='Blues',
        max_words=50
    )
    cloud = wc.generate_from_frequencies(word_counts)
    
print("Merging...")
review_with_title = review_df.merge(master_df[['id', 'title']], on='id', how='left')

for title, group in review_with_title.groupby('title'):
    movie_nouns = []
    for review_text in group['review']:
        movie_nouns.extend(extract_nouns_okt(review_text))
        
    movie_counts = Counter(movie_nouns)
    if movie_counts:
        top_movie_words = dict(movie_counts.most_common(30))
        generate_wordcloud(top_movie_words, f"[{title}] 리뷰 워드클라우드")

print("Done without error.")
