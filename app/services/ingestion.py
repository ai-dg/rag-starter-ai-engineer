"""
Document ingestion pipeline.

This module prepares source documents for semantic retrieval.

Responsibilities:
- Load documents in supported formats: Markdown, plain text, and PDF.
- Validate files before processing them.
- Extract and clean their textual content.
- Split the content into meaningful, overlapping chunks.
- Attach metadata such as the source filename, file type, and PDF page number.
- Generate an embedding for each chunk.
- Store the chunks and their embeddings in Chroma.

The original implementation only supports Markdown files and splits their
content into fixed chunks of 500 characters:

    Markdown files
        -> text extraction
        -> fixed-size chunking
        -> OpenAI embeddings
        -> Chroma vector store

This implementation improves the pipeline in four areas:

1. Multi-format support
   - `.md` and `.txt` files are read as plain text.
   - `.pdf` files are extracted page by page so that page numbers can be
     preserved in the metadata.

2. Input validation
   - Check that the documents directory exists.
   - Reject unsupported file formats.
   - Reject empty files.
   - Reject files whose content cannot be extracted.
   - Reject documents with empty extracted text.
   - Reject files that exceed the configured size limit.
   - Ensure that at least one valid document is available for indexing.

3. Error handling
   - Log invalid or unreadable files with a clear error message.
   - Skip an invalid file when other valid documents can still be processed.
   - Stop the ingestion with an explicit error if no valid document remains.

4. Chunking strategy
   - Prefer splitting at paragraph, line, or sentence boundaries.
   - Use an overlap between consecutive chunks to preserve context around
     chunk boundaries.
   - Keep the chunk size and overlap configurable.
"""



# def load_docs():
#     print("chargement des documents...")
#     texts = []
#     files = glob.glob(DOCS_DIR + "/*.md")
#     for f in files:
#         content = open(f).read()
#         texts.append(content)
#         print("ok ->", f)
#     print(f"{len(texts)} fichiers charges")
#     return texts


# def chunk_text(text):
#     chunks = []
#     i = 0
#     while i < len(text):
#         chunks.append(text[i:i + CHUNK_SIZE])
#         i = i + CHUNK_SIZE
#     return chunks


# def build_index():
#     texts = load_docs()

#     all_chunks = []
#     for t in texts:
#         for c in chunk_text(t):
#             all_chunks.append(c)

#     print(f"{len(all_chunks)} chunks generes")

#     docs = []
#     for c in all_chunks:
#         docs.append(Document(page_content=c))

#     embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
#     store = Chroma.from_documents(docs, embeddings)

#     print("index construit")
#     return store




