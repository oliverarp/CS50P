# MyBooks - A simple book library software

2024 by Oliver Arp <oarp@gmx.net>

This is my final project for the [CS50P](https://cs50.harvard.edu/python/2022/)  *Introduction to Programming with Python* course.

Video Demo: https://youtu.be/vN3wQte-mRo

## Table of content

* [Requirements](#requirements)
    * [Functional requirements](#functional-requirements)
    * [Non-functional requirements](#non-functional-requirements)
* [Installation](#installation)
    * [Download the source code](#download-the-source-code)
    * [Create a virtual environment](#create-a-virtual-environment-optional
    )
    * [Install required packages](#install-required-packages)
* [Usage](#usage)
    * [The command line interface (CLI)](#the-command-line-interface)
    * [Create an empty library](#create-an-empty-book-library)
    * [Add a book](#add-a-book)
        * [Fetch meta data from the internet](#fetch-meta-data-from-the-internet)
    * [Import bulk data](#import-bulk-data)
        * [Import a library file](#import-a-library-file)
        * [Bulk import meta data from the internat](#bulk-import-meta-data-from-the-internat)
    * [List and find books](#list-and-find-books)
    * [Update (modify) a book](#update-modify-a-book)
    * [Delete a book](#delete-a-book)
* [Library file format](#library-file-format)
* [Code structure](#code-structure)
    * [Unit tests](#unit-tests)
* [Known issues](#known-issues)




## Requirements

Below you find
- the *functional requirements* for this project as I have defined them
- the *non-functional requirements* that have to be met in order to be accepted as final project for [CS50P](https://cs50.harvard.edu/python/2022/):

### Functional requirements

- Implement a simple book library software, i.e., a simple data base that stores meta data representing books. 
- A book shall be represented by the following meta data:
    - title (mandatory)
    - list of authors (mandatory)
    - list of keywords (optional)
    - date of publication (optional)
    - ISBN (optional)
- Provide a command line interface (CLI) for performing the following operation: 
    - Initialize an empty book library
    - Add a book to the library
    - List the books in the library, i.e., their meta data
    - Find books based on its meta data, especially search for keywords, authors, date ranges, phrases contained in the title
    - Update, i.e., change, the meta data of a selected book
    - Delete a selected book
    - Fetch meta data from internet based on ISBN 
    - Import bulk data into the library from a file
- The book library shall be saved in and restored from a human readable file format.


### Non-functional requirements

- The project must be implemented in Python.
- The project must have a main function and three or more additional functions. At least three of those additional functions must be accompanied by tests that can be executed with pytest.

    - The main function must be in a file called project.py, which should be in the “root” (i.e., top-level folder) of the project.
    - The  3 required custom functions other than main must also be in project.py and defined at the same indentation level as main (i.e., not nested under any classes or functions).
    - The test functions must be in a file called test_project.py, which should also be in the “root” of your project. They shall have the same name as the custom functions, prepended with test_ (test_custom_function, for example, where custom_function is a function you’ve implemented in project.py).
    - Additional classes and functions may be implemented beyond the minimum requirement.

- Implementing the project should entail more time and effort than is required by each of the course’s problem sets.
- Any pip-installable libraries that the project requires must be listed, one per line, in a file called requirements.txt in the root of the project.

## Installation

Make sure you have [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/) installed. 


### Download the source code

Download the source code from GitHub https://github.com/oliverarp/CS50P


### Install required packages

Install required Python packages:
```console
$ cd CS50P/project
$ pip install -r requirements.txt
```

## Usage

The software provides a command line interface (CLI) for performing fundamental operations like *initialization* of the library, *importing* bulk data into the library, *adding* books, *listing* (and finding) books, *updating* (changing) the meta data of a book as well as *removing* a book from the library.

### The command line interface

Execute
```console
$ python project.py --help
```
to obtain a general overview on the usage of the CLI:
```console
usage: project.py [-h] [--file FILE] {init,add,delete,list,update,import} ...

A simple book library software

positional arguments:
  {init,add,delete,list,update,import}
                        sub-command help
    init                Initialize empty library
    add                 Add a book to the library
    delete              Delete a book from the library
    list                List library contents
    update              Modify book in library
    import              Import data

options:
  -h, --help            show this help message and exit
  --file FILE           Library file
```

Currently the CLI supports the commands **init**, **add**, **delete**, **list**, **update**, **import**.

Execute
```console
$ python project.py <COMMAND_NAME> --help
```
to get command specific help.


### Create an empty book library

Before adding books to the library it is required to initialize an empty book library by executing

```console
$ python project.py init
```

This will create by default a file *mybooks.json* in the current folder.

Note: A description of the used file format can be found below in the section [Library file format](#library-file-format).

You can use different library files by using the ```--file <different file name>``` option.


If a library file with the selected name already exists, you will be asked, if it shall be overwritten. In that case all data of the existing file will be lost. You can prevent that question and force overwriting the existing file by using the ```--force``` option.

### Add a book

Add a book with minimum amount of meta data
```console
$ python project.py add --title "A book" --authors "John Doe"
```
You should receive a message:
```console
Added: John Doe, "A book"
```

A more sophisticated example:
```console
$ python project.py add --title "Another book" --authors "Jane Doe" "Fred Nurk" --publication-date 2024-07-10 --keywords "sample book" apple cat --isbn 9781362906773
```
yielding:
```console
Added: Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3
```

#### Fetch meta data corresponding to an ISBN from the internet

Execute:
```console
$ python project.py add --isbn 978-0-7475-3269-9 --fetch-meta
```
which yields

```console
Added: J. K. Rowling, "Harry Potter And The Philosopher's Stone" (1997), ISBN 978-0-7475-3269-9
```

### Import bulk data

Currently there are two ways of importing bulk data in to the library:
1. Import the contents of another [library file](#library-file-format) 
1. Provide a list of ISBN numbers in a text file (one ISBN per line) that will be used to fetch meta data from the internet.

#### Import a library file

To import an existing [library file](#library-file-format), here *sample_library.json* execute: 
```console
$ python project.py import --json-file sample_library.json
```
which yields in this case

```console
Importing file sample_library.json ...
20 of 20 books imported (0 duplicates).
```

Note: The books of the sample library will be used below to demonstrate the command line interface. 


#### Bulk import meta data from the internat

Another way of importing multiple books is ti specify a list of ISBN in a text file (here *sample_isbns.txt*), which one ISBN per line and executing:

```console
$ python project.py import --isbn-file  sample_isbns.txt
```

The program tries to fetch the corresponding meta data from the internet. On success you ge an output similar to 
```console
Importing file sample_isbns.txt ...
Imported ISBN 9780785839781.
Imported ISBN 9780141033570.
Imported ISBN 9781529034523.
Imported ISBN 1494745429.
Imported ISBN 9781920265298.
Imported ISBN 9780008471286.
Imported ISBN 9798749522310.
Imported ISBN 9781526626585.
Imported ISBN 9780552569460.
9 of 9 books imported (0 duplicates, 0 lines skipped).
```

### List and find books

The *list* command is a powerful tool to list and find book in the library. The command accepts a multitude of options to affect which books will be listed and how the result wil be displayed:

```console
$ python project.py list --help     
```

```console
usage: project.py list [-h] [--title TITLE] [--isbn ISBN] [--keywords KEYWORD [KEYWORD ...]] [--authors AUTHOR [AUTHOR ...]] [--show-all] [--match-all] [--published-after YYYY-MM-DD]
                       [--published-before YYYY-MM-DD] [--show-keywords] [--uuid UUID] [--show-uuid] [--bare]

options:
  -h, --help            show this help message and exit
  --title TITLE         Title of the book
  --isbn ISBN           ISBN number
  --keywords KEYWORD [KEYWORD ...]
                        Space-separated list of keywords
  --authors AUTHOR [AUTHOR ...]
                        Space-separated list of author names
  --show-all            Show all metadata of the book
  --match-all           Match all of given authors or keywords
  --published-after YYYY-MM-DD
                        Date in ISO format (YYYY-MM-DD)
  --published-before YYYY-MM-DD
                        Date in ISO format (YYYY-MM-DD)
  --show-keywords       Show keywords
  --uuid UUID           UUID of book in library
  --show-uuid           Show UUID of book in library
  --bare                Disable enumeration
``` 

The following examples use books from the [sample library](#import-a-library-file) to demonstrate the *list* command:

A most simple application is to list all books in library:

Execute:
```console
$ python project.py list
```
Sample output:
```console
[1] John Doe, "A book"
[2] Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3
...
```

By default the *list* command returns an enumerated list of books, one book per line, that is sorted by the publication date (unknown and latest first).

You can disable the enumeration by using the `--bare` option:
```console
$ python project.py list --bare
```
Sample output:
```console
John Doe, "A book"
Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3
...
```
Note: The standard output format of the *list* command shows only a subset of the available metadata that is stored in the library. You can use the ```--show-all``` option to display all available metadata.

To update and delete books from the library is is necessary to have a method of uniquely identifying each book in the library. This is done via [UUID](https://de.wikipedia.org/wiki/Universally_Unique_Identifier)s. Each book is tagged automatically with an UUID when added to the library.

One can display the UUID of a book by means of the ```--show-uuid``` option of the *list* command:

```console
$ python project.py list --show-uuid
```
Sample output:
```console
[1] John Doe, "A book" <8f8f2a13-82b6-4642-8d24-841471f58f0c>
[2] Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3 <f63d2956-e670-4db3-b4b4-3f49a881b125>
...
```
The UUID of each book is shown between angled brackets.

In the following sections the different options of the *list* command are demonstrated that allow to restrict the result set based on various criteria. 

Note: All of the following options can be combined for a sophisticated search in the library.

#### Findung books based on meta-data

As seen in the command line help (see above) the list command offers various options to restrict the result set based on the metadata of the books.

##### Find a book based on its title

```console
$ python project.py list --title "*book*"
```
Sample output:
```console
[1] John Doe, "A book"
[2] Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3
[3] John Christopher, "The Tripods: The White Mountains - Book 1" (2013), ISBN 978-0-552-56946-0
```



##### Find book with certain keywords

To find books based on keywords provide a  space separated list of keywords to the *list* command:
```console
$ python .\project.py list --keywords fake science --show-keywords
```
Sample output:
```console
[1] Rachel Adams, Steve Young, "Mastering Python Programming" (2023), ISBN 978-0-295-84836-5 ['Python', 'fake', 'programming', 'software development']
[2] Alice Johnson, Bob Smith, "Mysteries of the Quantum Realm" (2023), ISBN 978-0-04-358963-2 ['fake', 'physics', 'quantum mechanics', 'science']
[3] Oliver Martin, "The Digital Economy" (2022), ISBN 978-0-7995-1082-9 ['business', 'economics', 'fake', 'innovation', 'technology']
[4] Frank Harris, "AI in the Modern World" (2021), ISBN 978-1-75784-517-5 ['artificial intelligence', 'fake', 'future', 'science', 'technology']
[5] Tina Evans, Uma Nelson, "Mindfulness and Meditation" (2020), ISBN 1-5142-3568-4 ['fake', 'meditation', 'mental health', 'mindfulness', 'well-being']
[6] Gina Wright, Ian Black, Henry Adams, "Journey Through the Stars" (2020), ISBN 978-1-229-56826-7 ['exploration', 'fake', 'science fiction', 'space']
[7] Catherine Bell, David White, Emily Green, "The Lost Kingdom" (2019), ISBN 978-0-7600-9827-1 ['adventure', 'fake', 'fantasy', 'kingdom', 'magic']
[8] Jane Miller, Karen Lee, John Doe, "The Art of Cooking" (2018) ['cooking', 'culinary arts', 'fake', 'food', 'recipes']
[9] fake, Laura Clark, Michael Davis, et al., "Ancient Civilizations" (2017), ISBN 978-1-175-08426-2 ['archaeology', 'civilizations', 'fake', 'history']
[10] Paula Roberts, Quincy Brown, John Doe, "Gardening for Beginners" (2016), ISBN 978-0-514-18689-6 ['fake', 'gardening', 'hobbies', 'nature', 'plants']
```

Note: The standard behavior is that the *list* command return all books that are tagged by **one or more** of the specified keywords. If it is desired to find only those books that are tagged by **all** of the specified keywords add the ```--match-all``` option:

```console
$ python .\project.py list --keywords fake science --show-keywords --match-all
```
Sample output:
```console
[1] Alice Johnson, Bob Smith, "Mysteries of the Quantum Realm" (2023), ISBN 978-0-04-358963-2 ['fake', 'physics', 'quantum mechanics', 'science']
[2] Frank Harris, "AI in the Modern World" (2021), ISBN 978-1-75784-517-5 ['artificial intelligence', 'fake', 'future', 'science', 'technology']
```

If keywords contain space, use single or double quotes on the command line:

```console
$  python .\project.py list --keywords "artificial intelligence" fake --show-keywords --match-all 
```
Sample output:
```console
[1] Frank Harris, "AI in the Modern World" (2021), ISBN 978-1-75784-517-5 ['artificial intelligence', 'fake', 'future', 'science', 'technology']
```

Wildcards are also allowed:

```console
$ python .\project.py list --keywords "*artificial*"  --show-keywords
```
Sample output:
```console
[1] Frank Harris, "AI in the Modern World" (2021), ISBN 978-1-75784-517-5 ['artificial intelligence', 'fake', 'future', 'science', 'technology']  
```


###### Find books of specific authors

To find all  books of the author *John Doe* execute:

```console
$ python .\project.py list --authors "John Doe" 
```
Sample output:
```console
[1] John Doe, "A book"
[2] Jane Miller, Karen Lee, John Doe, "The Art of Cooking" (2018)
[3] Paula Roberts, Quincy Brown, John Doe, "Gardening for Beginners" (2016), ISBN 978-0-514-18689-6
```

Wildcards and multiple authors are allowed. To find all books of the authors with last names Doe **or** Nurk execute:

```console
$ python .\project.py list --authors "*Doe" "*Nurk" 
```
Sample output:
```console
[1] John Doe, "A book"
[2] Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3
[3] Jane Miller, Karen Lee, John Doe, "The Art of Cooking" (2018)
[4] Paula Roberts, Quincy Brown, John Doe, "Gardening for Beginners" (2016), ISBN 978-0-514-18689-6
```

To get only those books that match both author patterns, i.e. all books of the authors with last names *Doe* **and** *Nurk* execute:

```console
$ python .\project.py list --authors "*Doe" "*Nurk" --match-all
```
Sample output:
```console
[1] Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3
```


##### Find books based on its publication date

To find all books that are published, e.g., after 1/1/2020 execute:

```console
$ python .\project.py list --published-after 2020-01-01
```
Sample output:
```console
[1] Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3
[2] Rachel Adams, Steve Young, "Mastering Python Programming" (2023), ISBN 978-0-295-84836-5
[3] Alice Johnson, Bob Smith, "Mysteries of the Quantum Realm" (2023), ISBN 978-0-04-358963-2
[4] Oliver Martin, "The Digital Economy" (2022), ISBN 978-0-7995-1082-9
[5] Frank Harris, "AI in the Modern World" (2021), ISBN 978-1-75784-517-5
[6] Herman Melville, "Moby Dick" (2021), ISBN 978-0-7858-3978-1
[7] Lewis Carroll, "Alice In Wonderland - The Original 1865 Edition With Complete Illustrations By Sir John Tenniel (A Classic Novel Of Lewis Carroll)" (2021), ISBN 979-8-7495-2231-0
[8] J. R. R. Tolkien, "The Lord Of The Rings [Illustrated Edition]" (2021), ISBN 978-0-00-847128-6
[9] Tina Evans, Uma Nelson, "Mindfulness and Meditation" (2020), ISBN 1-5142-3568-4
[10] Gina Wright, Ian Black, Henry Adams, "Journey Through the Stars" (2020), ISBN 978-1-229-56826-7
```

Similarly, to find all books that are published before 1/1/1900 execute:

```console
$ python .\project.py list --published-before 1900-01-01
```
Sample output:
```console
[1] Bernhard Riemann, "Über die Hypothesen, welche der Geometrie zu Grunde liegen" (1868)
[2] Évariste Galois, "Éléments de mathématique" (1830)
[3] Joseph-Louis Lagrange, "Mécanique Analytique" (1788)
[4] Jean le Rond d'Alembert, "Traité de dynamique" (1743)
[5] Leonhard Euler, "The Mathematical Principles of Natural Philosophy" (1736)
[6] Isaac Newton, "Philosophiæ Naturalis Principia Mathematica" (1687)
[7] René Descartes, "Discours de la méthode" (1637)
[8] Francis Bacon, "Novum Organum" (1620)
[9] Johannes Kepler, "Harmonices Mundi" (1619)
[10] Nicolaus Copernicus, "De revolutionibus orbium coelestium" (1543)
```

Both approaches can be combined to find all books that are published between 1/1/1800 and 1/1/1700:

```console
$ python .\project.py list --published-before 1800-01-01 --published-after 1700-01-01
```
Sample output:
```console
[1] Joseph-Louis Lagrange, "Mécanique Analytique" (1788)
[2] Jean le Rond d'Alembert, "Traité de dynamique" (1743)
[3] Leonhard Euler, "The Mathematical Principles of Natural Philosophy" (1736)
```

##### Find book based on its ISBN

FIXME

```console
$ python .\project.py list --isbn 1514235684
```
Sample output:
```console
[1] Tina Evans, Uma Nelson, "Mindfulness and Meditation" (2020), ISBN 1-5142-3568-4
```
Note: The list command also accepts the ISBN with dashes, i.e. "1-5142-3568-4".

##### Find book based on its UUID

To find books based on their UUID execute:
```console
$ python .\project.py list --uuid c93ec88a-33d2-4c13-9793-74b1645dc5f6
```
Sample output:
```console
[1] Gina Wright, Ian Black, Henry Adams, "Journey Through the Stars" (2020), ISBN 978-1-229-56826-7
```

Note: You can use the ```--show-uuid``` flag of the list command to show the UUIDs of the books in the library.


### Update (modify) a book

The *update* command allows to modify the metadata of a book in the library. The command requires the
argument *uuid* to identify the book that shall be modified. All other optional arguments are shown in the command line help:

```console
$ python project.py update --help     
```
```console
usage: project.py update [-h] --uuid UUID [--title TITLE] [--isbn ISBN] [--authors AUTHOR [AUTHOR ...]] [--keywords KEYWORD [KEYWORD ...]] [--publication-date YYYY-MM-DD]

options:
  -h, --help            show this help message and exit
  --uuid UUID           UUID of book in library (required)
  --title TITLE         Set new title
  --isbn ISBN           Set new ISBN number
  --authors AUTHOR [AUTHOR ...]
                        Replace authors by space-separated list of author names
  --keywords KEYWORD [KEYWORD ...]
                        Replace keywords by space-separated list of new keywords
  --publication-date YYYY-MM-DD
                        Set publication date in ISO format (YYYY-MM-DD)
```

Note: It is not possible to modify the UUID of a book in the library (see )after the book has been created.

The following examples use books from the [sample library](#import-a-library-file) to demonstrate the *update* command:


#### Change the title of a book

```console
$ python .\project.py list --authors "Jane Doe" --show-uuid
```
Sample output:
```console
[1] Jane Doe, Fred Nurk, "Another book" (2024), ISBN 978-1-362-90677-3 <f63d2956-e670-4db3-b4b4-3f49a881b125>
```


```console
$ python .\project.py update --title "A modified book" --uuid f63d2956-e670-4db3-b4b4-3f49a881b125
Updated: f63d2956-e670-4db3-b4b4-3f49a881b125
````
List the modified book:
```console
$ python .\project.py list --uuid f63d2956-e670-4db3-b4b4-3f49a881b125 --show-uuid
```
```console
 [1] Jane Doe, Fred Nurk, "A modified book" (2024), ISBN 978-1-362-90677-3
```

FIXME

#### Change the list of authors

Get the uuid of the book that shall be updated:
```console
$ python .\project.py list --title "Ancient Civilizations" --show-uuid --show-all-authors
```

```console
[1] fake, Laura Clark, Michael Davis, Nancy Edwards, Gina Wright, "Ancient Civilizations" (2017), ISBN 978-1-175-08426-2 <aaf437ec-40a7-4f95-b11d-70b541167310>
```

Delete first author "fake":

```console
$ python .\project.py update --authors "Laura Clark" "Michael Davis" "Nancy Edwards" "Gina Wright" --uuid aaf437ec-40a7-4f95-b11d-70b541167310
````
```console
Updated: aaf437ec-40a7-4f95-b11d-70b541167310
```

List updated book:
```console
$ python .\project.py list --uuid aaf437ec-40a7-4f95-b11d-70b541167310 --show-all-authors
```

```console
[1] Laura Clark, Michael Davis, Nancy Edwards, Gina Wright, "Ancient Civilizations" (2017), ISBN 978-1-175-08426-2
```

### Change the list of keywords

Get the uuid of the book that shall be updated:
```console
$ python .\project.py list --title "Journey Through the Stars" --show-keywords --show-uuid
```

```console
[1] Gina Wright, Ian Black, Henry Adams, "Journey Through the Stars" (2020), ISBN 978-1-229-56826-7 ['exploration', 'fake', 'science fiction', 'space'] <c93ec88a-33d2-4c13-9793-74b1645dc5f6>
```

Add keyword "warp drive" to the list of keywords:
```console
$ python .\project.py update --uuid c93ec88a-33d2-4c13-9793-74b1645dc5f6 --keywords 'exploration' 'fake' 'science fiction' 'space' 'warp drive'
```

```console
Updated: c93ec88a-33d2-4c13-9793-74b1645dc5f6
```

Note: Currently there is no convenient way to add or delete specific keywords. Only the replacement of the complete list of keywords is supported. 

List modified book:
```console
$ python .\project.py list --uuid c93ec88a-33d2-4c13-9793-74b1645dc5f6 --show-keywords
```

```console
[1] Gina Wright, Ian Black, Henry Adams, "Journey Through the Stars" (2020), ISBN 978-1-229-56826-7 ['exploration', 'fake', 'science fiction', 'space', 'warp drive']
```

#### Change the ISBN

Get the uuid of the book that shall be updated:
```console
$ python .\project.py list --title "The Art of Cooking" --show-uuid
```

```console
[1] Jane Miller, Karen Lee, John Doe, "The Art of Cooking" (2018) <23271944-9e47-45d1-a592-9e74b1f562f0>
```

So far there is no ISBN specified. The following command adds an ISBN:
```console
$ python .\project.py update --uuid 23271944-9e47-45d1-a592-9e74b1f562f0 --isbn 9798749522310
``` 

```console
Updated: 23271944-9e47-45d1-a592-9e74b1f562f0
```

List updated book:
```console
$ python .\project.py list --uuid 23271944-9e47-45d1-a592-9e74b1f562f0
```

```console
[1] Jane Miller, Karen Lee, John Doe, "The Art of Cooking" (2018), ISBN 979-8-7495-2231-0
```


#### Change the publication date

Get the uuid of the book that shall be updated:
```console
$ python .\project.py list --title "Mindfulness and Meditation" --show-uuid --show-all
```

```console
[1] Tina Evans, Uma Nelson, "Mindfulness and Meditation" (2020-10-25), ISBN 1-5142-3568-4 ['fake', 'meditation', 'mental health', 'mindfulness', 'well-being'] <9b63e7af-81c4-478f-952d-2baacdd8ba09>
```

To change the publication date execute:

```console
$ python .\project.py update --uuid 9b63e7af-81c4-478f-952d-2baacdd8ba09 --publication-date 2020-09-23

```console
Updated: 9b63e7af-81c4-478f-952d-2baacdd8ba09
```

List the updated book:
```console
$ python .\project.py list --uuid 9b63e7af-81c4-478f-952d-2baacdd8ba09 --show-all
```

```console
[1] Tina Evans, Uma Nelson, "Mindfulness and Meditation" (2020-09-23), ISBN 1-5142-3568-4 ['fake', 'meditation', 'mental health', 'mindfulness', 'well-being'] <9b63e7af-81c4-478f-952d-2baacdd8ba09>
```

### Delete a book

The *delete* command allows to delete books from the library. 
```console
 $ python .\project.py delete --help
 ```
 ```console
 usage: project.py delete [-h] --uuid UUID

options:
  -h, --help   show this help message and exit
  --uuid UUID  UUID of book in library
``` 

The command requires the uuid of the book that shall be deleted.

Get the uuid of the book that shall be deleted from the library:

```console
$ python .\project.py list --title "A book" --show-uuid
```
```console
[1] John Doe, "A book" <8f8f2a13-82b6-4642-8d24-841471f58f0c>
```

Delete the book from the library:
```console
$ python .\project.py delete --uuid 8f8f2a13-82b6-4642-8d24-841471f58f0c
```

```console
Deleted book with UUID 8f8f2a13-82b6-4642-8d24-841471f58f0c
```

To verify the deletion of the book check that

```console
$ python project.py list --uuid 8f8f2a13-82b6-4642-8d24-841471f58f0c
```
yields no result.


## Library file format

The contents of the book library is stored in a JSON file. An empty file is created by the [Init command](#create-an-empty-book-library). The same format can also be used for the [import of bulk data](#import-a-library-file). Below you see an exceprt of the provided file *sample_library.json*:

```json
[
    {
        "__type__": "mybooks.Book",
        "uuid": "ff85c452-def5-4e5c-adde-ff3798766812",
        "title": "Harmonices Mundi",
        "authors": [
            "Johannes Kepler"
        ],
        "publication_date": "1619-01-01",
        "keywords": [
            "harmonics",
            "astronomy",
            "mathematics"
        ]
    },
    {
        "__type__": "mybooks.Book",
        "uuid": "0eaf43d0-75b5-433d-9cc9-45f4211a3d41",
        "title": "\u00c9l\u00e9ments de math\u00e9matique",
        "authors": [
            "\u00c9variste Galois"
        ],
        "publication_date": "1830-01-01",
        "keywords": [
            "group theory",
            "mathematics",
            "algebra"
        ]
    },

...
]
```

The file contains a JSON array of books. Each book is represented by a JSON object containing a key-value pair ```"__type__": "mybooks.Book"``` that is used as an identifier for a valid book object in the context of this project. Each book object contains additional key-value pairs representing the metadata of the corresponding book. 

## Code structure

The code consists of three main files [project.py](#projectpy), [book_library.py](#book_librarypy), and [book.py](#bookpy). For each file [unit tests](#unit-tests) are implemented.

### project.py
It contains:
* the main function
* the definition of the command line interface (CLI) in the function *parse_args()*
* Handler functions *handle_cli_command_XXXXX()* for all CLI commands, i.e. *init*, *add*, *delete*, *list*, *update*, and *import* .

In this file uses the classes *BookLibraryJSON* and "Book" implemented in [book_library.py](#book_librarypy) and [book.py](#bookpy) that represent the actual book library and the books, respectively.

### book_library.py

In this file a class *BookLibraryJSON* is implemented. It stores the books of the library and implements methods for  *adding*, *findung*, *updating*, and *removing* books, as well as methods for reading and saving [library files](#library-file-format).


### book.py

In this file a class *Book* is implemented which represents a single book with all its metadata in the library. A dictionary is used to store the metadata in a book object. The class implements various properties and methods that allow to set, partially validate and access the metadata of the book. It also contains implementations of the classes *BookJSONEncoder* and *BookJSONDecoder* that are used for serialization/deserialization of book objects when saveing or restoring  to or from a [library file](#library-file-format). The class Book is also capable of fetching metadata of a book from the internet based in its ISBN number. 


### Unit Tests

Unit tests for the functions defined in the above menstioned source files are implemented in the file *test_project.py*, *test_book_library.py*, and *test_book.py*. To run the test execute
```console
$ pytest
```
in the project folder.
