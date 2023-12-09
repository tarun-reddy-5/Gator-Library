import time
from minHeap import MinHeap

class BookNode:
    # Class BookNode for storing the info about the book.
    def __init__(self, bookID, title, author, availability='Yes', borrowedBy=None):
        self.bookID = bookID
        self.title = title
        self.author = author
        self.availability = availability
        self.borrowedBy = borrowedBy
        self.reservationHeap = MinHeap()  # Binary min-heap object for reservations
        self.reservations = [] # PatronID waitlist for the book ordered by the patron’s priority

    

class Node:
    # Each Node represents a book in the Red Black Tree
    def __init__(self, bookNode, color='red'): #Assigning the Red color for a newly created Node
        self.book = bookNode #bookNode object
        self.key = bookNode.bookID
        self.left = None
        self.right = None
        self.parent = None
        self.color = color
        


class RedBlackTree:
    def __init__(self): #RedBlackTree Constructor
        self.root = None # Initialize the root of the Red-Black Tree
        self.colorDic={} #Dictionary to hold the Key, Color pairs
        self.colorFlipCount=0

# insert start
# Perform left rotation around node x
    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

# Perform right rotation around node y
    def rotate_right(self, y):
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

# Insert a new node into the Red-Black Tree
    def insert(self, bookNode):
        new_node = Node(bookNode)
        new_key = new_node.key
        # If the tree is empty, new node is the root
        if not self.root:
            self.root = new_node
            self.root.color = 'black' # color of the root should be black
        else:
            current = self.root
            parent = None
            # Traversing the tree to find the appropriate position for the new node
            while current:
                parent = current
                if new_key < current.key:
                    current = current.left
                else:
                    current = current.right
            # Setting the parent of the new node and adjusting left/right child accordingly
            new_node.parent = parent
            if new_key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
            self.insert_fix(new_node) # Fixing any violations of Red-Black Tree properties after insertion

        self.colorFlipCount_update() # Updating color flip count after insertion

# Fixing violations in the Red-Black Tree properties after insertion
    def insert_fix(self, node):
        while node.parent and node.parent.color == 'red':
            # Checking if the parent is a left child of its parent
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                # Case 1: Uncle is red
                if uncle and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right: # Case 2: Node is a right child
                        node = node.parent
                        self.rotate_left(node)
                    # Case 3: Node is a left child
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                # Case 1: Uncle is red
                if uncle and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    
                    if node == node.parent.left: # Case 2: Node is a left child
                        node = node.parent
                        self.rotate_right(node)
                    # Case 3: Node is a right child
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.rotate_left(node.parent.parent)

        self.root.color = 'black' # Ensuring the root remains black to satisfy Red-Black Tree properties

# insert end

# Search start

    def search(self, bookID):
        # Searching for the key i.e bookID using binary search tree traversal technique
        current = self.root
        while current and current.key != bookID:
            if bookID < current.key:
                current = current.left
            else:
                current = current.right
        return current  # Returns the node if found, None otherwise
    
# Search end
    
