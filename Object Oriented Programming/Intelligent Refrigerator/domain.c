#include "domain.h"
#include <stdlib.h>
#include <string.h>

/// Creates a new product
/// \param name
/// \param category
/// \param quantity
/// \param day
/// \param month
/// \param year
/// \return The newly created product's pointer
Product* create_product(char* name, enum product_category category, int quantity, int day, int month, int year) {
    Product* product = (Product*) malloc(sizeof(Product));

    if(product == NULL) {
        return NULL;
    }


    product->name = NULL;
    product->expiration_date = NULL;
    product->category = category;
    product->quantity = quantity;

    set_product_name(product, name);
    set_product_expiration_date(product, day, month, year);

    return product;
}

/// Destroys a product, deleting everything related to it from the memory
/// \param product
void destroy_product(Product* product) {
    if(product == NULL) {
        return;
    }

    if(product->name) {
        free(product->name);
    }

    if(product->expiration_date) {
        free(product->expiration_date);
    }

    free(product);
}

/// Returns the product's name
/// \param product
/// \return The product name
char* get_product_name(Product* product) {
    if(product == NULL) {
        return NULL;
    }

    return product->name;
}

/// Sets the product's name in memory and attaches the name to the product
/// \param product
/// \param name The product name
void set_product_name(Product* product, char* name) {
    if(product->name != NULL) {
        free(product->name);
        product->name = NULL;
    }


    product->name = (char*)malloc(sizeof(char) * (strlen(name) + 1));
    strcpy(product->name, name);
}

/// Returns the expiration date of the product
/// \param product
/// \return The expiration date
Date* get_product_expiration_date(Product* product) {
    if(product == NULL) {
        return NULL;
    }

    return product->expiration_date;
}

/// Sets the product's expiration date in memory and attaches the expiration date to the product
/// \param product
/// \param day
/// \param month
/// \param year
void set_product_expiration_date(Product* product, int day, int month, int year) {
    if(product == NULL) {
        return;
    }

    if(product->expiration_date) {
        free(product->expiration_date);
        product->expiration_date = NULL;
    }

    Date* date = (Date*)malloc(sizeof(Date));

    date->day = day;
    date->month = month;
    date->year = year;

    product->expiration_date = date;

}

/// Returns the product's category
/// \param product
/// \return category
enum product_category get_product_category(Product* product) {

    if(product == NULL) {
        return -1;
    }

    return product->category;
}