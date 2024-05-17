# TRAVEL PAGE

## Video Demo

<https://youtu.be/ILW2e7kBqZM>

## Description

This TRAVEL PAGE is my final project for CS50 !!
I love to travel so much that I decided to create my travel journal site.
For the main content, I created a page to record my own past trips and a page to list countries I would like to visit in the future.
Both pages hold data on the year, season, region, country, and people I want to go with.
The trip record page allows users to easily upload photos of their memories, and a modal window allows users to zoom in on the photos.
Also, the flags shown in the index.html display are some of the countries I have visited in the past.
I am looking forward to updating this list in the future as I would like to visit more countries myself !!

## Each Page's Description

####　layout.html:
This is the html for the general framework layout.
Javascript is described in wish.html and travel.html.
The Javascript is designed to work in conjunction with Region and Country in the list, narrowing down and displaying countries in the region selected by Region.

####　error.html:
When an error occurs in any of the items, this page informs the user of the nature of the error.
The error message and the error message are updated for each field. The error message can be a confirmation of the entered information, such as a password that is different from the registered one, a username or password that is different, or a notification of a required field, such as region not selected, birthday not entered, and so on.

####　index.html:
This page is the home of the TRAVEL PAGE.
Since the world is the stage for travel, I have set up a large picture of the earth and scattered national flags.
After login, index.html becomes the top page, but if someone who is not logged in visits this page, they are automatically redirected to the login page because the login information cannot be read from the session.

####　register.html:
This page is the user account creation page.
Validations have been set up so that all fields are required for each item.
Passwords are stored in a hash rather than directly in the DB, which is more secure than storing them directly in the DB.

####　login.html:
This page is for users who have already created a user in register.html to log in.
Users can log in by entering the username, date of birth, and password used during user registration.
Once logged in, the login information is stored in the session, so the login state is maintained.
After login, index.html becomes the top page.

####　change_password.html:
This page is for users to change their password.
You can change your password by entering your current password, confirmation password, and new password.
If the password is successfully changed, the date of the update is saved in the DB, and the system redirects the user to index.html.

####　wish.html:
This page is for registering a wish list of countries you would like to visit in the future.
The year that can be registered is set so that only dates in the future can be saved. Therefore, the current year is saved as THIS YEAR and set as a minimum year to SELECT, so you cannot register years before this year.
The registered wish list is displayed at the bottom of the form.
Flag image paths are stored in travel.db, so it is possible to display the flags of countries in the list stored in the wish page and the travel page.

####　travel.html:
This page lists the countries that users have visited in the past.
The years that can be registered are only those after the year of your birth.
A photo of one of the memories can also be saved and enlarged in a modal window.
Since the image paths of the flags are stored in travel.db, it is possible to display the flags of the countries in the list stored in the wish page and travel page.

#### design:
The overall design was designed to be simple, easy to read, and use friendly colors.
The wish list and register list are tables, and the table rows change color when the mouse hovers over each row, making it easy for users to see which row they are checking.
Both the flag and the earth used on the page were illustrated to express the soft image of the site.
