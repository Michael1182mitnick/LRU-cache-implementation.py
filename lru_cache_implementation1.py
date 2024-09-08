# Implement a Least Recently Used (LRU) cache using a data structure that supports get and put operations in 𝑂(1)time.

class Node:
    """Doubly Linked List Node."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        """Initialize the LRUCache with a given capacity."""
        self.capacity = capacity
        self.cache = {}  # HashMap to store key -> Node
        self.head = Node(0, 0)  # Dummy head of the doubly linked list
        self.tail = Node(0, 0)  # Dummy tail of the doubly linked list
        self.head.next = self.tail  # Initialize the list as empty
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Remove a node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_tail(self, node: Node) -> None:
        """Add a new node right before the tail."""
        prev_tail = self.tail.prev
        prev_tail.next = node
        node.prev = prev_tail
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        """Get the value of the key if it exists in the cache, otherwise return -1."""
        if key in self.cache:
            node = self.cache[key]
            # Move the accessed node to the end (most recently used)
            self._remove(node)
            self._add_to_tail(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """Add or update the value of the key. Evict the least recently used if capacity is exceeded."""
        if key in self.cache:
            # Update the value of an existing node
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_tail(node)
        else:
            if len(self.cache) >= self.capacity:
                # Remove the least recently used item (head's next node)
                lru_node = self.head.next
                self._remove(lru_node)
                del self.cache[lru_node.key]
            # Add the new key-value pair
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_tail(new_node)


# Example usage
lru_cache = LRUCache(2)
lru_cache.put(1, 1)  # Cache is {1=1}
lru_cache.put(2, 2)  # Cache is {1=1, 2=2}
print(lru_cache.get(1))  # Returns 1
lru_cache.put(3, 3)  # Evicts key 2, Cache is {1=1, 3=3}
print(lru_cache.get(2))  # Returns -1 (not found)
lru_cache.put(4, 4)  # Evicts key 1, Cache is {3=3, 4=4}
print(lru_cache.get(1))  # Returns -1 (not found)
print(lru_cache.get(3))  # Returns 3
print(lru_cache.get(4))  # Returns 4