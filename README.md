## Comments ##


### This project is intended to showcase Django Rest Framework at work. The problem statement is below ###


Create a comment API using the Django REST Framework that will allow the user to submit comments associated with the below content URLs, or retrieve a list of comments associated with a content URL.

Content URLs
/Facebook
/BestBuy
/Walmart

Use the specs below to design the app with some flexibility to allow an administrator to adjust these numbers.

* All requests should go through the Django REST Framework.
* A Create (POST) end point should take the following fields and save them to the database: Username, Comment, content URL.
* A List (GET) end point would take a content URL and return a list of all previously submitted comments matching that content URL.
* Any IP Address adding more than 2 comments in 1 minute should have that request rejected and be locked out for 5 minutes.
* Any Comment that is an exact duplicate of an existing comment posted within the last 24 hours should be rejected and the originating IP Address should be locked out for 1 minute.
* The API should use a rate limiter to prevent the user from making more than 20 requests (POST and GET) per minute.

*Use sqlite database.*

*No real need to use authenticated users, the username field can be set manually*
