# MyBooks - A simple book library software
# Copyright (C) 2024  Oliver Arp
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from book_library import BookLibraryJSON
from book import Book

import argparse
import os.path
import sys
import isbnlib

def handle_cli_command_init(args) -> bool:
    '''
    Create an empty library
    '''
    if os.path.isfile(args.file) and not args.force: 
        answer = input(f"Do you really want to overwrite existing file {args.file}? [Yes/No]: ")
        if answer != "Yes":
            print("Leaving existing file unchanged!")
            return False

    lib = BookLibraryJSON()
    lib.write_to_json_file(args.file)
    print("Initialized empty database.")

    return True


def handle_cli_command_import(args):
    '''
    Import data from a file
    Returns number of imported books
    '''

    if not os.path.isfile(args.file):
        print("Cannot find library file. Use init command to create an empty file.")
        return False

    if not (args.json_file or args.isbn_file):
        raise ValueError( 'Either --json-file or --isbn-file must be specified!')

    if args.json_file and args.isbn_file:
        raise ValueError( 'Options --json-file and --isbn-file must nor be specified simultaneously. Aborting.')
    
    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)

    # Import JSON file
    if args.json_file:
        import_lib = BookLibraryJSON()

        print(f"Importing file {args.json_file} ...")
        import_lib.read_from_json_file(args.json_file)

        books_for_import = 0
        books_imported = 0
        for book in import_lib:
            books_for_import += 1
            if lib.add(book):
                books_imported += 1
            

        print(f"{books_imported} of {books_for_import} books imported ({books_for_import-books_imported} duplicates).")
        lib.write_to_json_file(args.file)
        
        return books_imported

    # Import ISBN file
    elif args.isbn_file:
        print(f"Importing file {args.isbn_file} ...")
        file = open(args.isbn_file, 'rt')
        
        valid_isbn = 0
        books_imported = 0
        lines_skipped = 0
        for line in file:
            isbn = isbnlib.get_canonical_isbn(line.strip())
            if isbn:
                valid_isbn += 1
                if not lib.find(isbn=isbn):
                    book = Book.from_isbn(isbn)
                    if book and lib.add(book):
                        print(f'Imported ISBN {isbn}.') 
                        books_imported += 1
                    else:
                        print(f'Could not fetch metadata for ISBN {isbn}.')    
                else:
                    print(f'Ignoring ISBN {isbn} (already in library).') 
            else:
                lines_skipped += 1

        file.close()

        print(f"{books_imported} of {valid_isbn} books imported ({valid_isbn-books_imported} duplicates, {lines_skipped} lines skipped).")
        lib.write_to_json_file(args.file)

        return books_imported


def handle_cli_command_list(args):
    '''
    List the contents of the library
    '''

    if not os.path.isfile(args.file):
        print("Cannot find library file. Use init command to create an empty file.")
        return False

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)

    find_args = {}

    if args.title:
        find_args["title"] = args.title

    if args.isbn:
        find_args["isbn"] = args.isbn
    
    if args.keywords:
        find_args["keywords"] = args.keywords

    if args.authors:
        find_args["authors"] = args.authors

    if args.match_all:
        find_args["match_all"] = True

    if args.published_after:
        find_args["published_after"] = args.published_after

    if args.published_before:
        find_args["published_before"] = args.published_before

    if args.uuid:
        find_args["uuid"] = args.uuid

    try:
        books = sorted(lib.find(**find_args), key=lambda b: f"{b.publication_date}", reverse=True)
    except ValueError as e:
        print(e)
        return 0


    for index, book in enumerate(books):
            
            book_str = ""

            if not args.bare:
                book_str += f"[{index+1}] "
                
            if args.show_all:
                book_str += f" {book.full_str()}"
            else:
                book_str += f" {str(book)}"

            if args.show_keywords or args.show_all:
                book_str += f" {str(sorted(book.keywords))}"

            if args.show_uuid or args.show_all:
                book_str += f" <{book.uuid}>"

            print(book_str)
            #print(book.meta) 
            #print(book.as_json) 

    return len(books)

def handle_cli_command_add(args) -> bool:
    '''
    Add a book to the library
    '''

    if not os.path.isfile(args.file):
        print("Cannot find library file. Use init command to create an empty file.")
        return False


    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)

    if args.fetch_meta: 
        if not args.isbn:
            raise ValueError("ISBN must be specified!")

        if args.title or args.authors or args.publication_date:
            print("Warning: Arguments --title, --authors and --publication-date will be ignored!")


        book = Book.from_isbn(args.isbn)
        if args.keywords:
            book.add_keyword(*(args.keywords))

        
    else:            
        meta = dict()
        if args.title:
            meta["title"] = args.title
        if args.isbn:
            meta["isbn"] = args.isbn
        if args.authors:
            meta["authors"] = args.authors
        if args.keywords:
            meta["keywords"] = args.keywords
        if args.publication_date:
            meta["publication_date"] = args.publication_date

        #print(meta)
        book = Book.from_meta(meta)


    if lib.add(book):
        print("Added: " + str(book))
        lib.write_to_json_file(args.file)    
        return True
    else:
        return False


def handle_cli_command_update(args):
    '''
    Modify the meta data of an existing book in the library
    '''

    if not os.path.isfile(args.file):
        print("Cannot find library file. Use init command to create an empty file.")
        return False

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)


    if not args.uuid:
        raise ValueError("UUID must be specified!")
        
    else:            
        meta = dict()
        if args.title:
            meta["title"] = args.title
        if args.isbn:
            meta["isbn"] = args.isbn
        if args.authors:
            meta["authors"] = args.authors
        if args.keywords:
            meta["keywords"] = args.keywords
        if args.publication_date:
            meta["publication_date"] = args.publication_date


    if lib.update(args.uuid, **meta):
        print("Updated: " + args.uuid)
        lib.write_to_json_file(args.file)    
        return True
    else:
        return False



