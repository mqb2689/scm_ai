from app.rag.document_store import cosine_similarity, split_text


def test_split_text_returns_chunks_with_overlap():
    text = "a" * 2000
    chunks = split_text(text, chunk_size=500, overlap=50)
    assert len(chunks) > 1
    assert chunks[0][-50:] == chunks[1][:50]


def test_split_text_empty():
    assert split_text("  \n ") == []


def test_cosine_similarity_identical_vectors():
    assert abs(cosine_similarity([1.0, 0.0], [1.0, 0.0]) - 1.0) < 1e-9


def test_cosine_similarity_zero_vector():
    assert cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0
