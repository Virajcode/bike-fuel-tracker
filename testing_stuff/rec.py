import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

def load_resources(index_path, mapping_path):
    """
    Load the FAISS index and mapping data
    
    Parameters:
    -----------
    index_path : str
        Path to the FAISS index file
    mapping_path : str
        Path to the mapping CSV file
        
    Returns:
    --------
    index : faiss.Index
        Loaded FAISS index
    mapping_df : pandas.DataFrame
        DataFrame with mapping information
    """
    print(f"Loading FAISS index from {index_path}...")
    index = faiss.read_index(index_path)
    
    print(f"Loading mapping data from {mapping_path}...")
    mapping_df = pd.read_csv(mapping_path)
    
    return index, mapping_df

def search_locations(query, index_path="location_vectors.faiss", 
                     mapping_path="vector_mapping.csv", 
                     model_name="all-MiniLM-L6-v2", 
                     top_k=5):
    """
    Search for locations similar to the query
    
    Parameters:
    -----------
    query : str
        User query text
    index_path : str
        Path to the FAISS index file
    mapping_path : str
        Path to the mapping CSV file
    model_name : str
        Name of the sentence transformer model to use
    top_k : int
        Number of results to return
        
    Returns:
    --------
    results : list
        List of dictionaries with search results
    """
    # Load resources
    index, mapping_df = load_resources(index_path, mapping_path)
    
    # Load model
    print(f"Loading model {model_name}...")
    model = SentenceTransformer(model_name)
    
    # Process query
    print(f"Processing query: '{query}'")
    query_vector = model.encode([query])[0].astype(np.float32)
    
    # Check if we need to normalize the vector
    # Assuming it was built with IP (inner product) similarity
    if isinstance(index, faiss.IndexFlatIP):
        query_vector = query_vector / np.linalg.norm(query_vector)
    
    # Search
    distances, indices = index.search(query_vector.reshape(1, -1), top_k)
    
    # Extract results
    results = []
    for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
        if idx == -1:  # FAISS returns -1 if fewer than k results are found
            continue
        
        result = {
            'rank': i + 1,
            'score': float(distance),
            'index': int(idx)
        }
        
        # Add title and other available information
        if 'title' in mapping_df.columns:
            result['title'] = mapping_df.iloc[idx]['title']
        
        if 'place_id' in mapping_df.columns:
            result['place_id'] = mapping_df.iloc[idx]['place_id']
            
        # Add geospatial information if available
        # for geo_col in ['latitude', 'longitude', 'lat', 'lng']:
        #     if geo_col in mapping_df.columns:
        #         result[geo_col] = mapping_df.iloc[idx][geo_col]
        
        results.append(result)
    
    return results

def main():
    """Interactive search function"""
    # Configuration
    index_path = "location_vectors.faiss"
    mapping_path = "vector_mapping.csv"
    model_name = "all-MiniLM-L6-v2"
    
    print("Location Search System")
    print("=====================")
    print(f"Using index: {index_path}")
    print(f"Using mapping: {mapping_path}")
    print()
    
    while True:
        # Get user query
        query = input("Enter your search query (or 'q' to quit): ")
        if query.lower() in ['q', 'quit', 'exit']:
            break
            
        # Set number of results
        try:
            k = int(input("How many results do you want? (default: 5): "))
        except ValueError:
            k = 5
            
        # Perform search
        results = search_locations(query, index_path, mapping_path, model_name, k)
        
        # Display results
        print("\nSearch Results:")
        print("---------------")
        if not results:
            print("No results found.")
        else:
            for result in results:
                print(f"{result['rank']}. {result['title']}")
                # print(f"   Score: {result['score']:.4f}")
                if 'place_id' in result:
                    print(f"   Place ID: {result['place_id']}")
                # 
                print()
        
        print()

if __name__ == "__main__":
    main()