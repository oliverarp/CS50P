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
from project import parse_args 
from project import handle_cli_command_init
from project import handle_cli_command_import
from project import handle_cli_command_list
from project import handle_cli_command_add
from project import handle_cli_command_delete
from project import handle_cli_command_update
from book_library import BookLibraryJSON
import argparse
import os
import shutil

def test_parse_args():
    argv = ['--file', 'foo.json', 'init']

    args = parse_args(argv)

    assert args.command == 'init'
    assert args.file == 'foo.json'

    # missing command argument
    argv = ['--file', 'foo.json']
    with pytest.raises(SystemExit):
        args = parse_args(argv)


def test_parse_args_init():
    argv = ['init', '--force']

    args = parse_args(argv)

    assert args.command == 'init'
    assert args.force == True


def test_parse_args_import():
    argv = ['import', '--isbn-file', 'sample_isbns.txt', '--json-file', 'sample_library.json']

    args = parse_args(argv)

    assert args.command == 'import'
    assert args.isbn_file == 'sample_isbns.txt'
    assert args.json_file == 'sample_library.json'

def test_parse_args_list():
    argv = ['list', '--title', 'A Title', '--isbn', '123-4567890', '--keywords', 'cat', 'dog', '--authors', 'Jane Doe', 'John Doe', '--match-all', 
            '--published-after', '2020-01-01', '--published-before', '2021-12-31', '--show-keywords', '--uuid', '23271944-9e47-45d1-a592-9e74b1f562f0', '--show-uuid']

    args = parse_args(argv)
    assert args.command == 'list'
    assert args.title == 'A Title'
    assert args.isbn == '123-4567890'
    assert args.keywords == ['cat', 'dog']
    assert args.authors == ['Jane Doe', 'John Doe']
    assert args.match_all == True
    assert args.published_after == '2020-01-01'
    assert args.published_before == '2021-12-31'
    assert args.show_keywords == True
    assert args.uuid == '23271944-9e47-45d1-a592-9e74b1f562f0'
    assert args.show_uuid == True

def test_parse_args_add():
    argv = ['add', '--title', 'A Title', '--isbn', '123-4567890', '--keywords', 'cat', 'dog', '--authors', 'Jane Doe', 'John Doe',  
            '--publication-date', '2020-01-01',  '--fetch-meta']
    
    args = parse_args(argv)
    assert args.command == 'add'
    assert args.title == 'A Title'
    assert args.isbn == '123-4567890'
    assert args.keywords == ['cat', 'dog']
    assert args.authors == ['Jane Doe', 'John Doe']
    assert args.publication_date == '2020-01-01'
    assert args.fetch_meta == True
    

def test_parse_args_update():
    argv = ['update', '--uuid', '23271944-9e47-45d1-a592-9e74b1f562f0', '--title', 'A Title', '--isbn', '123-4567890', '--keywords', 'cat', 'dog', '--authors', 'Jane Doe', 'John Doe',  
            '--publication-date', '2020-01-01']
    
    args = parse_args(argv)
    assert args.command == 'update'
    assert args.uuid == '23271944-9e47-45d1-a592-9e74b1f562f0'
    assert args.title == 'A Title'
    assert args.isbn == '123-4567890'
    assert args.keywords == ['cat', 'dog']
    assert args.authors == ['Jane Doe', 'John Doe']
    assert args.publication_date == '2020-01-01'


def test_parse_args_delete():
    argv = ['delete', '--uuid', '3063619e-495c-4082-ab8c-8eec88d63cc9']
    
    args = parse_args(argv)
    assert args.command == 'delete'
    assert args.uuid == '3063619e-495c-4082-ab8c-8eec88d63cc9'


def test_handle_cli_command_init(monkeypatch):
    tmp_lib_name = "temporary_test_library.tmp"
    if os.path.isfile(tmp_lib_name):
        os.remove(tmp_lib_name)

    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.command = 'init'
    args.force = False
    answer = handle_cli_command_init(args)
    assert answer == True
    assert os.path.isfile(tmp_lib_name)


    # Try initializing when file already exists, but dont' answer Yes
    monkeypatch.setattr('builtins.input', lambda _: "cat")  
    answer = handle_cli_command_init(args)
    assert answer == False
    assert os.path.isfile(tmp_lib_name)
    
    # Try initializing when file already exists, and answer Yes
    monkeypatch.setattr('builtins.input', lambda _: "Yes")  
    answer = handle_cli_command_init(args)
    assert answer == True
    assert os.path.isfile(tmp_lib_name)

    os.remove(tmp_lib_name)



