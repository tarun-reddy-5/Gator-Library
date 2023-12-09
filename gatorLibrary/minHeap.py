class MinHeap:
    def __init__(self):
        # Initialize the heap as an empty list
        self.heap = []

    def parent(self, i):
        # Calculate the index of the parent node
        return (i - 1) // 2

    def left_child(self, i):
        # Calculate the index of the left child node
        return 2 * i + 1

    def right_child(self, i):
        # Calculate the index of the right child node
        return 2 * i + 2

    def swap(self, i, j):
        # Swap elements at indices i and j in the heap
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, reservation): # priority = reservation[0], timestamp = reservation[1]

        # Add a reservation to the heap
        self.heap.append(reservation)
        index = len(self.heap) - 1
        #Maintaining the heap property by swapping elements if necessary
        while index > 0 and self.heap[self.parent(index)] > self.heap[index]:
            self.swap(index, self.parent(index))
            index = self.parent(index)

    def heapify(self, i):
        # Heapify the subtree rooted at index i
        left = self.left_child(i)
        right = self.right_child(i)
        smallest = i
        # Check if left child exists and compare with smallest
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        # Check if right child exists and compare with smallest
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        # If smallest is not the current root, swap and continue heapifying
        if smallest != i:
            self.swap(i, smallest)
            self.heapify(smallest)

    def extract_min(self):
        # Extracting the minimum element from the heap
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify(0)

        return root

    def get_min(self):
        # Get the minimum element without removing it from the heap
        return self.heap[0] if self.heap else None
    
    def traverse_heap(self):
        #Return the patronID from reservations in the heap
        return [item[2] for item in self.heap] # patronID=item[2]

