from redBlackTree import BookNode,RedBlackTree

# Write to the output file Start

def write_to_file(content):
    output_file.write(content+'\n') #Writing the content into output file

# Write to the output file End

#Operations Start

def operations(operation, info_list):
    # Function to call various library operations
    if operation == 'InsertBook':
        library.insert(BookNode(info_list[0],info_list[1],info_list[2],info_list[3]))

    elif operation == 'DeleteBook':
        reserveList = library.delete(info_list[0])
        printDeleteBook(info_list[0],reserveList)

    elif operation == 'PrintBook':
        bookData = library.search(info_list[0])
        printBook(bookData,info_list[0])

    elif operation == 'PrintBooks':
        range_book_nodes = library.range_books(info_list[0],info_list[1])
        if (len(range_book_nodes)==0):
            write_to_file('No book is in the range ({}, {})\n'.format(info_list[0],info_list[1]))
        
        else:
            for bookNode in range_book_nodes:
                printBook(bookNode)
    
    elif operation == 'FindClosestBook':
        closest_smaller_node, closest_larger_node = library.closest_keys_with_min_difference(info_list[0])
        printClosestBooks(info_list[0],closest_smaller_node, closest_larger_node)

    elif operation == 'BorrowBook':
        book_id, reserve_flag, patron_id = library.BorrowBook(info_list[0],info_list[1],info_list[2])
        printBorrowBook(book_id, reserve_flag, patron_id)

    elif operation == 'ReturnBook':
        book_id, nextPatron = library.ReturnBook(info_list[0],info_list[1])
        currPatron = info_list[0]
        printReturnBook(book_id, currPatron, nextPatron)

#Operations End

#Print Book Start

def printBook(bookNode,bookID=None):
    #Helper Function to print Book in Library
    if bookNode :
        write_to_file("BookID = {}".format(bookNode.book.bookID))
        write_to_file("Title = {}".format(bookNode.book.title))
        write_to_file("Author = {}".format(bookNode.book.author))
        write_to_file("Availability = {}".format(bookNode.book.availability))
        write_to_file("BorrowedBy = {}".format(bookNode.book.borrowedBy))
        write_to_file("Reservations = {}\n".format(bookNode.book.reservations))
    else:
        write_to_file('Book {} not found in the library\n'.format(bookID))



#Print Book Ends

#Print Delete Book Start

def printDeleteBook(bookID, reserveList):
    #Helper Function to Delete Book from Library
    if reserveList is None:
        write_to_file('Book {} is not present in the library to delete\n'.format(bookID))
    else:
        if(len(reserveList)==0):
            write_to_file('Book {} is no longer available\n'.format(bookID))
        elif(len(reserveList)==1):
            write_to_file('Book {} is no longer available. Reservation made by Patron {} has been cancelled!\n'.format(bookID,reserveList[0]))
        else:
            reserveList = [str(patron) for patron in reserveList]
            patrons_str = ', '.join(reserveList) # Converting the reserveList into string
            write_to_file('Book {} is no longer available. Reservations made by Patrons {} have been cancelled!\n'.format(bookID, patrons_str))

#Print Delete Book End

#Print Closest Book Start

def printClosestBooks(key, closest_smaller_node, closest_larger_node):
    # Helper Function to print the closest book for the given book
    if closest_smaller_node == None and closest_larger_node == None:
        write_to_file('Closest Book does not exist\n')

    elif closest_smaller_node == None:
        printBook(closest_larger_node)

    elif closest_larger_node == None:
        printBook(closest_smaller_node)

    else:

        smaller_key = closest_smaller_node.key
        larger_key = closest_larger_node.key

        if (abs(key-smaller_key) < abs(key-larger_key)):
            printBook(closest_smaller_node)

        elif (abs(key-smaller_key) > abs(key-larger_key)):
            printBook(closest_larger_node)
        
        else:
            printBook(closest_smaller_node)
            printBook(closest_larger_node)

#Print Closest Book End

#Print Borrow Book Start

def printBorrowBook(book_id, reserve_flag, patron_id):
    # Helper Function to Borrow the book and reserve the book if it is not available
    if(book_id == None):
        write_to_file('Book {} is not their in library\n'.format(book_id))

    else:
        if reserve_flag == False:
            write_to_file('Book {} Borrowed by Patron {}\n'.format(book_id,patron_id))
        else:
            write_to_file('Book {} Reserved by Patron {}\n'.format(book_id,patron_id))


#Print Borrow Book End

#Print Return Book Start

def printReturnBook(book_id, currPatron, nextPatron):
    #Helper Function to Return the book
    write_to_file('Book {} Returned by Patron {}\n'.format(book_id, currPatron))
    if nextPatron is not None:
        write_to_file('Book {} Alloted to Patron {}\n'.format(book_id, nextPatron))


#Print Return Book End


# Function to call all the library opeartions start

def helper_main(input_file_name, output_file_name):
    # Helper Main function to Create the RedBlackTree and output_file object
    global library #declaring library object as global
    library = RedBlackTree()

    global output_file #declaring output_file as global
    output_file = open(output_file_name, 'w') 

    try:
        with open(input_file_name, "r") as file: #opening the file in read only mode
            for line in file:
                operation = line.split('(')[0]  # Extract operation before '('
                operation=operation.lstrip() #removing white spaces at the start of the line
                if operation == 'Quit':
                    write_to_file('Program Terminated!!')
                    break
                elif operation == 'ColorFlipCount':
                    colorCount = library.get_colorFlipCount()
                    write_to_file('Color Flip Count: {}\n'.format(colorCount))     
                else:
                    info = line.split('(')[1].split(')')[0]  # Extracting information within '(' and before ')'
                    info_list = []
                    for elem in info.split(','):
                        elem = elem.strip().strip('"') # Split info into list removing spaces and quotes
                        # Trying to convert to integer if not enclosed in quotes
                        try:
                            elem = int(elem)
                        except ValueError:
                            pass  # It remains as a string if it can't be converted to an integer
                        info_list.append(elem) 
                    operations(operation, info_list)

    except FileNotFoundError:
        print("File not found or path is incorrect.")

    output_file.close()

# Function to call all the library opeartions end