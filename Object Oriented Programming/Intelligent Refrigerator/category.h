#pragma once

enum product_category {
    dairy,
    sweets,
    meat,
    fruit
};

const int category_length;
const char* category_string[4];

int get_category_int(char* category);