# Gator-Library
Gator Library is a sophisticated library management system that employs Red-Black tree and Binary Min Heap data structures for efficiently managing its books, patrons, and borrowing operations.

# Overview
1. The gatorLibrary project is a sophisticated library management system developed in Python.
2.  It offers an array of functionalities for efficiently managing its books, patrons, and borrowing operations.
3.  The system is structured into multiple modules, each responsible for distinct aspects of the library's operations.
4.  The system employs a Red-Black tree data structure to guarantee effective book management.
5.  Using Binary Min-heaps as a data structure, a priority-queue method can be implemented to manage book reservations if a book is not currently available for borrowing.
6.  Every book will have a min-heap to record readers' reservations.

# Execution
#### 1. Python Installation:<br/>
Ensure you have Python installed on your system.
#### 2. Download the Source Code:<br/>
Obtain the gatorLibrary source code files.
#### 3. Navigate to the Directory:<br/>
Open a terminal or command prompt.
Use the `cd` command to navigate to the directory where the `gatorLibrary` files
are located.
#### 4. Input File Preparation:<br/>
Prepare an input file (`input_file.txt`) that contains the commands and data to perform library operations.
#### 5. Execute the Script:<br/>
Run the `gatorLibrary.py` script by typing the following command in the terminal:<br/>
##### python3 gatorLibrary.py test1.txt<br/>
Replace `test1.txt` with the actual name of your input file and python3 with your python version.
#### 6. Operation Execution:<br/>
The script will interpret the commands from the input file and execute the corresponding library operations.<br/>
Operations include inserting books, deleting books, searching for books, borrowing/returning books, and more.
#### 7. Output File Generation:<br/>
The script will generate an output text file containing the results of the executed operations in the same directory.
#### 8. Review Results:<br/>
Open the generated output file to review the results of the performed operations. This file will contain information regarding the success or details of each operation.<br/>
If the directory contains the input files with the same name, the output file is overwritten based on your running input file.

# Summary
1. The gatorLibrary project offers a robust and versatile library management system, leveraging the efficiency of the Red-Black Tree data structure and Binary Min Heap for managing book reservations.
2. The tree's balanced nature allows for quick searches, aiding in finding books by their unique identifiers (IDs). This is crucial in library environments where swift book retrieval is essential.
3. The Min Heap structure allows for constant-time extraction of the patron with the highest priority, ensuring swift allocation of books to waiting patrons.
