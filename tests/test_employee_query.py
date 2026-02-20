import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path='./vectorstore/chroma')
collection = client.get_collection(name='company_documents')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Test employee query with role_general filter
query = 'What is the remote work policy?'
embedding = model.encode(query, normalize_embeddings=True).tolist()

# Query with employee role (role_general filter)
results = collection.query(
    query_embeddings=[embedding],
    n_results=5,
    where={'role_general': True}
)

print('Results with role_general=True:')
if results['documents'] and results['documents'][0]:
    for i, (doc, meta, dist) in enumerate(zip(results['documents'][0], results['metadatas'][0], results['distances'][0]), 1):
        relevance = (1 - dist) * 100
        print(f'{i}. Relevance: {relevance:.1f}%')
        print(f'   Source: {meta["source_document"]}')
        print(f'   Section: {meta["section_title"]}')
        print(f'   Preview: {doc[:80]}...')
        print()
else:
    print('No results found!')
