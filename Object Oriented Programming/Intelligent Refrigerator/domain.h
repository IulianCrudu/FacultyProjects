#pragma once

#include "category.h"

typedef struct {
    int day;
    int month;
    int year;
} Date;

typedef struct {
    char* name;
    enum product_category category;
    int quantity;
    Date* expiration_date;
} Product;

Product* create_product(char* name, enum product_category category, int quantity, int day, int month, int year);
void destroy_product(Product* product);

char* get_product_name(Product* product);
void set_product_name(Product* product, char* name);

Date* get_product_expiration_date(Product* product);
void set_product_expiration_date(Product* product, int day, int month, int year);

enum product_category get_product_category(Product* product);
