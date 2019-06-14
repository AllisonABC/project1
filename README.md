# Project 1

Web Programming with Python and JavaScript

import.py creates tables books, authors, reviews, and users

application.py is a flask application that allows users to register for an account
with a username and password. Once logged in, a user can search for a book by
its isbn number, its title, or its author (including things "like" them).
Once the list of results appears, the user can click on any of the books in
the list and see information about the book, including average review and number
of reviews of the book from goodreads (uses the goodreads api). Then the user
can leave a rating and review of this book.

The flask templates include:
    index.html is the home page where a logged in user can search for a book
    login.html is the page where the user can enter login information
    register.html is the page where a user can register for the site
    error.html is the page the user is sent to if the information entered
        causes a problem; a message is displayed
    layout.html is the generic template of all the html pages
    results.html is the page listing all results of the search
    book.html is the page with details of one particular book; a user can also
        enter a rating and review on this page
    details.com is the display of json results from api/<isbn number>