def test_handle_cli_command_import(mocker):
    tmp_lib_name = "temporary_test_library.tmp"

    # No simultaneous usage of --json-file and --isbn-file
    args = argparse.Namespace()
    args.file = tmp_lib_name

    # Step : create empty library
    if os.path.isfile(tmp_lib_name):
        os.remove(tmp_lib_name)

    args = argparse.Namespace()
    args.file = tmp_lib_name

    answer = handle_cli_command_init(args)
    assert answer == True
    assert os.path.isfile(tmp_lib_name)

    
    # Test case json and isbn file specified
    args.json_file = 'json_file.json'
    args.isbn_file = 'isbn_file.txt'
    with pytest.raises(ValueError):
        handle_cli_command_import(args)        


    # Test case --import-json
    args.json_file = 'sample_library.json'
    args.isbn_file = None

    num_imported = handle_cli_command_import(args)
    assert num_imported == 20

    # Test case --import-isbn
    # resuse test library from previous test
    args.json_file = None
    args.isbn_file = 'sample_isbns.txt'

    with mocker.patch('isbnlib.meta', return_value={'Title': "A Title", 'Authors': ['John Doe', 'Jane Doe'], 'Year': 1970}):
        num_imported = handle_cli_command_import(args)
    assert num_imported == 9

    if os.path.isfile(tmp_lib_name):
        os.remove(tmp_lib_name)




def test_handle_cli_command_list():
    # prepare temporary test library
    tmp_lib_name = "temporary_test_library.tmp"
    sample_library_name = 'sample_library.json'
    assert os.path.isfile(sample_library_name)
    shutil.copyfile(sample_library_name, tmp_lib_name)
    assert os.path.isfile(tmp_lib_name)

    # all possible args simultaneously
    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.title = 'A title'
    args.isbn = '9780043589632'
    args.keywords = ['Cat', 'Dog']
    args.authors = ['Jane Doe', 'John Doe']
    args.match_all = True
    args.published_after = "1970-01-01"
    args.published_before = "2024-06-19"
    args.show_all = True
    args.show_keywords = True
    args.uuid = None
    args.show_uuid = True

    num_books = handle_cli_command_list(args)        
    assert num_books == 0

    args.title = "The Lost Kingdom"
    args.isbn = None
    args.keywords = None
    args.authors = None
    args.match_all = False
    args.published_after = None
    args.published_before = None
    args.show_keywords = False
    args.uuid = None
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 1

    args.title = None
    args.isbn = '9780043589632'
    args.keywords = None
    args.authors = None
    args.match_all = False
    args.published_after = None
    args.published_before = None
    args.show_keywords = False
    args.uuid = None
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 1

  
    args.title = None
    args.isbn = None
    args.keywords = ['fake', 'group theory']
    args.authors = None
    args.match_all = False
    args.published_after = None
    args.published_before = None
    args.show_keywords = False
    args.uuid = None
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 11

    args.title = None
    args.isbn = None
    args.keywords = ['fake', 'group theory']
    args.authors = None
    args.match_all = True
    args.published_after = None
    args.published_before = None
    args.show_keywords = False
    args.uuid = None
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 0


    args.title = None
    args.isbn = None
    args.keywords = None
    args.authors = ['Quincy Brown', 'John Doe']
    args.match_all = False
    args.published_after = None
    args.published_before = None
    args.show_keywords = False
    args.uuid = None
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 2

    args.title = None
    args.isbn = None
    args.keywords = None
    args.authors = ['Quincy Brown', 'John Doe']
    args.match_all = True
    args.published_after = None
    args.published_before = None
    args.show_keywords = False
    args.uuid = None
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 1

    args.title = None
    args.isbn = None
    args.keywords = None
    args.authors = None
    args.match_all = None
    args.published_after = "1600-01-01"
    args.published_before = "1650-12-31"
    args.show_keywords = False
    args.uuid = None
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 3


    args.title = None
    args.isbn = None
    args.keywords = None
    args.authors = None
    args.mach_all = None
    args.published_after = None
    args.published_before = None
    args.show_keywords = False
    args.uuid = '23271944-9e47-45d1-a592-9e74b1f562f0'
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 1

    assert os.path.isfile(tmp_lib_name)
    os.remove(tmp_lib_name)


