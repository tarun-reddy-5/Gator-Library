from helper import helper_main
import sys

if __name__ == '__main__':
    input_file = sys.argv[1]
    input_file_name, extension = input_file.split('.')
    if extension == 'txt':
        output_file_name = input_file_name + '_output_file.'+ 'txt'
        helper_main(input_file, output_file_name)
    else:
        print("File not found or path is incorrect.")
