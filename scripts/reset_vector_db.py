"""Reset Vector Database"""

import shutil
import os

def reset_vector_db(db_path: str = "../vectorstore/chroma"):
    """Delete and recreate the vector database"""
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
        print(f"✅ Deleted {db_path}")
    
    os.makedirs(db_path, exist_ok=True)
    print(f"✅ Created fresh {db_path}")

if __name__ == "__main__":
    reset_vector_db()