def test_handle_cli_command_list_output_no_keywords(capsys):
    # prepare temporary test library
    tmp_lib_name = "temporary_test_library.tmp"
    sample_library_name = 'sample_library.json'
    assert os.path.isfile(sample_library_name)
    shutil.copyfile(sample_library_name, tmp_lib_name)
    assert os.path.isfile(tmp_lib_name)

    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.title = None
    args.isbn = None
    args.keywords = None
    args.authors = None
    args.match_all = False
    args.show_all = False
    args.published_after = "1600-01-01"
    args.published_before = "1650-12-31"
    args.show_keywords = False
    args.uuid = False
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 3

    expected_output = '''1: René Descartes, "Discours de la méthode" (1637)
2: Francis Bacon, "Novum Organum" (1620)
3: Johannes Kepler, "Harmonices Mundi" (1619)
'''

    captured = capsys.readouterr()
    assert captured.out == expected_output

    assert os.path.isfile(tmp_lib_name)
    os.remove(tmp_lib_name)

def test_handle_cli_command_list_output_keywords(capsys):
    # prepare temporary test library
    tmp_lib_name = "temporary_test_library.tmp"
    sample_library_name = 'sample_library.json'
    assert os.path.isfile(sample_library_name)
    shutil.copyfile(sample_library_name, tmp_lib_name)
    assert os.path.isfile(tmp_lib_name)

    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.title = None
    args.isbn = None
    args.keywords = None
    args.authors = None
    args.match_all = True
    args.show_all = False
    args.published_after = "1600-01-01"
    args.published_before = "1650-12-31"
    args.show_keywords = True
    args.uuid = False
    args.show_uuid = False
    num_books = handle_cli_command_list(args)        
    assert num_books == 3

    expected_output = '''1: René Descartes, "Discours de la méthode" (1637) ['methodology', 'philosophy', 'rationalism']
2: Francis Bacon, "Novum Organum" (1620) ['logic', 'philosophy', 'scientific method']
3: Johannes Kepler, "Harmonices Mundi" (1619) ['astronomy', 'harmonics', 'mathematics']
'''
    captured = capsys.readouterr()
    assert captured.out == expected_output

    assert os.path.isfile(tmp_lib_name)
    os.remove(tmp_lib_name)

def test_handle_cli_command_list_output_uuid(capsys):
    # prepare temporary test library
    tmp_lib_name = "temporary_test_library.tmp"
    sample_library_name = 'sample_library.json'
    assert os.path.isfile(sample_library_name)
    shutil.copyfile(sample_library_name, tmp_lib_name)
    assert os.path.isfile(tmp_lib_name)

    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.title = None
    args.isbn = None
    args.keywords = None
    args.authors = None
    args.match_all = True
    args.show_all = False
    args.published_after = "1600-01-01"
    args.published_before = "1650-12-31"
    args.show_keywords = True
    args.uuid = False
    args.show_uuid = True
    num_books = handle_cli_command_list(args)        
    assert num_books == 3

    expected_output = '''1: René Descartes, "Discours de la méthode" (1637) ['methodology', 'philosophy', 'rationalism'] <3063619e-495c-4082-ab8c-8eec88d63cc9>
2: Francis Bacon, "Novum Organum" (1620) ['logic', 'philosophy', 'scientific method'] <de897810-692d-4ef0-8fd7-426da3b2318d>
3: Johannes Kepler, "Harmonices Mundi" (1619) ['astronomy', 'harmonics', 'mathematics'] <ff85c452-def5-4e5c-adde-ff3798766812>
'''
    captured = capsys.readouterr()
    assert captured.out == expected_output

    assert os.path.isfile(tmp_lib_name)
    os.remove(tmp_lib_name)



