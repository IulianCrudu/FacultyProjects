#include "category.h"
#include <string.h>

const int category_length = 4;
const char* category_string[4] = { "dairy", "sweets", "meat", "fruit" };

/// Returns the integer value for a given enum member
/// \param category
/// \return -1 if category string isn't in the enum or the position of the category string in the enum
int get_category_int(char* category) {
    for(int i = 0; i < category_length; i++) {
        if(strcmp(category_string[i], category) == 0) {
            return i;
        }
    }

    return -1;
}