# Delete start

    def delete(self, key):
        # Function to delete a node with the given key from the Red-Black Tree
        node_to_delete = self.search(key)
        if node_to_delete is None:
            return None # If the node to delete is not found, return None
        # Handling scenarios for deletion based on the type of node and its children
        if node_to_delete == self.root and not node_to_delete.left and not node_to_delete.right:
            # Case: Deleting the root when it has no children
            self.root = None
        else:
            self.delete_node(node_to_delete) # Delete the found node

        self.colorFlipCount_update() # Update the color flip count after deletion

        reserveList = node_to_delete.book.reservations
        return reserveList # Return the list of reservations (if any) for the deleted node

    def delete_node(self, node):
        # Function to handle node deletion by rearranging the tree
        # Determine the node to be removed and its successor/predecessor
        if node.left is None or node.right is None:
            y = node
        else:
            y = self.predecessor(node)  # Get the predecessor for the node (used for root deletion)
        # Determine the child node of the node to be removed
        if y.left:
            x = y.left
        else:
            x = y.right

        if x:
            x.parent = y.parent # Update the parent node of the child node
        # Reassign the parent's child reference to the child node
        if y.parent is None:
            self.root = x # If the node to delete is the root, update the root reference
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        # If the node to delete isn't the node found for deletion, update its key
        if y != node:
            node.key = y.key
        # Perform fixup if the node removed was a black node
        if y.color == 'black':
            self.delete_fix(x, y.parent) # Fix the Red-Black Tree properties

    def delete_fix(self, x, x_parent):
        # Function to fix Red-Black Tree properties after deletion
        while x != self.root and (x is None or x.color == 'black'):
            if x == x_parent.left:
                # Handling cases when x is a left child of its parent
                sibling = x_parent.right

                if sibling.color == 'red':
                    # Case 1: Sibling is red
                    sibling.color = 'black'
                    x_parent.color = 'red'
                    self.rotate_left(x_parent)
                    sibling = x_parent.right

                if (sibling.left is None or sibling.left.color == 'black') and \
                   (sibling.right is None or sibling.right.color == 'black'):
                    # Case 2: Both of sibling's children are black
                    sibling.color = 'red'
                    x = x_parent
                    x_parent = x.parent
                else:
                    if sibling.right is None or sibling.right.color == 'black':
                    # Case 3: Sibling's right child is black
                        sibling.left.color = 'black'
                        sibling.color = 'red'
                        self.rotate_right(sibling)
                        sibling = x_parent.right
                    # Case 4: Sibling's right child is red
                    sibling.color = x_parent.color
                    x_parent.color = 'black'
                    sibling.right.color = 'black'
                    self.rotate_left(x_parent)
                    x = self.root
            else:
                # Handling cases when x is a right child of its parent (symmetric to the left child cases)
                sibling = x_parent.left

                if sibling.color == 'red':
                    sibling.color = 'black'
                    x_parent.color = 'red'
                    self.rotate_right(x_parent)
                    sibling = x_parent.left

                if (sibling.right is None or sibling.right.color == 'black') and \
                   (sibling.left is None or sibling.left.color == 'black'):
                    sibling.color = 'red'
                    x = x_parent
                    x_parent = x.parent
                else:
                    if sibling.left is None or sibling.left.color == 'black':
                        sibling.right.color = 'black'
                        sibling.color = 'red'
                        self.rotate_left(sibling)
                        sibling = x_parent.left

                    sibling.color = x_parent.color
                    x_parent.color = 'black'
                    sibling.left.color = 'black'
                    self.rotate_right(x_parent)
                    x = self.root

        if x:
            x.color = 'black' # Ensure the root's color remains black after fixing properties

    def predecessor(self, node):
        # Function to find the predecessor node of a given node
        if node.left:
            node = node.left
            while node.right:
                node = node.right
            return node
        # Handling the parent node when the given node doesn't have a left child
        parent = node.parent
        while parent and node == parent.left:
            node = parent
            parent = parent.parent
        return parent

    
# Delete End

#inorder traversal start

    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result) # Starting the inorder traversal from the root node
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node) #Appending the Red Black Tree nodes into the result List
            self._inorder(node.right, result)

#inorder traversal start

#Range Search starts

    def range_books(self, start_key, end_key):
    #Using the inorder traversal to find the books in the given range of BookID's
        range_book_nodes =[]
        inorder = self.inorder_traversal()
        for node in inorder:
            if(node.key>=start_key and node.key<=end_key):
                range_book_nodes.append(node)

        return range_book_nodes
    
#Range Search ends