def test_handle_cli_command_add():
    # prepare temporary test library
    tmp_lib_name = "temporary_test_library.tmp"
    sample_library_name = 'sample_library.json'
    assert os.path.isfile(sample_library_name)
    shutil.copyfile(sample_library_name, tmp_lib_name)
    assert os.path.isfile(tmp_lib_name)

    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.title = 'A new book'
    args.isbn = '9781255431085'
    args.keywords = ['New', 'Fake']
    args.authors = ['John Doe', 'Fred Nurk']
    args.publication_date = "2024-06-21"
    args.fetch_meta = False


    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    res = lib.find()
    assert len(res) == 20
    
    assert handle_cli_command_add(args) == True       

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    res = lib.find()
    assert len(res) == 21
    

    # trying to add the same book twice returns False
    assert handle_cli_command_add(args) == False 

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    res = lib.find()
    assert len(res) == 21

    assert os.path.isfile(tmp_lib_name)
    os.remove(tmp_lib_name)




def test_handle_cli_command_add():
    # prepare temporary test library
    tmp_lib_name = "temporary_test_library.tmp"
    sample_library_name = 'sample_library.json'
    assert os.path.isfile(sample_library_name)
    shutil.copyfile(sample_library_name, tmp_lib_name)
    assert os.path.isfile(tmp_lib_name)

    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.title = 'A new book'
    args.isbn = '9781255431085'
    args.keywords = ['New', 'Fake']
    args.authors = ['John Doe', 'Fred Nurk']
    args.publication_date = "2024-06-21"
    args.fetch_meta = False


    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    res = lib.find()
    assert len(res) == 20
    
    assert handle_cli_command_add(args) == True       

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    res = lib.find()
    assert len(res) == 21
    

    # trying to add the same book twice returns False
    assert handle_cli_command_add(args) == False 

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    res = lib.find()
    assert len(res) == 21

    assert os.path.isfile(tmp_lib_name)
    os.remove(tmp_lib_name)



def test_handle_cli_command_update():
    # prepare temporary test library
    tmp_lib_name = "temporary_test_library.tmp"
    sample_library_name = 'sample_library.json'
    assert os.path.isfile(sample_library_name)
    shutil.copyfile(sample_library_name, tmp_lib_name)
    assert os.path.isfile(tmp_lib_name)


    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.uuid = "23271944-9e47-45d1-a592-9e74b1f562f0"

    args.title = 'A modified titlek'
    args.isbn = '9786610326266'
    args.keywords = ["Apple", "Banana"]
    args.authors = ["Author A", "Author B", "Author C"]
    args.publication_date = "1990-01-31"


    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    
    assert handle_cli_command_update(args) == True


#     args = argparse.Namespace()
#     args.file = tmp_lib_name
#     args.title = None
#     args.isbn = None
#     args.keywords = None
#     args.authors = None
#     args.all = False
#     args.published_after = None
#     args.published_before = None
#     args.show_keywords = True
#     args.show_uuid = True
#     num_books = handle_cli_command_list(args)        
#     assert num_books == 3

#     expected_output = '''1: René Descartes, "Discours de la méthode" (1637) ['methodology', 'philosophy', 'rationalism'] <3063619e-495c-4082-ab8c-8eec88d63cc9>
# 2: Francis Bacon, "Novum Organum" (1620) ['logic', 'philosophy', 'scientific method'] <de897810-692d-4ef0-8fd7-426da3b2318d>
# 3: Johannes Kepler, "Harmonices Mundi" (1619) ['astronomy', 'harmonics', 'mathematics'] <ff85c452-def5-4e5c-adde-ff3798766812>
# '''
#     captured = capsys.readouterr()
#     assert captured.out == expected_output


    assert os.path.isfile(tmp_lib_name)
    os.remove(tmp_lib_name)


def test_handle_cli_command_delete():
    # prepare temporary test library
    tmp_lib_name = "temporary_test_library.tmp"
    sample_library_name = 'sample_library.json'
    assert os.path.isfile(sample_library_name)
    shutil.copyfile(sample_library_name, tmp_lib_name)
    assert os.path.isfile(tmp_lib_name)


    args = argparse.Namespace()
    args.file = tmp_lib_name
    args.uuid = "3063619e-495c-4082-ab8c-8eec88d63cc9"

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    assert len(lib) == 20
    
    assert handle_cli_command_delete(args) == True       

    lib = BookLibraryJSON()
    lib.read_from_json_file(args.file)
    assert len(lib) == 19

    assert os.path.isfile(tmp_lib_name)
    os.remove(tmp_lib_name)
