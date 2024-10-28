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
from book_library import BookLibraryJSON
from book import Book
import datetime

@pytest.fixture
def sample_library():
    lib = BookLibraryJSON()
    lib.read_from_json_file("sample_library.json")
    return lib

def test_BookLibraryJSON_init(sample_library):
    # create empty library
    lib = BookLibraryJSON()
    assert len(lib.books) == 0

    # check also sample_library
    assert len(sample_library.books) == 20



def test_BookLibraryJSON_len_(sample_library):
    assert len(sample_library) == 20

def test_BookLibraryJSON_iter_(sample_library):
    
    book_count = 0 
    for book in sample_library:
        assert isinstance(book, Book)
        book_count += 1

    assert book_count == len(sample_library)


def test_BookLibraryJSON_add(sample_library):
    sample_library.add(Book(title="Added book", authors=["John Doe"]))
    assert len(sample_library.books) == 21
    


def test_BookLibraryJSON_find(sample_library):
    
    # find without arguments shall return all books
    res = sample_library.find()
    assert len(res) == 20


    # find title
    res = sample_library.find(uuid="ff85c452-def5-4e5c-adde-ff3798766812")
    assert len(res) == 1

    # find title
    res = sample_library.find(title="De revolutionibus orbium coelestium")
    assert len(res) == 1

    # find title with wildcards
    res = sample_library.find(title="*revolutionibus*")
    assert len(res) == 1

    # find author
    res = sample_library.find(authors=['Nicolaus Copernicus'])
    assert len(res) == 1

    # find multiple authors
    res = sample_library.find(authors=['Quincy Brown', 'John Doe'])
    assert len(res) == 2

    # require multiple authors
    res = sample_library.find(authors=['Quincy Brown', 'John Doe'], match_all=True)
    assert len(res) == 1

    res = sample_library.find(authors=['Nicolaus Copernicus', 'Bernhard Riemann'], match_all=True)
    assert len(res) == 0

    # find author with wildcard
    res = sample_library.find(authors=['*Copernicus*'])
    assert len(res) == 1

    # find single keyword
    res = sample_library.find(keywords=['fake'])
    assert len(res) == 10

    # find multiple keywords
    res = sample_library.find(keywords=['fake', 'group theory'])
    assert len(res) == 11

    # require multiple keywords
    res = sample_library.find(keywords=['fake', 'quantum mechanics'], match_all=True)
    assert len(res) == 1

    res = sample_library.find(isbn="9780043589632")
    assert len(res) == 1

    # find based on publication_date
    res = sample_library.find(published_before="1700-01-01")
    assert len(res) == 5

    res = sample_library.find(published_after="2020-01-01")
    assert len(res) == 6

    res = sample_library.find(published_after="1600-01-01", published_before="1650-12-31")
    assert len(res) == 3

    # empty result
    assert not sample_library.find(authors=['Non-existent Author'])



def test_BookLibraryJSON_update(sample_library):
    res = sample_library.find(uuid='23271944-9e47-45d1-a592-9e74b1f562f0')
    assert len(res) == 1
    assert res[0].meta == { "__type__": "mybooks.Book", "uuid": "23271944-9e47-45d1-a592-9e74b1f562f0", "title": "The Art of Cooking", "authors": ["Jane Miller", "Karen Lee", "John Doe"], "publication_date": datetime.date(2018, 5, 5),
        "keywords": {"culinary arts", "cooking", "fake", "food", "recipes"}}


    uuid = res[0].uuid
    sample_library.update(uuid)

    update_count = sample_library.update(uuid, title="A modified title", authors=["Author A", "Author B", "Author C"], isbn="9786610326266", publication_date="1990-01-31", keywords=["Apple", "Banana"])
    assert update_count == 8
    assert res[0].meta == {'__type__': 'mybooks.Book', 'uuid': '23271944-9e47-45d1-a592-9e74b1f562f0', 'title': 'A modified title', 'authors': ['Author A', 'Author B', 'Author C'], 'publication_date': datetime.date(1990, 1, 31), 
                         'isbn': '9786610326266', 'keywords': {'Apple', 'Banana'}}




def test_BookLibraryJSON_remove(sample_library):
    
    assert len(sample_library) == 20

    uuid = "3063619e-495c-4082-ab8c-8eec88d63cc9"
    res = sample_library.find(uuid=uuid)
    assert len(res) == 1

    return_value = sample_library.remove(uuid)
    assert return_value == True
    assert len(sample_library) == 19

    # Try to remove book thst is not in library
    return_value = sample_library.remove('a9cd307b-f811-489b-8ede-b1a5b68ce4f3')
    assert return_value == False
    assert len(sample_library) == 19

    # Tra to remove None
    with pytest.raises(ValueError):
        sample_library.remove(None)
    


    
@pytest.mark.xfail
def test_BookLibraryJSON_write_to_json_file(sample_library):
    raise NotImplementedError

