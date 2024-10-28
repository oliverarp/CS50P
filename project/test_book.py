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

import pytest
import datetime
from book import Book

def test_Book_minimum_meta(mocker):
    
    with pytest.raises(ValueError):
        book = Book()

    with pytest.raises(ValueError):
        book = Book(title="A Book")

    with mocker.patch('uuid.uuid4', return_value='12345678-1234-1234-1234-123456789abc'):
        book = Book(title="A Book", authors=["John Doe"])
    assert book.title == "A Book"
    assert len(book.authors) == 1
    assert book.authors[0] == "John Doe" 
    assert book.uuid == '12345678-1234-1234-1234-123456789abc'


def test_Book_isbn():
    
    # bare ISBN-13    
    book = Book( title="A Book", authors=["John Doe"], isbn="9786610326266")
    assert book.isbn == "9786610326266"

    # decorated ISBN-13
    book = Book( title="A Book", authors=["John Doe"], isbn="ISBN 979-10-90636-07-1")
    assert book.isbn == "9791090636071"

    # bare ISBN-10
    book = Book( title="A Book", authors=["John Doe"], isbn="0826497527")
    assert book.isbn == "0826497527"

    # decorated ISBN-10
    book = Book( title="A Book", authors=["John Doe"], isbn="ISBN 817525766-0" )
    assert book.isbn == "8175257660"

    # invalid ISBN: Too long for ISBN-13
    with pytest.raises(ValueError):
        book = Book(title="A Book", authors=["John Doe"], isbn="12345678901234")

    # Invalid ISBN: Too long for ISBN-10, too short for ISBN-13
    with pytest.raises(ValueError):
        book = Book(title="A Book", authors=["John Doe"], isbn="123456789012" )

    # Invalid ISBN: Too long for ISBN-10, too short for ISBN-13
    with pytest.raises(ValueError):
        book = Book(title="A Book", authors=["John Doe"], isbn="12345678901")

    # Invalid ISBN: Too short for ISBN-10 and ISBN-13
    with pytest.raises(ValueError):
        book = Book(title= "A Book", authors=["John Doe"], isbn="123456789")

    # Invalid ISBN: wrong checksum
    # valid isbn as reference
    book = Book( title="A Book", authors=["John Doe"], isbn="ISBN 979-10-90636-07-1")
    assert book.isbn == "9791090636071"
    # invalid isbn: changed last digit (checksum) of the valid isbn above
    with pytest.raises(ValueError):
        book = Book(title= "A Book", authors=["John Doe"], isbn="ISBN 979-10-90636-07-2")


def test_Book_publication_date():
    book = Book(title="A Book", authors=["John Doe"])
    assert book.publication_date == None

    book = Book(title="A Book", authors=["John Doe"], publication_date="1970-01-31")
    assert book.publication_date == datetime.date(1970, 1, 31)

    book = Book(title="A Book", authors=["John Doe"], publication_date="1970")
    assert book.publication_date == datetime.date(1970, 1, 1)

    book = Book(title="A Book", authors=["John Doe"], publication_date=datetime.date(1970, 5, 26))
    assert book.publication_date == datetime.date(1970, 5, 26)

    with pytest.raises(ValueError):
        book = Book(title="A Book", authors=["John Doe"], publication_date="1970-13-45")

    with pytest.raises(ValueError):
        book = Book(title="A Book", authors=["John Doe"], publication_date="cat")

    with pytest.raises(ValueError):
        book = Book(title="A Book", authors=["John Doe"], publication_date=42)


def test_Book_Authors():
    authors = [
        "Jane M. Doe",
        "Max Mustermann", 
        "Fred Nurk",
        "John Doe"
        ]
    
    book = Book(title="Book", authors=authors)
    assert book.authors[0] == "Jane M. Doe"
    assert book.authors[1] == "Max Mustermann"
    assert book.authors[2] == "Fred Nurk"
    assert book.authors[3] == "John Doe"

