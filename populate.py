import re
import sqlite3


def get_database_connection():
    try:
        conn = sqlite3.connect('bible.db')
    except sqlite3.Error as error:
        print("Error occurred - ", error)
    return conn


def parse_line(line):
    # pattern = r'^([a-zA-Z]+)(\d+):(\d+)$'
    pattern = r'([0-9]*[a-zA-Z]+)\s*([0-9]+)\s*:\s*([0-9]+)'

    # split the line of text at the first space
    split_string = line.split(' ', 1)
    string, text = tuple(split_string)

    # find book, chapter, and verse
    match = re.match(pattern, string)

    try:
        book_name = match.group(1)
    except Exception:
        print(line)
        exit(0)
    chapter_number = int(match.group(2))
    verse_number = int(match.group(3))

    # print(f"Book: {book_name}, Chapter: {chapter_number}, Verse: {verse_number}")
    return book_name, chapter_number, verse_number, text


def populate_verses():
    """ The database already has the books table. Read the source
     file and get the verses and insert into the database verses table. """
    # connect to the database
    conn = get_database_connection()
    crs = conn.cursor()

    # get the list of book_ids, etc from the books table
    books = {}
    sql = "SELECT id, abbrev, name FROM books"
    for book in crs.execute(sql):
        books[book[1]] = [book[0], book[2]]

    # read the whole bible text
    with open(r'kjv.txt', 'r') as f:
        for line in f.readlines()[1:]:
            abbrev, chapter, verse, text = parse_line(line)
            text.strip('\n ')
            book_id = books[abbrev][0]
            crs.execute("INSERT OR IGNORE INTO verses (chapter, number, text, book_id) VALUES (?, ?, ?, ?)",
                        (chapter, verse, text, book_id))

    # finally, commit than disconnect from the database
    conn.commit()
    conn.close()


populate_verses()