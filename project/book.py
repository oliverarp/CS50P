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

import uuid
import datetime
import isbnlib
import re
import json

# BOOK_META_SERVICE="dnb"

class BookJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if isinstance(obj, Book):
            return obj._meta
        
        return json.JSONEncoder.default(self, obj)

class BookJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
    
        if dct.get("__type__") == "mybooks.Book":
            return Book.from_meta(dct)
        
        return dct 

class Book:
    def __init__(self, **kwargs) -> None:

        self._meta = {'__type__': 'mybooks.Book'}
        
        if kwargs.get('uuid'):
            self._meta['uuid'] = kwargs['uuid']
        else:
            self._meta['uuid'] = str(uuid.uuid4())

        if not ( ("title" in kwargs) and ("authors" in kwargs) and (len(kwargs['authors'])>0) ):
            raise ValueError("Title and authors are requred!")

        self.update(**kwargs)
    

    def update(self, **kwargs) -> int:
        updates_performed = 0

        if kwargs.get("uuid") and (kwargs["uuid"] != self._meta['uuid']):
            raise ValueError("Changing the UUID is not allowed!")
        
        if kwargs.get("title"):
            if not isinstance(kwargs["title"], str):
                raise ValueError("Title must be a str!")

            self._meta['title'] = kwargs["title"]
            updates_performed += 1

        if kwargs.get("authors"):
            if not isinstance(kwargs["authors"], list):
                raise ValueError("List of authors expected!")
            
            # ensure that earch element of authors is a str
            for author in kwargs["authors"]:
                if not isinstance(author, str):
                    raise ValueError("Author must be a str!")
        
            self._meta['authors'] = kwargs["authors"]
            updates_performed += len(kwargs["authors"])


        if kwargs.get("publication_date"):
            if isinstance(kwargs["publication_date"], datetime.date):
                self._meta['publication_date'] = kwargs["publication_date"]
                updates_performed += 1
            
            elif isinstance(kwargs["publication_date"], str):
                if d := Book._parse_date_str(kwargs["publication_date"]):
                    self._meta['publication_date'] = datetime.date(d[0],d[1],d[2])
                    updates_performed += 1
                else:
                    raise ValueError("Invalid publication date!")
            else:
                raise ValueError("Publication date must be either datetime.date or str!")
        
        
        if kwargs.get("isbn"):
            isbn = isbnlib.canonical(kwargs["isbn"])
            if isbnlib.notisbn(isbn):
                raise ValueError(f'Invalid ISBN: {kwargs["isbn"]}')
            
            self._meta['isbn'] = isbn
            updates_performed += 1


        if kwargs.get("keywords"):
            if (isinstance(kwargs["keywords"], set) or isinstance(kwargs["keywords"], list)):
                self._meta['keywords'] = set()
                for keyword in kwargs["keywords"]:           
                    self.add_keyword(keyword)
                    updates_performed += 1
            else:
                raise ValueError("Keywords must be either set or list!")
        
        return updates_performed
    
    def __str__(self) -> str:

        book_str = ""

        if not self.authors:
            raise ValueError("No author specified!")
        
        elif len(self.authors)<=3:
            book_str += ', '.join(self.authors) + ", "
        else:
            book_str += ', '.join(self.authors[0:3]) + ", et al., "

        if not self.title:
            raise ValueError("No author specified!")
        
        book_str += f'"{self.title}"'


        if self.publication_date:
            book_str += f' ({self.publication_date.year})'
        
        if self.isbn:
            book_str += f', ISBN {self.isbn_str}'
        
        return book_str


    def full_str(self) -> str:

        book_str = ""

        if not self.authors:
            raise ValueError("No author specified!")
        
        book_str += ', '.join(self.authors) + ", "

        if not self.title:
            raise ValueError("No author specified!")
        
        book_str += f'"{self.title}"'

        if self.publication_date:
            book_str += f' ({self.publication_date.isoformat()})'
        
        if self.isbn:
            book_str += f', ISBN {self.isbn_str}'
        
        return book_str



    @staticmethod
    def _parse_date_str(date_str):
        if not isinstance(date_str, str):
            return False
        
        year = None
        month = 1
        day = 1

        if m:=re.match("^(\\d{4})-(\\d{2})-(\\d{2})$", date_str.strip()):
            year = int(m.group(1))
            month = int(m.group(2))
            if month<1 or month>12:
                raise ValueError("Invalid month!")
            day = int(m.group(3))
            if day<1 or day>31:
                raise ValueError("Invalid day!")

        elif m:=re.match("^(\\d{4})$", date_str.strip()):
            year = int(m.group(1))

        if year:
            return (year, month, day)
        
        else:
            return False

    @classmethod
    def _meta_from_isbn(cls, isbn: str) -> dict:
        
        meta = dict()
        
        isbn = isbnlib.canonical(isbn)

        try:
            isbn_meta = isbnlib.meta(isbn)    

            if isbn_meta and isinstance(isbn_meta, dict):
                if "Title" in isbn_meta:
                    meta['title'] = isbn_meta['Title']
                    
                if "Authors" in isbn_meta:
                    meta['authors'] = isbn_meta["Authors"]

                if "Year" in isbn_meta:
                    meta['publication_date'] = datetime.date(int(isbn_meta["Year"]), 1, 1)
                
                meta["isbn"] = isbn

                return meta
            
        except isbnlib.NotValidISBNError:
            raise ValueError('Invalid ISBN!')
        
        return None
    
    @classmethod
    def from_isbn(cls, isbn):
        if meta := Book._meta_from_isbn(isbn):
            if book := Book.from_meta(meta):
                return book

        return None

    def fetch_meta(self) -> bool:
        if meta := Book._meta_from_isbn(self.isbn):
            for key in meta:
                self._meta[key] = meta[key]
            return True

        return False
    


    @classmethod
    def from_json(cls, json_str):
        return Book.from_meta(json.loads(json_str))
        

    @classmethod
    def from_meta(cls, meta):
        return Book(**meta)
        

    @property
    def meta(self) -> dict:
        return self._meta

    @property
    def uuid(self) -> str:
        return self._meta['uuid']


    @property
    def as_json(self):
        meta = self._meta
        return json.dumps(self._meta, cls=BookJSONEncoder)

    @property
    def isbn(self):
        return self._meta.get('isbn')

    @property
    def isbn_str(self):
        isbn = self._meta.get('isbn')
        if isbn:
            return isbnlib.mask(isbn)
        else:
            False

    @property
    def title(self):
        return self._meta.get('title')

    @property
    def publication_date(self) -> datetime.date:
        return self._meta.get('publication_date')


    @property
    def authors(self):
        return self._meta.get('authors')
    

    @property
    def keywords(self):
        if not "keywords" in self._meta:
            return set()
        
        return self._meta.get('keywords')

    def __eq__(self, other):
        if isinstance(other, Book):
            if not (self.uuid and other.uuid):
                raise ValueError('Undefined UUID!')    
            
            return self.uuid == other.uuid
        else:        
            return False

    def __hash__(self):
        if self.uuid:
            return hash(self.uuid)
        else:
            raise ValueError('Undefined UUID!')


    def add_keyword(self, *args):
        
        for keyword in args:
            if not isinstance(keyword, str):
                raise ValueError("Keyword must be a string!")
           
            keyword = keyword.strip()
            if keyword:
                if not "keywords" in self._meta:
                    self._meta['keywords'] = set()

                self._meta['keywords'].add(keyword)


 