def handle_cli_command_delete(args) -> bool:
    '''
    Delete a book from the library
    '''

    if not os.path.isfile(args.file):
        print("Cannot find library file. Use init command to create an empty file.")
        return False


    if not args.uuid:
        raise ValueError("UUID must be specified!")

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)

    if lib.remove(args.uuid):
        print(f"Deleted book with UUID {args.uuid}" )
        lib.write_to_json_file(args.file)    
        return True
    else:
        return False


def parse_args(argv):
    '''
    Define CLI and parse command line arguments
    Expects sys.argv[1:] as argument
    '''
  # Configure CLI
    parser = argparse.ArgumentParser(description = "A simple book library software")
    parser.add_argument("--file", type=str, default="mybooks.json", help="Library file")    
    subparsers = parser.add_subparsers(dest="command", help="sub-command help", required=True)
    parser_init = subparsers.add_parser("init", help="Initialize empty library")
    parser_init.add_argument("--force", action='store_true', help="Force overwriting exisiting database")
    parser_add = subparsers.add_parser("add", help="Add a book to the library")
    parser_add.add_argument("--title", type=str, help="Title of the book")
    parser_add.add_argument("--isbn", type=str, help="ISBN number")
    parser_add.add_argument("--authors", type=str, metavar="AUTHOR", nargs = "+", help="Space-separated list of author names")
    parser_add.add_argument("--keywords", type=str, metavar="KEYWORD", nargs = "+", help="Space-separated list of keywords")
    parser_add.add_argument("--publication-date", metavar="YYYY-MM-DD",type=str, help="Publication date in ISO format (YYYY-MM-DD)")
    parser_add.add_argument("--fetch-meta", action='store_true', help="Fetch meta data based on ISBN from online service.")
    parser_remove = subparsers.add_parser("delete", help="Delete a book from the library")
    parser_remove.add_argument("--uuid", required=True, type=str, help="UUID of book in library")
    parser_list = subparsers.add_parser("list", help="List library contents")
    parser_list.add_argument("--title", type=str, help="Title of the book")
    parser_list.add_argument("--isbn", type=str, help="ISBN number")
    parser_list.add_argument("--keywords", type=str, metavar="KEYWORD", nargs = "+", help="Space-separated list of keywords")
    parser_list.add_argument("--authors", type=str, metavar="AUTHOR", nargs = "+", help="Space-separated list of author names")
    parser_list.add_argument("--show-all", action='store_true', help="Show all metadata of the book")
    parser_list.add_argument("--match-all", action='store_true', help="Match all of given authors or keywords")
    parser_list.add_argument("--published-after", metavar="YYYY-MM-DD",type=str, help="Date in ISO format (YYYY-MM-DD)")
    parser_list.add_argument("--published-before", metavar="YYYY-MM-DD",type=str, help="Date in ISO format (YYYY-MM-DD)")
    parser_list.add_argument("--show-keywords", action='store_true', help="Show keywords")
    parser_list.add_argument("--uuid", type=str, help="UUID of book in library")
    parser_list.add_argument("--show-uuid", action='store_true', help="Show UUID of book in library")
    parser_list.add_argument("--bare", action='store_true', help="Disable enumeration")
    parser_update = subparsers.add_parser("update", help="Modify book in library")
    parser_update.add_argument("--uuid", type=str, required=True, help="UUID of book in library (required)")
    parser_update.add_argument("--title", type=str, help="Set new title")
    parser_update.add_argument("--isbn", type=str, help="Set new ISBN number")
    parser_update.add_argument("--authors", type=str, metavar="AUTHOR", nargs = "+", help="Replace authors by space-separated list of author names")
    parser_update.add_argument("--keywords", type=str, metavar="KEYWORD", nargs = "+", help="Replace keywords by space-separated list of new keywords")
    parser_update.add_argument("--publication-date", metavar="YYYY-MM-DD",type=str, help="Set publication date in ISO format (YYYY-MM-DD)")
    parser_import = subparsers.add_parser("import", help="Import data")
    parser_import.add_argument("--json-file", type=str, help="JSON file")
    parser_import.add_argument("--isbn-file", type=str, help="Text file with one isbn per line")

    return parser.parse_args(argv)


if __name__ == "__main__":
    
    # Parse command line arguments
    args = parse_args(sys.argv[1:])
    
    # Handle command "init"
    if args.command == "init":
        if handle_cli_command_init(args):
            sys.exit(0)
        else:
            sys.exit(1)

    # Handle command "import"
    elif args.command == "import":
        try:
            handle_cli_command_import(args)
        except ValueError as err:
            print(err)
        sys.exit(0)

    # Handle command "list"
    elif args.command == "list":
        handle_cli_command_list(args)
        sys.exit(0)

    # Handle command "add"
    elif args.command == "add":
        handle_cli_command_add(args)
        sys.exit(0)

    # Handle command "update"        
    elif args.command == "update":
        handle_cli_command_update(args)
        sys.exit(0)        
    
    # Handle command "delete"
    elif args.command == "delete":
        handle_cli_command_delete(args)
        sys.exit(0)
    else:
        raise ValueError("Invalid command!")
    