#closest key start

    def closest_keys_with_min_difference(self, target_key):
    #Using the inorder traversal to find the closest bookID for a given bookID
        inorder = self.inorder_traversal()

        closest_smaller = float('-inf') #Assigning minus infinity to closest_smaller
        closest_larger = float('inf') #Assigning infinity to closest_larger

        closest_smaller_node = None
        closest_larger_node = None

        for node in inorder:
            if node.key == target_key: #If the bookID is present in the Red Black Tree, return the Node
                return node, None
            elif node.key < target_key:
                #Getting the bookID with maximum value from all the bookID's smaller than the given bookID
                if closest_smaller != max(closest_smaller, node.key):
                    closest_smaller = max(closest_smaller, node.key)
                    closest_smaller_node = node
            elif node.key > target_key:
                #Getting the bookID with minimum value from all the bookID's greater than the given bookID
                if closest_larger != min(closest_larger, node.key):
                    closest_larger = min(closest_larger, node.key)
                    closest_larger_node = node

        if closest_smaller == float('-inf'):
            closest_smaller_node = None # Assigning None value if their is no bookID smaller than the given bookID
        if closest_larger == float('inf'):
            closest_larger_node = None # Assigning None value if their is no bookID greater than the given bookID

        return closest_smaller_node, closest_larger_node

  
#closest key end


#BorrowBook start

    def BorrowBook(self, patron_id, book_id,priority):
    # Function to assign book to the Patron and updating the reservation Heap
        bookNode = self.search(book_id) #Searching whether the book exists in the Library
        reserveHeap = bookNode.book.reservationHeap
        if bookNode == None:
            return None, False, patron_id
        else:
            book_availability = bookNode.book.availability
            book_availability = book_availability.lower()
            if (book_availability == 'no'):
                # Inserting the Patron into Reservation Heap as the book is not available
                timestamp = time.time() # Using timestamp for reservation if the priority is same
                reservation = (priority, timestamp, patron_id)
                reserveHeap.insert(reservation)
                traverseList = reserveHeap.traverse_heap()
                # Assiging the List of only PatronID's to the reservationList on the basis of Priority
                bookNode.book.reservations = traverseList 
                #bookNode.book.borrowedBy = patron_id
                return book_id, True, patron_id
            else:
                # Assigning the book to the Patron as the book is available
                bookNode.book.borrowedBy = patron_id
                bookNode.book.availability = 'No'
                traverseList = reserveHeap.traverse_heap()
                bookNode.book.reservations = traverseList
                return book_id, False, patron_id


#BorrowBook end

#ReturnBook start

    def ReturnBook(self, patron_id, book_id):
    # Function to return book by the Patron and assigning the book to next Patron in reservation Heap    
        bookNode = self.search(book_id)
        reserveHeap = bookNode.book.reservationHeap
        nextReservation = reserveHeap.extract_min() # Calling the extract_min method in MinHeap to assign the book to next Patron
        bookNode.book.reservations = reserveHeap.traverse_heap()
        if nextReservation is None:
            bookNode.book.borrowedBy = None
            bookNode.book.availability = 'Yes' # If their are no reservations then make the book available
            return book_id, None
        else:
            bookNode.book.borrowedBy = nextReservation[2]

        return book_id, nextReservation[2]

#ReturnBook end


#Color Flip Starts

    def colorFlip_inorder_traversal(self):
        # Inorder traversal of the red Black Tree to create a dictionary with the latest key, color pairs
        dic = {}
        self.colorFlip_inorder(self.root, dic)
        return dic

    def colorFlip_inorder(self, node, dic):
        if node:
            self.colorFlip_inorder(node.left, dic)
            dic[node.key]=node.color # Updating the dictionary with key, color pairs after insert or delete for comparision
            self.colorFlip_inorder(node.right, dic)

    def colorFlipCount_update(self):
    # Function to update the color flip count
        comp_dic1 = self.colorDic # Dictionary before insert ot delete
        comp_dic2 = self.colorFlip_inorder_traversal() # Dictionary after insert ot delete
        for key in comp_dic2:
            if key in comp_dic1:
                if(comp_dic1[key] != comp_dic2[key]):
                    self.colorFlipCount += 1 # If the color is different after the update or delete we increment the color flip count
        self.colorDic = comp_dic2

    def get_colorFlipCount(self):
        # Getter for color flip count
        return self.colorFlipCount

#Color Flip Ends 