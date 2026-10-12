from dataclasses import dataclass
from pathlib import Path
import math


@dataclass
class Chunk:
    source: str
    text: str
    embedding: list[float]


def split_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    """Simple character-based chunker. Upgrade for language-aware parsing as needed."""
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        chunks.append(cleaned[start:end])
        if end == len(cleaned):
            break
        start = end - overlap
    return chunks


def read_documents(root: Path) -> list[tuple[str, str]]:
    """Read only Markdown and plain-text files from the configured local directory."""
    if not root.exists():
        return []
    documents: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if text.strip():
            documents.append((str(path.relative_to(root)), text))
    return documents


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or not left:
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


class LocalDocumentStore:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []

    async def reindex(self, root: Path, ollama, embedding_model: str) -> int:
        documents = read_documents(root)
        new_chunks: list[tuple[str, str]] = []
        for source, content in documents:
            new_chunks.extend((source, piece) for piece in split_text(content))

        # Build a replacement index only after embeddings succeed.
        embeddings: list[list[float]] = []
        batch_size = 32
        for start in range(0, len(new_chunks), batch_size):
            batch = [text for _, text in new_chunks[start : start + batch_size]]
            embeddings.extend(await ollama.embed(embedding_model, batch))

        if len(embeddings) != len(new_chunks):
            raise RuntimeError("Embedding count does not match chunk count")

        self.chunks = [
            Chunk(source=source, text=content, embedding=embedding)
            for (source, content), embedding in zip(new_chunks, embeddings)
        ]
        return len(self.chunks)

    async def search(self, query: str, ollama, embedding_model: str, top_k: int = 4) -> list[dict]:
        if not self.chunks:
            return []
        query_embeddings = await ollama.embed(embedding_model, [query])
        query_embedding = query_embeddings[0]
        ranked = sorted(
            (
                (cosine_similarity(query_embedding, chunk.embedding), chunk)
                for chunk in self.chunks
            ),
            key=lambda item: item[0],
            reverse=True,
        )
        return [
            {"source": chunk.source, "text": chunk.text, "score": round(score, 4)}
            for score, chunk in ranked[: max(1, top_k)]
        ]