def test_Book_str_():
    # only title an author
    book = Book(title="A Book", authors=["John Doe"])
    assert str(book) == 'John Doe, "A Book"'



    # isbn title and publication year
    book = Book(title="A Book", authors=["John Doe"], isbn="9791090636071", publication_date="1970-01-31")
    assert str(book) == 'John Doe, "A Book" (1970), ISBN 979-10-90636-07-1'

    authors = [
        "Jane M. Doe",
        "Max Mustermann", 
        "Fred Nurk",
        "John Doe"
        ]

    # one author         
    book = Book(title="A Book", authors=authors[0:1], isbn="9791090636071", publication_date="1970-01-31")
    assert str(book) == 'Jane M. Doe, "A Book" (1970), ISBN 979-10-90636-07-1'

    # two authors
    book = Book(title="A Book", authors=authors[0:2], isbn="9791090636071", publication_date="1970-01-31")
    assert str(book) == 'Jane M. Doe, Max Mustermann, "A Book" (1970), ISBN 979-10-90636-07-1'

    # three authors
    book = Book(title="A Book", authors=authors[0:3], isbn="9791090636071", publication_date="1970-01-31")
    assert str(book) == 'Jane M. Doe, Max Mustermann, Fred Nurk, "A Book" (1970), ISBN 979-10-90636-07-1'

    # abbreviation of long author lists (>3)
    book = Book(title="A Book", authors=authors[0:4], isbn="9791090636071", publication_date="1970-01-31")
    assert str(book) == 'Jane M. Doe, Max Mustermann, Fred Nurk, et al., "A Book" (1970), ISBN 979-10-90636-07-1'


def test_Book_full_str():
    authors = [
        "Jane M. Doe",
        "Max Mustermann", 
        "Fred Nurk",
        "John Doe"
        ]

    book = Book(title="A Book", authors=authors, isbn="9791090636071", publication_date="1970-01-31")
    assert book.full_str() == 'Jane M. Doe, Max Mustermann, Fred Nurk, John Doe, "A Book" (1970-01-31), ISBN 979-10-90636-07-1'



def test_Book_eq_():
    # books are supposed to have different uuids --> not equal
    book1 = Book(title="A Book", authors=["John Doe"])
    book2 = Book(title="A Book", authors=["John Doe"])
    assert book1 != book2

    # the books have equal uuid, but different meta data --> equal
    book1 = Book(title="A Book", authors=["John Doe"], uuid='16fd2706-8baf-433b-82eb-8c7fada847da')
    book2 = Book(title="A Book [special edition]", authors=["John M. Doe"], uuid='16fd2706-8baf-433b-82eb-8c7fada847da')
    assert book1 == book2

    # Differently set uuid --> unequal
    book1 = Book(title="A Book", authors=["John Doe"], uuid='16fd2706-8baf-433b-82eb-8c7fada847da')
    book2 = Book(title="A Book", authors=["John Doe"], uuid='12345678-1234-1234-1234-123456789abc')
    assert book1 != book2


def test_Book_init_with_keywords():
    keyword_list = ["Cat", "Dog", "Cat"]
    book = Book(title="A Book", authors=["John Doe"], keywords = keyword_list)
    assert len(book.keywords) == 2 
    assert "Cat" in book.keywords
    assert "Dog" in book.keywords

    keyword_set = {"Cat", "Dog"}
    book = Book(title="A Book", authors=["John Doe"], keywords = keyword_set)
    assert len(book.keywords) == 2 
    assert "Cat" in book.keywords
    assert "Dog" in book.keywords


def test_Book_add_keyword():
    book = Book(title="A Book", authors=["John Doe"],)
    book.add_keyword("Cat")
    book.add_keyword("Cat", "Dog", "cat", " ")
    book.add_keyword()

    with pytest.raises(ValueError):
        book.add_keyword(42)

    assert len(book.keywords) == 3 
    assert "Cat" in book.keywords
    assert "Dog" in book.keywords
    assert "cat" in book.keywords


def test_Book_parse_date_str():
    assert Book._parse_date_str("2024-01-01") == (2024, 1, 1)
    assert Book._parse_date_str("2024") == (2024, 1, 1)
    assert Book._parse_date_str("cat") == False
    assert Book._parse_date_str("2024-1-01") == False
    assert Book._parse_date_str("2024-01-1") == False

    with pytest.raises(ValueError):
        Book._parse_date_str("2024-00-01")
        
    with pytest.raises(ValueError):
        Book._parse_date_str("2024-13-01")

    with pytest.raises(ValueError):
        Book._parse_date_str("2024-01-00")

    with pytest.raises(ValueError):
        Book._parse_date_str("2024-01-32")



def test_Book_meta(mocker):

    authors = [ "Jane M. Doe", "Max Mustermann"]

    keywords = ["Cat", "Dog"]

    # prvide uuid as argument at initialization
    book = Book(title="A book title", authors=authors, isbn="9791090636071", publication_date="1970-01-31", keywords=keywords, uuid='16fd2706-8baf-433b-82eb-8c7fada847da')
    
    assert book.meta == {'__type__': 'mybooks.Book', 'uuid': '16fd2706-8baf-433b-82eb-8c7fada847da', 'title': 'A book title', 'authors': ['Jane M. Doe', 'Max Mustermann'], 'publication_date': datetime.date(1970, 1, 31), 
                         'isbn': '9791090636071', 'keywords': {'Dog', 'Cat'}}

    # automatic creation of uuid, if not provided as argument
    with mocker.patch('uuid.uuid4', return_value='12345678-1234-1234-1234-123456789abc'):
        book = Book(title="A book title", authors=authors, isbn="9791090636071", publication_date="1970-01-31", keywords=keywords)    
    
    assert book.meta == {'__type__': 'mybooks.Book', 'uuid': '12345678-1234-1234-1234-123456789abc', 'title': 'A book title', 'authors': ['Jane M. Doe', 'Max Mustermann'], 'publication_date': datetime.date(1970, 1, 31), 
                         'isbn': '9791090636071', 'keywords': {'Dog', 'Cat'}}


