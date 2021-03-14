#include "ui.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

UI* create_ui(Service* service) {
    if(service == NULL) {
        return NULL;
    }

    UI* ui = (UI*)malloc(sizeof(UI));
    if(ui == NULL) {
        return NULL;
    }

    ui->service = service;

    return ui;
}

void destroy_ui(UI* ui) {
    if(ui == NULL) {
        return;
    }
    destroy_service(ui->service);

    free(ui);
}

void print_menu(UI* ui) {
    printf("1. Add a Product. \n");
    printf("2. Update a Product. \n");
    printf("3. Delete a Product. \n");
    printf("4. List all products. \n");
    printf("5. Display all the products containing a given string sorted by quantity. \n");
    printf("6. Display all the products containing a given string sorted by name. \n");
    printf("7. Products of a given category (or all) that expire in the next x days.\n");
    printf("8. Undo the last operation. \n");
    printf("9. Redo operation. \n");
    printf("0. Exit. \n");
}

enum product_category read_product_category_ui() {
    char category_str[25];
    enum product_category category;

    printf("Enter the category(dairy, sweets, meat, fruit): \n");
    while(1) {
        scanf("%s", category_str);
        category = get_category_int(category_str);
        if(category == -1) {
            printf("The product category entered is not valid. Please enter it again: \n");
        } else {
            break;
        }
    }

    return category;
}

void add_product_ui(UI* ui) {
    char name[256];
    int quantity, day, month, year;

    printf("Enter the name: \n");
    scanf("%s", name);
    enum product_category category = read_product_category_ui();

    printf("Enter the quantity: \n");
    while(1) {
        scanf("%d", &quantity);

        if(quantity <= 0)
            printf("Quantity can't be 0 or negative. Try again. \n");
        else
            break;
    }

    printf("Enter the expiration date(dd mm yyyy): \n");
    while(1) {
        scanf("%d %d %d", &day, &month, &year);
        if(day <= 0 || month <=0 || year <= 0 || day > 30 || month > 12)
            printf("Invalid date. Try again \n");
        else
            break;
    }

    if(add_product(ui->service, name, category, quantity, day, month, year) == 0) {
        printf("Something went wrong. :( \n");
    }
}

void update_product_ui(UI* ui) {
    char name[256];
    int quantity, day, month, year;

    printf("Enter the name: \n");
    scanf("%s", name);
    enum product_category category = read_product_category_ui();

    Product* product = get_product(ui->service, name, category);

    if(product == NULL) {
        printf("There's no product with the given name in the given category.");
        return;
    }

    printf("Enter the new quantity. Type %d to leave it as it is now. \n", product->quantity);
    while(1) {
        scanf("%d", &quantity);

        if(quantity <= 0)
            printf("Quantity can't be 0 or negative. Try again. \n");
        else
            break;
    }

    Date* expiration_date = get_product_expiration_date(product);
    printf("Enter the new expiration date. Type %d %d %d to leave it as it is now. \n", expiration_date->day, expiration_date->month, expiration_date->year);
    while(1) {
        scanf("%d %d %d", &day, &month, &year);
        if(day <= 0 || month <=0 || year <= 0 || day > 30 || month > 12)
            printf("Invalid date. Try again \n");
        else
            break;
    }

    if(update_product(ui->service, name, category, quantity, day, month, year) == 0) {
        printf("Something went wrong \n");
    }
}

void delete_product_ui(UI* ui) {
    char name[256];

    printf("Enter the name: \n");
    scanf("%s", name);
    enum product_category category = read_product_category_ui();

    Product* product = get_product(ui->service, name, category);

    if(product == NULL) {
        printf("There's no product with the given name in the given category.\n");
        return;
    }

    if(delete_product(ui->service, name, category) == 0) {
        printf("Something went wrong \n");
    }
}

void list_products_ui(UI* ui, DynamicArray* products) {
    for(int i = 0; i < products->length; i++) {
        Product* product = get_element(products, i);
        Date* expiration_date = get_product_expiration_date(product);
        const char* category = category_string[product->category];
        printf(
                "%d. %s of category %s. Quantity: %d. Expires at: %d-%d-%d. \n",
                i+1,
                get_product_name(product),
                category,
                product->quantity,
                expiration_date->day, expiration_date->month, expiration_date->year
        );
    }
    printf("\n");
}

void list_all_products_ui(UI* ui) {
    DynamicArray* products = list_products(ui->service);

    list_products_ui(ui, products);

    free(products->elements);
    free(products);
}

void display_products_containing_string_ui(UI* ui, int mode) {
    char name_string[100];

    printf("Enter the string:\n");
    getchar();
    fgets(name_string, 100, stdin);
    // fgets appends to the string even the \n character and we don't want it
    name_string[strlen(name_string) - 1] = '\0';
    DynamicArray* products = products_containing_string(ui->service, name_string, mode);
    list_products_ui(ui, products);
    free(products->elements);
    free(products);
}

void display_products_that_will_expire(UI* ui) {
    char category_str[25];
    int x_days;
    int ok = 0;
    printf("Enter the category or leave empty for all:\n");
    while(!ok) {
        getchar();
        fgets(category_str, 25, stdin);
        // fgets appends to the string even the \n character and we don't want it
        category_str[strlen(category_str) - 1] = '\0';

        if(strlen(category_str) == 0 || get_category_int(category_str) != -1)
            ok = 1;
        else
            printf("Invalid category. Enter again: \n");
    }

    printf("Enter the x days to filter for: \n");
    scanf("%d", &x_days);

    DynamicArray* products = list_expiring_products(ui->service, category_str, x_days);
    list_products_ui(ui, products);
    free(products->elements);
    free(products);
}

void load_fixtures(UI* ui) {
    char names[10][25] = {"Bread", "Chocolate", "Milk", "Milk2", "Biscuits", "Cereals", "Apple", "Orange", "Banana", "Egg"};

    for(int i=0; i<10;i++) {
        add_product(ui->service, names[i], i%4, 20 - i+2, i*3+1, i+1, 2021);
    }
}

void undo_operation_ui(UI* ui) {
    if(!undo_operation(ui->service)) {
        printf("Nothing to undo\n");
    }
}

void redo_operation_ui(UI* ui) {
    if(!redo_operation(ui->service)) {
        printf("Nothing to redo\n");
    }
}

void start_app(UI* ui) {
    int user_input;
    load_fixtures(ui);
    while (1) {
        print_menu(ui);
        printf("Enter the command number:\n");
        scanf("%d", &user_input);

        printf("User input %d \n", user_input);

        if(user_input == 1) {
            add_product_ui(ui);
        }
        else if(user_input == 2) {
            update_product_ui(ui);
        }
        else if(user_input == 3) {
            delete_product_ui(ui);
        }
        else if(user_input == 4) {
            list_all_products_ui(ui);
        }
        else if(user_input == 5) {
            display_products_containing_string_ui(ui, 1);
        }
        else if(user_input == 6) {
            display_products_containing_string_ui(ui, 2);
        }
        else if(user_input == 7) {
            display_products_that_will_expire(ui);
        }
        else if(user_input == 8) {
            undo_operation_ui(ui);
        }
        else if(user_input == 9) {
            redo_operation_ui(ui);
        }
        else if(user_input == 0) {
            printf("Bye bye \n");
            break;
        } else {
            printf("Bad command \n");
            break;
        }
    }
}