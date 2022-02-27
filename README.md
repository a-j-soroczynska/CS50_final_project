# Web application for restaurant *La Porta Aperta*
#### Video Demo:  https://youtu.be/Kv4u7Zr7WNo
#### Description:
For my final project I created a web application for the restaurant. The restaurant (fictional and totally made up by me) serves italian cuisine and its name is *La Porta Aperta*, which means *The Open Door* in italian.
The website is a web-based application using HTML, CSS, Flask with Python and SQL. I also used Bootstrap libraries and Google Maps Platform. All of the html files extend the basic template created in *layout.html*, use style from *styles.css*, database *restaurant.db* and follow the instructions from *application.py*.

My application contains several modules:
1. About us
This section is just a simple static web page displaying only information about the restaurant. It was written in *about.html* file.
2. Menu
This one also is just a page (*menu.html*) with no interaction possible, but it takes from the database what dishes are on the menu at the moment and uses a for loop to display them. 
3. Delivery
This is the most complex module in my application - it allows the user to order food with delivery. 
It starts with *delivery.html* file, which displays all of the dishes that are on the menu at the moment. This information is taken from the database and displayed using a for loop. The user can choose dishes he or she wants to order and, one by one, add them to the cart. After adding every single dish, the user gets an alert with positive information and can go to see the cart. Checking the cart is also possible at every moment by clicking on a cart icon at the top of the dishes list.
Cart page was written in *cart.html* and shows what dishes were already added to the cart and how many there were. It is also possible to change the number of dishes by clicking plus or minus.
After clicking Order button, the user goes to *adress.html*. This page contains a delivery address form in which all of the fields are required. 
The last page of this module is *summary.html*, which is basically summarization of all information - chosen dishes and delivery address. If the user decides that all of the information is correct, clicks a Confirm and order button and gets a positive alert. This is the end of the food ordering process - order is added to the database and the user can place another one or go back to the home page.
4. Reservations
In the reservation section the user can book a table in the restaurant. To do so, he or she must complete the form written in *reservation.html*. After that the application checks in the database if there are any free tables for the chosen date, time and number of people. If so, the booked table is added to the database and the user gets a positive alert. If not, the information in alert is negative and the user is asked to choose another date.
5. Opinions
In this part the user can add an opinion about the restaurant or check out opinions already added by other people. To allow that I created file *opinions.html* with a form and a for loop that displays opinions taken from the database. After submitting the form, the user gets an alert that tells if the opinion was added successfully or not.
6. Contact
This module contains two parts: contact information (with map localization added by Google Maps Platform) and contact form. In the contact form the user can send a message to the restaurant. After submitting the form, the user gets an alert that tells if the message was sent successfully or not. It was written in *contact.html* file.