def test_Book_as_json():
    authors = [ "Jane M. Doe"]

    keywords = ["Cat"]

    book = Book(title="A book title", authors=authors, isbn="9791090636071", publication_date="1970-01-31", keywords=keywords, uuid='16fd2706-8baf-433b-82eb-8c7fada847da')    
    
    assert book.as_json == '{"__type__": "mybooks.Book", "uuid": "16fd2706-8baf-433b-82eb-8c7fada847da", "title": "A book title", "authors": ["Jane M. Doe"], "publication_date": "1970-01-31", "isbn": "9791090636071", "keywords": ["Cat"]}'
         



def test_Book_from_json():
    json_str = '{"title": "A book title", "authors": ["Jane M. Doe", "John Doe"], "publication_date": "1970-01-31", "isbn": "9791090636071", "keywords": ["Cat", "Dog"]}'    

    book = Book.from_json(json_str)
    assert book.title == "A book title"
    assert "Jane M. Doe" in book.authors
    assert "John Doe" in book.authors
    assert book.publication_date == datetime.date(1970, 1, 31)
    assert book.isbn == "9791090636071"
    assert "Cat" in book.keywords
    assert "Dog" in book.keywords


def test_Book_meta_from_isbn(mocker):
        isbn = "979-10906-36071"
        with mocker.patch('isbnlib.meta', return_value={'Title': "A Title", 'Authors': ['John Doe', 'Jane Doe'], 'Year': 1970}):
            meta = Book._meta_from_isbn(isbn)

        assert meta['publication_date'] == datetime.date(1970, 1, 1)
        assert meta['title'] == "A Title"
        assert 'John Doe' in meta['authors']
        assert 'Jane Doe' in meta['authors']
        assert meta['isbn'] == "9791090636071"


def test_Book_from_isbn(mocker):
        isbn = "979-10906-36071"

        meta = {'title': 'A book title', 'authors': ['John Doe', 'Jane Doe'], 'publication_date': datetime.date(1970, 1, 31), 
                            'isbn': '9791090636071', 'keywords': {'Dog', 'Cat'}}

        with mocker.patch('book.Book._meta_from_isbn', return_value=meta):
            book = Book.from_isbn(isbn)

        assert book.title == "A book title"
        assert 'John Doe' in book.authors
        assert 'Jane Doe' in book.authors
        assert book.publication_date == datetime.date(1970, 1, 31)
        assert book.isbn == '9791090636071'
        assert 'Cat' in book.keywords
        assert 'Dog' in book.keywords


def test_Book_update():
    authors = [ "Jane M. Doe", "Max Mustermann"]
    keywords = ["Cat", "Dog"]
    book = Book(title="A book title", authors=authors, isbn="9791090636071", publication_date="1970-01-31", keywords=keywords, uuid='16fd2706-8baf-433b-82eb-8c7fada847da')
    assert book.meta == {'__type__': 'mybooks.Book', 'uuid': '16fd2706-8baf-433b-82eb-8c7fada847da', 'title': 'A book title', 'authors': ['Jane M. Doe', 'Max Mustermann'], 'publication_date': datetime.date(1970, 1, 31), 
                         'isbn': '9791090636071', 'keywords': {'Dog', 'Cat'}}

    # refuse to change UUID
    with pytest.raises(ValueError):
        book.update(uuid="12345678-1234-1234-1234-123456789abc")

    update_count = book.update(title="A modified title", authors=["Author A", "Author B", "Author C"], isbn="9786610326266", publication_date="1990-01-31", keywords=["Apple", "Banana"])
    assert update_count == 8
    assert book.meta == {'__type__': 'mybooks.Book', 'uuid': '16fd2706-8baf-433b-82eb-8c7fada847da', 'title': 'A modified title', 'authors': ['Author A', 'Author B', 'Author C'], 'publication_date': datetime.date(1990, 1, 31), 
                         'isbn': '9786610326266', 'keywords': {'Apple', 'Banana'}}
