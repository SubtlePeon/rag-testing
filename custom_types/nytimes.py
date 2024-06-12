from typing import List, TypedDict

class BookResponseIsbn(TypedDict):
    isbn10: str
    isbn13: str

class BookResponseBuyLink(TypedDict):
    name: str
    url: str

class BookResponseBook(TypedDict):
    rank: int
    rank_last_week: int
    weeks_on_list: int
    asterisk: int
    dagger: int
    primary_isbn10: str
    primary_isbn13: str
    publisher: str
    description: str
    # Decimal string
    price: str
    title: str
    author: str
    contributor: str
    contributor_note: str
    # URL string
    book_image: str
    book_image_width: int
    book_image_height: int
    # URL string
    amazon_product_url: str
    age_group: str
    # Can be empty
    book_review_link: str
    # Can be empty
    first_chapter_link: str
    # Can be empty
    sunday_review_link: str
    article_chapter_link: str
    # Fields: isbn10 (str), isbn13 (str)
    isbns: List[BookResponseIsbn]
    # Fields: name (str), url (str)
    buy_links: List[BookResponseBuyLink]
    book_uri: str

class BookResponseResults(TypedDict):
    list_name: str
    list_name_encoded: str
    # Date string (YYYY-MM-DD)
    bestsellers_date: str
    # Date string (YYYY-MM-DD)
    published_date: str
    published_date_description: str
    # Date string, can be empty
    next_published_date: str
    previous_published_date: str
    display_name: str
    normal_list_ends_at: int
    updated: str
    books: List[BookResponseBook]

class BookResponse(TypedDict):
    status: str
    copyright: str
    num_results: int
    # Datetime string (looks like ISO 8601 / RFC 3339 format)
    last_modified: str
    results: BookResponseResults
