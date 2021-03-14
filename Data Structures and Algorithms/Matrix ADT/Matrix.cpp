#include "Matrix.h"
#include <exception>
using namespace std;


Matrix::Matrix(int nrLines, int nrCols) {
	if(nrLines <= 0 || nrCols <= 0) {
	    throw exception();
	}

	this->lines = nrLines;
	this->columns = nrCols;
	this->length = 0;
	this->sparse_matrix = new TElem*[3];
	for(int i = 0; i < 3; i++)
	    this->sparse_matrix[i] = new TElem[this->lines * this->columns];
}
// Theta(1)

int Matrix::nrLines() const {
	return this->lines;
}
// Theta(1)


int Matrix::nrColumns() const {
	return this->columns;
}
// Theta(1)


TElem Matrix::element(int i, int j) const {
    if(i >= this->lines || i < 0) {
        throw exception();
    }

    if(j >= this->columns || j < 0) {
        throw exception();
    }

	for(int column = 0; column < this->length; column++) {
	    if(this->sparse_matrix[0][column] > i)
	        break;
	    if(this->sparse_matrix[0][column] == i && this->sparse_matrix[1][column] == j)
	        return this->sparse_matrix[2][column];
	}
	return NULL_TELEM;
}
// Best case: Theta(1), Worst Case: Theta(length) => General complexity: O(length)

void Matrix::add(int index, int i, int j, TElem e) {
    if(i >= this->lines || i < 0) {
        throw exception();
    }

    if(j >= this->columns || j < 0) {
        throw exception();
    }

    if(index < 0 || index > this->length) {
        throw exception();
    }

    for(int column = this->length; column >= index; column--) {
        this->sparse_matrix[0][column+1] = this->sparse_matrix[0][column];
        this->sparse_matrix[1][column+1] = this->sparse_matrix[1][column];
        this->sparse_matrix[2][column+1] = this->sparse_matrix[2][column];
    }

    this->sparse_matrix[0][index] = i;
    this->sparse_matrix[1][index] = j;
    this->sparse_matrix[2][index] = e;
    this->length++;
}
// O(length)

void Matrix::remove(int index) {
    if(index < 0 || index >= this->length) {
        throw exception();
    }

    for(int j = index; j < this->length; j++) {
        this->sparse_matrix[0][j] = this->sparse_matrix[0][j+1];
        this->sparse_matrix[1][j] = this->sparse_matrix[1][j+1];
        this->sparse_matrix[2][j] = this->sparse_matrix[2][j+1];
    }

    this->length--;
}
// O(length)

TElem Matrix::modify(int i, int j, TElem e) {
	int index = 0;
	int found = 0;

	while(index < this->length) {
	    if(this->sparse_matrix[0][index] > i) {
	        found = 0;
	        break;
	    }

	    if(this->sparse_matrix[0][index] == i && this->sparse_matrix[1][index] > j) {
	        found = 0;
	        break;
	    }

	    if(this->sparse_matrix[0][index] == i && this->sparse_matrix[1][index] == j) {
	        found = 1;
	        break;
	    }

	    index++;
	}

	if(found) {
        int old_value = this->sparse_matrix[2][index];
	    if(e == 0)
            this->remove(index);

        if(e != 0)
            this->sparse_matrix[2][index] = e;

        return old_value;

	}

	if(e != 0)
	    this->add(index, i, j, e);

	return NULL_TELEM;
}
// O(length)

