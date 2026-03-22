"""
RAG Indexer for Test Case Matching

Uses sentence-transformers for embedding generation and FAISS for similarity search.
Falls back to simple keyword matching if dependencies are not available.
"""

from typing import List, Dict, Tuple, Optional
import json

from testwright.models.schemas import TestCase


class RAGIndexer:
    """Builds and queries a vector index of test cases for similarity matching"""

    def __init__(self, use_embeddings: bool = True):
        """Initialize the RAG indexer

        Args:
            use_embeddings: If True, use sentence-transformers for embeddings.
                           If False, use simple keyword matching.
        """
        self.use_embeddings = use_embeddings
        self.test_cases: List[TestCase] = []
        self.test_texts: List[str] = []
        self.embeddings = None
        self.model = None
        self.index = None

        if use_embeddings:
            self._init_embedding_model()

    def _init_embedding_model(self):
        """Initialize the sentence transformer model"""
        try:
            from sentence_transformers import SentenceTransformer
            # Use a lightweight model for speed
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("  - RAG: Using sentence-transformers for embeddings")
        except ImportError:
            print("  - RAG: sentence-transformers not installed, falling back to keyword matching")
            self.use_embeddings = False
            self.model = None

    def build_index(self, test_cases: List[TestCase]) -> None:
        """Build the vector index from test cases

        Args:
            test_cases: List of test cases to index
        """
        self.test_cases = test_cases

        # Create text representations for each test case
        self.test_texts = []
        for tc in test_cases:
            text = self._test_case_to_text(tc)
            self.test_texts.append(text)

        if self.use_embeddings and self.model:
            self._build_embedding_index()

        print(f"  - RAG: Indexed {len(test_cases)} test cases")

    def _test_case_to_text(self, tc: TestCase) -> str:
        """Convert a test case to searchable text"""
        parts = [
            tc.title,
            tc.module_title,
            tc.workflow,
            tc.expected_result,
            " ".join(tc.steps[:5])  # First 5 steps
        ]
        return " ".join(parts)

    def _build_embedding_index(self):
        """Build FAISS index from embeddings"""
        try:
            import numpy as np

            # Generate embeddings
            self.embeddings = self.model.encode(
                self.test_texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )

            # Try to use FAISS for faster search
            try:
                import faiss
                dimension = self.embeddings.shape[1]
                self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
                # Normalize embeddings for cosine similarity
                faiss.normalize_L2(self.embeddings)
                self.index.add(self.embeddings)
            except ImportError:
                # Fall back to numpy-based search
                self.index = None
                print("  - RAG: FAISS not installed, using numpy for search")

        except Exception as e:
            print(f"  - RAG: Failed to build embedding index: {e}")
            self.use_embeddings = False

    def search(
        self,
        query: str,
        top_k: int = 5,
        module_filter: Optional[str] = None
    ) -> List[Tuple[TestCase, float]]:
        """Search for test cases similar to the query

        Args:
            query: Search query text
            top_k: Number of results to return
            module_filter: Optional module name to filter by

        Returns:
            List of (TestCase, similarity_score) tuples
        """
        if self.use_embeddings and self.model:
            return self._search_embeddings(query, top_k, module_filter)
        else:
            return self._search_keywords(query, top_k, module_filter)

    def _search_embeddings(
        self,
        query: str,
        top_k: int,
        module_filter: Optional[str]
    ) -> List[Tuple[TestCase, float]]:
        """Search using embeddings"""
        import numpy as np

        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)

        if self.index is not None:
            # Use FAISS
            import faiss
            faiss.normalize_L2(query_embedding)
            scores, indices = self.index.search(query_embedding, min(top_k * 3, len(self.test_cases)))
            scores = scores[0]
            indices = indices[0]
        else:
            # Use numpy
            # Normalize embeddings
            query_norm = query_embedding / np.linalg.norm(query_embedding)
            embeddings_norm = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)
            # Compute cosine similarities
            similarities = np.dot(embeddings_norm, query_norm.T).flatten()
            # Get top indices
            top_indices = np.argsort(similarities)[::-1][:top_k * 3]
            indices = top_indices
            scores = similarities[top_indices]

        # Filter and return results
        results = []
        for idx, score in zip(indices, scores):
            if idx < 0 or idx >= len(self.test_cases):
                continue
            tc = self.test_cases[idx]

            # Apply module filter if specified
            if module_filter and module_filter.lower() not in tc.module_title.lower():
                continue

            results.append((tc, float(score)))

            if len(results) >= top_k:
                break

        return results

    def _search_keywords(
        self,
        query: str,
        top_k: int,
        module_filter: Optional[str]
    ) -> List[Tuple[TestCase, float]]:
        """Fallback keyword-based search"""
        query_words = set(query.lower().split())

        scores = []
        for i, text in enumerate(self.test_texts):
            tc = self.test_cases[i]

            # Apply module filter if specified
            if module_filter and module_filter.lower() not in tc.module_title.lower():
                scores.append((i, 0.0))
                continue

            text_words = set(text.lower().split())
            # Jaccard similarity
            intersection = len(query_words & text_words)
            union = len(query_words | text_words)
            score = intersection / union if union > 0 else 0.0
            scores.append((i, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        # Return top k
        results = []
        for idx, score in scores[:top_k]:
            if score > 0:
                results.append((self.test_cases[idx], score))

        return results

    def get_test_case_by_id(self, test_id: str) -> Optional[TestCase]:
        """Get a test case by its ID"""
        for tc in self.test_cases:
            if tc.id == test_id:
                return tc
        return None
