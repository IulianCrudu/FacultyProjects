def sum_even_numbers_on_even_position(array, left, right):
    """
    The chip and conquer algorithm that will compute the needed sum
    Input:
        array - the array with numbers for which we have to find out the sum
        left - the left most index at which we should start counting
        right - the right most index at which we should end counting

    Output:
        The sum of even elements found on even position for the given indices
    """

    # If left is bigger than right then we finished computing for the given chunk of the array
    if left > right:
        return 0

    s = 0
    if left % 2 == 0 and array[left] % 2 == 0:
        # This means the element from the left index is even and the left index is also even
        s = array[left]

    return s + sum_even_numbers_on_even_position(array, left+1, right)


def find_sum(array):
    """
    Input:
        array - the array with numbers for which we have to find out the sum
    Output:
        The sum of even numbers found on even positions or None if none such numbers exists in the array
    """
    sum = sum_even_numbers_on_even_position(array, 0, len(array))

    # If sum is 0 then there are no such numbers so we return None
    if sum == 0:
        return None
    return sum


def test_sum_even_numbers_on_even_position():
    assert sum_even_numbers_on_even_position([1], 0, 1) == 0
    assert sum_even_numbers_on_even_position([2], 0, 1) == 2
    arr = [2, 2, 4, 5, 6, 4, 13, 4, 10]
    assert sum_even_numbers_on_even_position(arr, 0, len(arr)) == 22
    assert sum_even_numbers_on_even_position([1], 1, 0) == 0


def test_find_sum():
    assert find_sum([1]) is None
    assert find_sum([2]) == 2
    arr = [2, 2, 4, 5, 6, 4, 13, 4, 10]
    assert find_sum(arr) == 22
    assert find_sum([1]) is None


test_sum_even_numbers_on_even_position()
test_find_sum()

