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

def search_locations(query, index_path, 
                     mapping_path, 
                     model_name, 
                     top_k):
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
            
        results.append(result)
    
    return results

def get_location(query):
    """Interactive search function"""
    # Configuration
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(base_dir, "data_collection", "location_vectors.faiss")
    mapping_path = os.path.join(base_dir, "data_collection", "vector_mapping.csv")
    model_name = "all-MiniLM-L6-v2"
    k = 5

    results = search_locations(query, index_path, mapping_path, model_name, k)

    return results
