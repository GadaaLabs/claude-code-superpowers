# AI Engineering — RAG Architecture Patterns

## Chunking Strategy

```markdown
## Chunking Decision Framework

| Document Type  | Chunk Size       | Overlap | Rationale                              |
|----------------|------------------|---------|----------------------------------------|
| Technical docs | 512–1024 tokens  | 10–15%  | Preserve code blocks, API signatures   |
| Legal contracts| 256–512 tokens   | 20%     | Maintain clause boundaries             |
| Research papers| 512 tokens       | 10%     | Keep abstract/intro intact             |
| Conversations  | 256 tokens       | 25%     | Preserve turn-taking context           |
| Code files     | Function-level   | N/A     | Split by function boundaries           |
```

```python
def chunk_document(text, strategy='semantic'):
    if strategy == 'fixed':
        return fixed_size_chunks(text, size=512, overlap=50)
    elif strategy == 'semantic':
        return semantic_chunks(text, embedding_model='all-MiniLM-L6-v2')
    elif strategy == 'recursive':
        return recursive_chunks(text, separators=['\n\n', '\n', '. '])
    elif strategy == 'code':
        return function_level_chunks(text)  # Parse AST
```

## Embedding Selection

```markdown
| Model                   | Dim  | Max Input | Speed  | Best For                     |
|-------------------------|------|-----------|--------|------------------------------|
| all-MiniLM-L6-v2        | 384  | 512       | Fast   | General RAG, low latency     |
| bge-large-en-v1.5       | 1024 | 512       | Medium | High-accuracy RAG            |
| text-embedding-3-large  | 3072 | 8191      | Slow   | Enterprise, multi-lingual    |
| e5-large-v2             | 1024 | 512       | Medium | Query-document asymmetry     |
| mxbai-embed-large       | 1024 | 512       | Medium | Open-source best quality     |
```

```python
EMBEDDING_CONFIG = {
    'model': 'bge-large-en-v1.5',
    'dimension': 1024,
    'normalize': True,       # L2 normalization for cosine similarity
    'batch_size': 32,
    'device': 'cuda' if available else 'cpu',
    'cache_embeddings': True,
}
```

## Retrieval Methods

```
Need exact keyword match?  → lexical (BM25)
Need semantic recall?      → dense retrieval
Need both?                 → hybrid (BM25 + dense, RRF weighted)
Need diversity?            → MMR (Maximal Marginal Relevance)
Multi-hop questions?       → iterative retrieval (retrieve → expand → retrieve)
```

```python
def retrieve(query, index, method='hybrid'):
    if method == 'lexical':
        return bm25_search(query, index, k=10)
    elif method == 'semantic':
        return cosine_similarity_search(embed(query), index, k=10)
    elif method == 'hybrid':
        lexical  = bm25_search(query, index, k=20)
        semantic = cosine_similarity_search(embed(query), index, k=20)
        return reciprocal_rank_fusion(lexical, semantic, k=10)
    elif method == 'mmr':
        return maximal_marginal_relevance(query, index, k=10, diversity=0.5)
```

## Re-ranking Config

```python
RERANKING_CONFIG = {
    'enabled': True,
    'model': 'cross-encoder/ms-marco-MiniLM-L-6-v2',
    'rerank_top_k': 5,   # From initial 20 results
    'alternatives': {
        'llm_rerank': {
            'prompt': 'Rank these documents by relevance to: {query}\n\nDocs: {docs}',
            'model': 'gpt-3.5-turbo',
            'cost_per_rerank': 0.002,
        },
        'prompt_compression': {
            'model': 'llm2vec',
            'compression_ratio': 0.3,
        }
    }
}
```

## Context Window Management

```python
CONTEXT_CONFIG = {
    'max_context_tokens': 8192,
    'strategies': {
        'truncate':       'Keep most relevant chunks until full',
        'compress':       'Use LLM2Vec to compress chunks',
        'map_reduce':     'Process chunks separately, combine results',
        'sliding_window': 'Process overlapping windows',
    },
    'token_budget': {
        'system_prompt':     500,
        'query':             100,
        'retrieved_context': 6000,
        'output_reserve':    1592,
    }
}
```
