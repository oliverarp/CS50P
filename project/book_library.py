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

from book import Book, BookJSONEncoder, BookJSONDecoder
import json
import isbnlib
import fnmatch
import datetime


class BookLibraryJSON:
    def __init__(self) -> None:
        
        self._books= set() # empty set

    def add(self, book) -> bool:
        """ Adds book to libary
            Returns 
                True if successfully added
                False if book is not addedto library because, already in library, 
                    or if another book in l,ibrary has an identical ISBN
        """        
        if not isinstance( book, Book):
            raise ValueError("Only Books allowed!")
        
        if book in self._books:
            return False

        # Don't add if isbn already in library
        if book.isbn and len(self.find( isbn=book.isbn ))>0:
            return False
        
        self._books.add(book)

        return True


    def find(self, **kwargs) -> list:
        """ Find books based on their meta data
            Returns all books if no argument is given 
        """

        if not all( arg in ["uuid", "title", "isbn", "authors", "keywords", "match_all", "published_after", "published_before"] for arg in kwargs):
            raise ValueError("Unsupported argument for find()!")

        results = self._books


        if kwargs.get('uuid'):
            results = filter(lambda b: fnmatch.fnmatch(b.uuid, kwargs["uuid"]), results)


        if kwargs.get('title'):
            results = filter(lambda b: fnmatch.fnmatch(b.title, kwargs["title"]), results)


        if kwargs.get('isbn'):
            isbn = isbnlib.canonical(kwargs["isbn"])
            results = filter(lambda b: b.isbn == isbn, results)


        if kwargs.get('authors'):
            if kwargs.get('match_all') and kwargs['match_all']==True:
                results = filter(lambda b: all(fnmatch.filter(b.authors, author) for author in kwargs["authors"]) , results)
            else:
                results = filter(lambda b: any(fnmatch.filter(b.authors, author) for author in kwargs["authors"]) , results)


        if kwargs.get('keywords'):
            if kwargs.get('match_all') and kwargs['match_all']==True:
                results = filter(lambda b: all(fnmatch.filter(b.keywords, keyword) for keyword in kwargs["keywords"]) , results)
            else:
                results = filter(lambda b: any(fnmatch.filter(b.keywords, keyword) for keyword in kwargs["keywords"]) , results)


        if kwargs.get('published_after'):
            adate = datetime.date.fromisoformat(kwargs['published_after'])
            results = filter(lambda b: (b.publication_date and (b.publication_date > adate)), results)


        if kwargs.get('published_before'):
            bdate = datetime.date.fromisoformat(kwargs['published_before'])
            results = filter(lambda b: (b.publication_date and (b.publication_date < bdate)), results)


        return list(results)

    def update(self, uuid: str, **kwargs) -> int:
        """ Change meta data of a book identified by its UUID in the library
            Note: The UUID of a book cannot be changed.
            Returns Number of changed properties if book has been updated
        """

        if not uuid or (not isinstance(uuid, str)):
            raise ValueError("BookLibraryJSON.update(): Valid UUID required!")
        
        res = self.find(uuid=uuid)
        if len(res)<1:
            raise ValueError(f"BookLibraryJSON.update(): Cannot find book with UUID {uuid} in library!")

        if len(res)>1:
            raise ValueError(f"BookLibraryJSON.update(): Found multiple books with UUID {uuid} in library!")

        for arg in kwargs:
            if not (arg in ["title", "isbn", "authors", "keywords", "publication_date", "isbn"]):
                raise ValueError(f'BookLibraryJSON.update(): Unsupported argument "{arg}"!')

        if not isinstance( res[0], Book):
            raise ValueError(f"BookLibraryJSON.update(): Illegal object found in library!")

        return res[0].update(**kwargs)


    
    def remove(self, uuid: str) -> bool:
        ''' 
        Remove a book from the library
        Returns True if book has been removed
        Returns False if book was not in library
        '''

        if not uuid or (not isinstance(uuid, str)):
            raise ValueError("BookLibraryJSON.remove(): Valid UUID required!")
        
        res = self.find(uuid=uuid)
        if len(res)<1:
            return False

        if len(res)>1:
            raise ValueError(f"BookLibraryJSON.remove(): Found multiple books with UUID {uuid} in library!")

        if not isinstance( res[0], Book):
            raise ValueError(f"BookLibraryJSON.remove(): Illegal object found in library!")


        self._books.remove(res[0])
        
        return True



    def read_from_json_file(self, filename):
        f = open(filename, 'rt',encoding="utf-8")
        self._books = set(json.load(f, cls=BookJSONDecoder))
        

    def write_to_json_file(self, filename):
        f = open(filename, 'wt',encoding="utf-8")
        json.dump(self._books, f, cls=BookJSONEncoder, indent=4)


    def __iter__(self):
        return iter(self._books)

    def __len__(self):
        return len(self._books)


    @property
    def books(self):
        return self._books
