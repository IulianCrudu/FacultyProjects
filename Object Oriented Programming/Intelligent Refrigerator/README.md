# Intelligent Refrigerator
CRUD application written in C language with specifications and unit test coverage.
**No memory leaks**.

- Vector structure with specific operations using a dynamically allocated array is used.
- Uses modular programming.
- Source code is specified and includes tests for all non-UI functions
- The program does not leak memory!
- Uses a layered architecture for the application (domain, repository, controller, UI). User interface, domain and data access elements will be stored in different modules. The user interface module only contains the user interface part.
- Has 10 entries available at application startup.


### Intelligent Refrigerator Story
The company *“Home SmartApps”* have decided to design a new intelligent refrigerator. Besides the hardware, they need a software application to manage the refrigerator. Each **Product** that the fridge can store has a `name`, a `category` (one of `dairy, sweets, meat or fruit`), a `quantity` and an `expiration date`. The software application will provide the following functionalities:\
**(a)** Add, delete or update a product. A product is uniquely identified by name and category. If a product that already exists is added, its quantity will be updated (the new quantity is added to the existing one).\
**(b)** Display all products whose name contains a given string (if the string is empty, all products from the refrigerator are considered), and show them sorted ascending by the existing quantity.\
**(c)** Display all products of a given category (if the category is empty, all types of food will be considered) whose expiration dates are close (expire in the following `X` days, where the value of `X` is user-provided).\
**(d)** Provide multiple undo and redo functionality. Each step will undo/redo the previous operation performed by the user.
