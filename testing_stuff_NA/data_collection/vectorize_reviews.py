import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def load_data(file_path):
    """Load data from CSV file and handle missing values."""
    print(f"Loading data from {file_path}...")
    df = pd.read_csv(file_path)
    df['combined_text'] = df['combined_text'].fillna('')
    return df

def convert_to_vectors(texts, model_name='all-MiniLM-L6-v2'):
    """Convert text data to vector embeddings."""
    print(f"Loading model {model_name}...")
    model = SentenceTransformer(model_name)
    
    print("Converting texts to vectors...")
    vectors = model.encode(texts, show_progress_bar=True)
    return vectors.astype(np.float32)  # Convert to float32 for FAISS

def create_faiss_index(vectors, index_type='flat'):
    """Create and populate a FAISS index."""
    dimension = vectors.shape[1]
    print(f"Creating FAISS index with dimension {dimension}...")
    
    if index_type == 'flat':
        # Basic flat index using L2 distance
        index = faiss.IndexFlatL2(dimension)
    elif index_type == 'ip':
        # Inner product index (for cosine similarity with normalized vectors)
        index = faiss.IndexFlatIP(dimension)
    else:
        raise ValueError(f"Unsupported index type: {index_type}")
    
    print(f"Adding {len(vectors)} vectors to index...")
    index.add(vectors)
    return index

def save_index_and_mapping(index, df, index_path, mapping_path):
    """Save FAISS index and id mapping."""
    print(f"Saving FAISS index to {index_path}...")
    faiss.write_index(index, index_path)
    
    print(f"Saving mapping data to {mapping_path}...")
    df[['position', 'title', 'place_id']].to_csv(mapping_path, index=False)

def main():
    # Configuration
    file_path = "merged_output.csv"  # Replace with your actual file path
    index_path = "location_vectors.faiss"
    mapping_path = "vector_mapping.csv"
    model_name = "all-MiniLM-L6-v2"
    index_type = "flat"  # 'flat' for L2 distance, 'ip' for inner product
    
    # Process data
    df = load_data(file_path)
    vectors = convert_to_vectors(df['combined_text'].tolist(), model_name)
    index = create_faiss_index(vectors, index_type)
    save_index_and_mapping(index, df, index_path, mapping_path)
    
    print(f"Done! Successfully processed {len(df)} locations.")

if __name__ == "__main__":
    main()

    