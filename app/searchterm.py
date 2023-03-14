import re


def convert_book_token(book_token):
    # Use regular expression to match tokens starting with one or more digits
    match = re.match(r'^(\d+)(.*)', book_token)
    if match:
        # If there is a match, extract the number and the rest of the token
        number = match.group(1)
        rest = str(match.group(2)).title()
        # Return the formatted string
        return f"{number} {rest}"
    else:
        # If there is no match, return the original token
        return book_token


def check_pattern(token):
    """
    classify the search token to determine if it is a verse reference OR text string for a verse.
    For example: 2Sam20:12, Ex20.11, Exo20.1, Exo20:11 or 'for in six days'
    """
    pattern = r'([0-9]*[a-zA-Z]+)\s*([0-9]+)\s*[\.\:]\s*([0-9]+)'
    if re.match(pattern, token):
        # find book, chapter, and verse
        match = re.match(pattern, token)

        book_abbrev = match.group(1)
        chapter_number = int(match.group(2))
        verse_number = int(match.group(3))

        return 'REF', {'book': book_abbrev, 'chapter': chapter_number, 'verse': verse_number}
    else:
        # TXT pattern
        return 'TXT', None