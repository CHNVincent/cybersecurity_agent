import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import pickle


class ShortTermMemory:
    """
    Short-term memory for storing current conversation context
    Uses in-memory cache for quick access during conversation session
    """

    def __init__(self, capacity: int = 20):
        self.messages_buffer = []
        self.capacity = capacity
        self.conversation_id = None

    def add_message(self, message: Dict[str, str]):
        """
        Add a message to short-term memory
        """
        # Add timestamp to the message
        message_with_ts = message.copy()
        message_with_ts["timestamp"] = datetime.now().isoformat()
        self.messages_buffer.append(message_with_ts)

        # Maintain capacity
        if len(self.messages_buffer) > self.capacity:
            self.messages_buffer.pop(0)

    def get_recent_messages(self, n: int = 5) -> List[Dict[str, str]]:
        """
        Retrieve the most recent n messages
        """
        return (
            self.messages_buffer[-n:]
            if len(self.messages_buffer) >= n
            else self.messages_buffer[:]
        )

    def get_all_messages(self) -> List[Dict[str, str]]:
        """
        Get all messages in short term memory
        """
        return self.messages_buffer[:]

    def clear(self):
        """
        Clear short-term memory
        """
        self.messages_buffer.clear()

    def set_conversation_id(self, conv_id: str):
        """
        Set the conversation ID associated with this memory
        """
        self.conversation_id = conv_id

    def get_conversation_id(self) -> Optional[str]:
        """
        Get the conversation ID
        """
        return self.conversation_id


class LongTermMemory:
    """
    Long-term memory using vector storage for storing important dialogues,
    audit reports and learning outcomes persistently
    """

    def __init__(self, vector_db_path: str = "./memory_store"):
        self.vector_db_path = vector_db_path
        self.storage_file = os.path.join(vector_db_path, "memory_storage.json")

        # Ensure directory exists
        os.makedirs(vector_db_path, exist_ok=True)

        # Load memory if exists
        if os.path.exists(self.storage_file):
            self.memory_store = self._load_memory()
        else:
            self.memory_store = []

    def _convert_memory_object(
        self, content: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Helper to convert content and metadata into memory object
        """
        return {
            "id": len(self.memory_store),
            "content": content,
            "vector": self._generate_simple_vector(content),  # Basic embedding sim
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

    def _generate_simple_vector(self, text: str) -> List[float]:
        """
        Very simple vector representation of text (in real implementation,
        would use a proper embedding model)
        """
        # Simple hash-based vector (not for production use)
        import hashlib
        import struct

        hash_str = hashlib.sha256(text.encode()).hexdigest()
        # Convert hex to floats
        vector = []
        for i in range(0, len(hash_str), 8):
            chunk = hash_str[i : i + 8]
            if len(chunk) == 8:
                vector.append(struct.unpack(">f", bytes.fromhex(chunk.zfill(8)))[0])
        return (
            vector[:384] if len(vector) > 384 else vector + [0.0] * (384 - len(vector))
        )

    def _save_memory(self):
        """
        Save memory to disk
        """
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.memory_store, f, ensure_ascii=False, indent=2)

    def _load_memory(self) -> List[Dict[str, Any]]:
        """
        Load memory from disk
        """
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def store(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Store information in long-term memory
        """
        memory_obj = self._convert_memory_object(content, metadata)
        self.memory_store.append(memory_obj)
        self._save_memory()

    def retrieve_by_similarity(
        self, query: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve memories similar to the query
        Simple implementation based on string similarity (not optimized for production)
        """
        query_vector = self._generate_simple_vector(query)
        similarities = []

        for memory_obj in self.memory_store:
            similarity = self._calculate_similarity(query_vector, memory_obj["vector"])
            similarities.append((similarity, memory_obj))

        # Sort by similarity (descending) and return top_k
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [mem[1] for mem in similarities[:top_k]]

    def _calculate_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        if not vec1 or not vec2:
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def search(
        self, query: str, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search memory with optional filtering
        """
        results = []

        # Convert query to vector and search by similarity
        similar_results = self.retrieve_by_similarity(query, top_k=10)

        # Apply filters if defined
        if filters:
            filtered_results = []
            for result in similar_results:
                match = True
                for key, value in filters.items():
                    if (
                        key not in result.get("metadata", {})
                        or result["metadata"][key] != value
                    ):
                        match = False
                        break
                if match:
                    filtered_results.append(result)
            return filtered_results
        else:
            return similar_results

    def remove(self, memory_id: str):
        """
        Remove a specific memory item by ID
        """
        self.memory_store = [mem for mem in self.memory_store if mem["id"] != memory_id]
        self._save_memory()

    def clear(self):
        """
        Clear all long-term memory
        """
        self.memory_store = []
        self._save_memory()
