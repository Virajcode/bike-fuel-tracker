from dotenv import load_dotenv
load_dotenv()
import serpapi
import os
import config as con
import pandas as pd
import csv


class SerpAPIDataExtractor:
    def __init__(self, search_query, no_of_results):
        self.api_key = os.getenv('SERPAPI_KEY')
        self.client = serpapi.Client(api_key=self.api_key)
        self.search_query = search_query
        self.no_of_results = no_of_results
        self.data_folder = 'location_csv'
        os.makedirs(self.data_folder, exist_ok=True)
    
    def fetch_data(self, start):
        """Fetch data from SerpAPI for a given start index."""
        results = self.client.search({
            'engine': 'google_maps',
            'type': 'search',
            'q': self.search_query,
            'll': '@18.516726,73.856255,10z',
            'start': start
        })
        return results
    
    def extract_fields(self, data):
        """Extract required fields from API response."""
        local_results = data.get("local_results", [])
        
        extracted_data = {
            'position': [entry.get('position', None) for entry in local_results],
            'title': [entry.get('title', '') for entry in local_results],
            'place_id': [entry.get('place_id', '') for entry in local_results],
            'latitude': [entry.get('gps_coordinates', {}).get('latitude', None) for entry in local_results],
            'longitude': [entry.get('gps_coordinates', {}).get('longitude', None) for entry in local_results],
            'rating': [entry.get('rating', None) for entry in local_results],
            'reviews': [entry.get('reviews', None) for entry in local_results],
            'type': [entry.get('type', '') for entry in local_results],
            'types': [entry.get('types', []) for entry in local_results]
        }
        return extracted_data
    
    def save_csv(self, data, start):
        """Save extracted data to a CSV file."""
        df = pd.DataFrame(data)
        file_path = f'{self.data_folder}/meta_data_{self.search_query}_{start}.csv'
        df.to_csv(file_path, index=False)
        print(f"{file_path} extracted successfully")
    
    def combine_csv_files(self):
        """Combine all saved CSV files into one final file."""
        dfs = []
        for j in range(0, self.no_of_results, 20):
            file_path = f'{self.data_folder}/meta_data_{self.search_query}_{j}.csv'
            df = pd.read_csv(file_path)
            dfs.append(df)
        
        combined_df = pd.concat(dfs, ignore_index=True)
        final_path = f'{self.data_folder}/{self.search_query}.csv'
        combined_df.to_csv(final_path, index=False)
        print("CSV files combined successfully!")
    
    def clean_up(self):
        """Remove intermediate CSV files."""
        for j in range(0, self.no_of_results, 20):
            file_path = f'{self.data_folder}/meta_data_{self.search_query}_{j}.csv'
            os.remove(file_path)
            print(f'{file_path} removed successfully')
    
    def run(self):
        """Execute the full extraction and processing pipeline."""
        for j in range(0, self.no_of_results, 20):
            data = self.fetch_data(j)
            extracted_data = self.extract_fields(data)
            self.save_csv(extracted_data, j)
        
        self.combine_csv_files()
        self.clean_up()


