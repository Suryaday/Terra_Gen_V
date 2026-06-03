from vectorstore_loader import load_docs

docs=load_docs()

count=0

for doc in docs:

    chunks=build_chunk(

        doc.page_content,

        doc.metadata["service"],

        doc.metadata["source"]

    )

    count+=len(chunks)

    if count>20:

        break

    for chunk in chunks:

        print("="*80)

        print(chunk["metadata"])

        print(chunk["text"][:500])