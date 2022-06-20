# Name: Taylor Garrison
# Description: This script contains a HashMap class that creates a hash table ADT, using a Dynamic Array to store its
# data as HashEntry objects. Collisions are handled by open addressing so that values with the same indices are moved
# to an empty index using quadratic probing. Removed values are considered tombstones, and are removed when the HashMap
# is resized or when a new value is placed in their spot.


from hash_map_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes two parameters - a string representing a key and an object representing a value. Put the key,value pair
        into the HashTable, resizing if necessary. Returns None.
        """

        # Check the table load and double capacity if >= .5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Calculate the index
        index = self._hash_function(key) % self._capacity

        # If there is nothing or a tombstone at the index, add the pair and increase size
        if self._buckets[index] is None or self._buckets[index].is_tombstone:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1

        # If the key exists, update the value
        elif self._buckets[index].key == key:
            self._buckets[index].value = value

        # Use quadratic probing to find an empty, tombstone, or matching key index and add the pair
        else:
            initial_index = index
            for num in range(1, self._capacity):
                index = (initial_index + num ** 2) % self._capacity
                if self._buckets[index] is None or self._buckets[index].is_tombstone:
                    self._buckets[index] = HashEntry(key, value)
                    self._size += 1
                    return
                elif self._buckets[index].key == key:
                    self._buckets[index] = HashEntry(key, value)
                    return

    def table_load(self) -> float:
        """
        Takes no parameters. Calculates and returns the load factor of the table.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Takes no parameters. Calculates and returns the number of empty buckets in the hash map.
        """

        # Set a counter and search for empty or tombstone indices, adding to the counter when found
        counter = 0
        for num in range(self._capacity):
            if self._buckets[num] is None or self._buckets[num].is_tombstone:
                counter += 1

        # Return the count
        return counter

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes an integer representing a new capacity for the table as a parameter. Resizes the table and copies over
        all old values, skipping tombstones. Returns None.
        """

        # Check if the new capacity is valid
        if new_capacity < 1 or new_capacity < self._size:
            return

        # Create and allocate a new DA
        new_da = DynamicArray()
        for _ in range(new_capacity):
            new_da.append(None)

        # Save the capacity, size, and DA of the original table and reassign each variable to the new table
        old_capacity = self._capacity
        old_da = self._buckets
        old_size = self._size
        self._buckets = new_da
        self._capacity = new_capacity
        self._size = 0

        # Add old values to the new table, skipping tombstones
        for num in range(old_capacity):
            if old_da[num] and not old_da[num].is_tombstone:
                self.put(old_da[num].key, old_da[num].value)

        # Set size to size of old array
        self._size = old_size

    def get(self, key: str) -> object:
        """
        Takes a string representing a key as a parameters and attempts to find the value associated with it. Returns
        the value if found, otherwise returns None.
        """

        # Calculate the index
        index = self._hash_function(key) % self._capacity

        # Return None if there is nothing there
        if self._buckets[index] is None:
            return None

        # Return value if the keys match, and it is not a tombstone
        elif self._buckets[index].key == key and not self._buckets[index].is_tombstone:
            return self._buckets[index].value

        # Perform quadratic probing, returning the appropriate value as above
        else:
            initial_index = index
            for num in range(1, self._capacity):
                index = (initial_index + num * num) % self._capacity
                if self._buckets[index] is None:
                    return None
                elif self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                    return self._buckets[index].value
            return None

    def contains_key(self, key: str) -> bool:
        """
        Takes a string representing a key as a string and attempts to find it in the table. Returns True if found,
        otherwise returns False.
        """

        # Use get to determine if the key exists
        if self.get(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Takes a string representing a key as a parameter and attempts to remove it from the table. If found, set the
        key,value pair to be a tombstone, otherwise does nothing. Returns None.
        """

        # Calculate the index
        index = self._hash_function(key) % self._capacity

        # Do nothing if nothing is at index
        if self._buckets[index] is None:
            return None

        # If key matches and isn't already a tombstone, set tombstone property to True and decrement size
        elif self._buckets[index].key == key:
            if self._buckets[index].is_tombstone:
                return None
            self._buckets[index].is_tombstone = True
            self._size -= 1

        # Perform quadratic probing if necessary until index fits one of the above situations and perform appropriate
        # actions
        else:
            initial_index = index
            for num in range(1, self._capacity):
                index = (initial_index + num * num) % self._capacity
                if self._buckets[index] is None:
                    return None
                elif self._buckets[index].key == key:
                    if self._buckets[index].is_tombstone:
                        return None
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
        return None

    def clear(self) -> None:
        """
        Takes no parameters. Clears the table of any values. Returns None
        """

        # Create new DA, allocate space, set size to 0
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        Takes no parameters. Generates a Dynamic Array containing all the keys in the table. Returns the DA.
        """

        # Create a key array
        key_arr = DynamicArray()

        # Iterate through table, adding keys that exist and aren't tombstones
        for num in range(self._capacity):
            if self._buckets[num] is not None and not self._buckets[num].is_tombstone:
                key_arr.append(self._buckets[num].key)

        # Return key array
        return key_arr


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        if i == 11:
            print(' ')
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())
    print('test concluded')

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        if m.empty_buckets() == 30:
            print(' ')
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())