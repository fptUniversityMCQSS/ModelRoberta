from haystack.retriever.dense import DensePassageRetriever
def retriever(document_store):
    
    retriever = DensePassageRetriever(document_store=document_store,
                                      query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                                      passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                                      max_seq_len_query=64,
                                      max_seq_len_passage=256,
                                      batch_size=16,
                                      use_gpu=False,
                                      embed_title=True,
                                      use_fast_tokenizers=True,
                                      progress_bar=True)
                                      
    return retriever