class GoogleMapsReviewsExtractor:
    def __init__(self, search_query):
        self.api_key = os.getenv('SERPAPI_KEY')
        self.client = serpapi.Client(api_key=self.api_key)
        self.search_query = search_query
        self.input_file = f'location_csv/{self.search_query}.csv'
        self.output_folder = 'location_csv'
        os.makedirs(self.output_folder, exist_ok=True)
    
    def extract_reviews(self):
        reviews = []
        topics = []
        place_ids = []
        
        with open(self.input_file, mode='r', encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for i, row in enumerate(csv_reader, start=1):
                place_id = row['place_id']
                place_ids.append(place_id)
                
                result = self.client.search({
                    'engine': "google_maps_reviews",
                    'place_id': place_id,
                    'sort_by': "ratingHigh"
                })
                
                review_list = []
                count = min(len(result.get("reviews", [])), 10)
                for j in range(count):
                    try:
                        review_list.append(result["reviews"][j]['extracted_snippet']['original'])
                    except KeyError:
                        print(f"No reviews found for {row['title']}")
                        continue
                reviews.append(review_list)
                
                topic_list = [t['keyword'] for t in result.get("topics", [])] if result.get("topics") else ["NA"]
                topics.append(topic_list)
                print(i)
        
        data = {'place_id': place_ids, 'reviews': reviews, 'topics': topics}
        df = pd.DataFrame(data)
        df.to_csv(f'{self.output_folder}/review_{self.search_query}.csv', index=False)
        print(f"Reviews for {self.search_query} extracted successfully")
    
    def run(self):
        self.extract_reviews()


class DataHandler:
    def __init__(self, search_query):
        self.search_query = search_query
        self.location_file = f'location_csv/{search_query}.csv'
        self.review_file = f'location_csv/review_{search_query}.csv'
        self.processed_file = f'location_csv/{search_query}_review_processed.csv'
        self.merged_file = f'location_csv/{search_query}_merged.csv'

    def process_data(self):
        import pandas as pd
        import numpy as np
        import re
        import ast
        import nltk
        from nltk.corpus import stopwords
        from nltk.stem.porter import PorterStemmer

        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        ps = PorterStemmer()

        def remove_emojis(text):
            emoji_pattern = re.compile(
                "[" 
                "\U0001F600-\U0001F64F"  # emoticons
                "\U0001F300-\U0001F5FF"  # symbols & pictographs
                "\U0001F680-\U0001F6FF"  # transport & map symbols
                "\U0001F700-\U0001F77F"  # alchemical symbols
                "\U0001F780-\U0001F7FF"  # geometric shapes
                "\U0001F800-\U0001F8FF"  # supplemental arrows
                "\U0001F900-\U0001F9FF"  # supplemental symbols
                "\U00002600-\U000026FF"  # miscellaneous symbols
                "\U00002700-\U000027BF"  # dingbats
                "\U0001FA00-\U0001FA6F"  # chess symbols
                "\U0001F1E0-\U0001F1FF"  # flags
                "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', text)

        def remove_stopwords(text):
            return ' '.join([word for word in text.split() if word.lower() not in stop_words])

        def stem(text):
            return " ".join([ps.stem(word) for word in text.split()])

        df = pd.read_csv(self.review_file)
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)
        df['Position'] = range(1, len(df) + 1)
        df = df[['Position', 'place_id', 'reviews', 'topics']]
        df['topics'] = df['topics'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else x)
        df['topics'] = df['topics'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
        df['reviews'] = df['reviews'].apply(ast.literal_eval)
        df['reviews'] = df['reviews'].apply(lambda x: ', '.join(x))
        df['reviews'] = df['reviews'].apply(lambda x: x.lower())
        df['topics'] = df['topics'].apply(lambda x: x.lower())
        df['reviews'] = df['reviews'].str.replace(r'[,.?\n]', '', regex=True)
        df['reviews'] = df['reviews'].apply(remove_emojis)
        df['reviews'] = df['reviews'].apply(remove_stopwords)
        df['reviews'] = df['reviews'].apply(stem)
        df.to_csv(self.processed_file, index=False)
        print(f"Processed data saved to {self.processed_file}")

    def merge_data(self):
        import pandas as pd

        df1 = pd.read_csv(self.location_file)
        df2 = pd.read_csv(self.processed_file)
        merged_df = pd.merge(df1, df2, on="place_id", how="inner")
        merged_df["combined_text"] = merged_df["title"] + " " + merged_df["types"] + " " + merged_df["reviews_y"] + " " + merged_df["topics"]
        merged_df['combined_text'] = merged_df['combined_text'].str.replace(r'[,.\[\]\n]', '', regex=True)
        merged_df.to_csv(self.merged_file, index=False)
        print(f"Merged data saved to {self.merged_file}")

    
    def clean_up(self):
        """Remove intermediate CSV files."""
        os.remove(self.location_file)
        os.remove(self.review_file)
        os.remove(self.processed_file)
        print(f'{self.location_file} removed successfully')
        print(f'{self.review_file} removed successfully')
        print(f'{self.processed_file} removed successfully')

    def run(self):
        self.process_data()
        self.merge_data()
        self.clean_up()


# Updated pipeline
for search_query in con.categories:
    extractor = SerpAPIDataExtractor(search_query, con.no_of_results)
    extractor.run()

    review_extractor = GoogleMapsReviewsExtractor(search_query)
    review_extractor.run()

    handler = DataHandler(search_query)
    handler.run()