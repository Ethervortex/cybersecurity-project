# Cyber Security Base 2023 - Project I

The application 'Opeapp' has CSRF vulnerability and four security vulnerabilities from OWASP Top 10-list 2021.
Flaws are: CSRF, Injection, Broken Access Control, Identification and Authentication Failures and Security Misconfiguration

LINK: https://github.com/Ethervortex/cybersecurity-project  

The application has two users for testing:
* gollum:precious1
* frodo:precious2

It is also possible to register new accounts.

Installation instructions:
- Install Django if not yet installed: python -m pip install Django
- Clone repository: git clone https://github.com/Ethervortex/cybersecurity-project.git
- Start development server: python manage.py runserver
- Application starts at localhost:8000/opeapp

## FLAW 1 (CSRF):
https://github.com/Ethervortex/cybersecurity-project/opeapp/templates/students.html
https://github.com/Ethervortex/cybersecurity-project/opeapp/templates/courses.html
https://github.com/Ethervortex/cybersecurity-project/opeapp/templates/grades.html  
Forms in students.html, courses.html and grades.html have Cross-site Request Forgery (CSRF) vulnerabilities.  

Fix:  
Uncomment lines with {% csrf_token %} in students, courses and grades templates:  
https://github.com/Ethervortex/cybersecurity-project//opeapp/templates/students.html#L17
https://github.com/Ethervortex/cybersecurity-project/opeapp/templates/students.html#L27
https://github.com/Ethervortex/cybersecurity-project/opeapp/templates/courses.html#L17
https://github.com/Ethervortex/cybersecurity-project/opeapp/templates/grades.html#L12  
Also uncomment CsrfViewMiddleware in settings.py:  
https://github.com/Ethervortex/cybersecurity-project/cs_proj/settings.py#L47

## FLAW 2 (Injection):
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L95  
The student search in Students (i.e. Oppilaat) page uses raw SQL query where performing SQL injection is possible.
User is supposed to be able to access only those students that the user has created, but by using SQL
injection it is possible to retrieve students added by other creator. This can be done for example by
doing search:  
' OR creator_id = 1; --  
Now all students created by id=1 are listed and sensitive student information (i.e. grades) can be viewed.  

Fix:  
Comment out the whole with-section (lines 95-99 in views.py) and uncomment safe version which uses the Django ORM
(Object-Relational Mapping) to filter the data:  
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L92

## FLAW 3 (Broken Access Control):
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L238  
The registered user is supposed to be able to access only the details of students the user has created. However,
the application has Broken Access Control in student_details-view. As a consequence, the user can access any
student stored in the database by modifying URL in the browser. The last number is student_id which can be changed and
details can be accessed:  
http://localhost:8000/opeapp/student/1/  

Fix:
Comment-out broken access to student details in views.py:  
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L238  
Uncomment fix where query ensures that the student is retrieved only if the current user is the creator of that student:  
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L235

## FLAW 4 (Identification and Authentication Failures):
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L69  
The application has two flaws related to authentication. The first flaw concerns the inadequacy of the logout mechanism.
Specifically, upon selecting the logout option, the user is redirected to the login page without effectively terminating the session.
The second security concern is the absence of a defined session timeout in the application. In this scenario,
a user accessing the application from a public computer simply closes the browser and departs. Subsequently, an attacker
gains access to the same browser an hour later, finding the user still authenticated.  

Fix:
Uncomment the line 'logout(request)' in views.py:  
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L69  
Uncomment the lines 127-129 in settings.py file that specify session timeouts:  
https://github.com/Ethervortex/cybersecurity-project/cs_proj/settings.py#L127

## FLAW 5 (Security Misconfiguration):
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L10  
A superuser with insecure credentials (admin:1234) is generated programmatically in the code.  

Fix:
First, remove code which generates superuser (lines 10-22 in views.py):  
https://github.com/Ethervortex/cybersecurity-project/opeapp/views.py#L10  
Then run the development server, login to the admin interface and delete the superuser which has insecure credentials.

