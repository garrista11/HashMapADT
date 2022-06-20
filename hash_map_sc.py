# Name: Taylor Garrison
# Description: This script contains a HashMap class that creates a hash table ADT that utilizes linked lists to store
# its data. Collisions are handled by chaining so that values with the same indices are stored in the same linked list.


from hash_map_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        Takes two parameters; a string that represents a key and an object that represents a value. Puts the key,
        value pair into the hash map. If the key already exists the value associated with it is updated. Returns None.
        """

        # Calculate the index
        index = self._hash_function(key) % self._capacity

        # Insert the pair if the linked list is empty
        if self._buckets[index].length() == 0:
            self._buckets[index].insert(key, value)
            self._size += 1

        # Iterate through the linked list and insert or add a new node
        else:
            for node in self._buckets[index]:
                if node.key == key:
                    node.value = value
                    return
            self._buckets[index].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Takes no parameters. Calculates and returns the number of empty buckets in the hash map.
        """

        # Set a counter and count the number of linked lists with a length of 0
        counter = 0
        for num in range(self._capacity):
            if self._buckets[num].length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        Takes no parameters. Calculates and returns the load factor of the table.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Takes no parameters. Clears the hash map of any contained data. Returns None.
        """

        # Set buckets to a new array and add the appropriate number of linked lists
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Reset the size
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes an integer as a parameter that represents the new capacity for the hash map. Updates the hash map to
        have a new capacity and copies over all old data in the new hash map. Returns None.
        """

        # Return if the new capacity is too small
        if new_capacity < 1:
            return

        # Create a new array and add the new number of linked lists
        new_da = DynamicArray()
        for _ in range(new_capacity):
            new_da.append(LinkedList())

        # Save the capacity and old DA and reassign buckets, capacity and size
        old_capacity = self._capacity
        old_buckets = self._buckets
        self._buckets = new_da
        self._capacity = new_capacity
        self._size = 0

        # Add the values from the old array to the new array using put
        for num in range(old_capacity):
            if old_buckets[num].length() != 0:
                for node in old_buckets[num]:
                    self.put(node.key, node.value)


    def get(self, key: str) -> object:
        """
        Takes a string representing a key and attempts to return the value associated with it. If the key does not
        exist, returns None.
        """

        # Determine the index
        index = self._hash_function(key) % self._capacity

        # Search for the key, returning None if isn't found
        if self._buckets[index].length() == 0:
            return None
        else:
            for node in self._buckets[index]:
                if node.key == key:
                    return node.value
            return None

    def contains_key(self, key: str) -> bool:
        """
        Takes a string representing a key and attempts to find that key in the hash map. Returns True if it was found,
        otherwise returns False.
        """

        # Use get to find if the key exists
        if self.get(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Takes a string representing a key and attempts to remove the key,value pair from the hash map. Does nothing if
        key does not exist. Returns None.
        """

        # If the hash map contains the key, calculate its index, remove it, and decrement size
        if self.contains_key(key):
            index = self._hash_function(key) % self._capacity
            self._buckets[index].remove(key)
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Takes no parameters. Creates a Dynamic Array containing all the keys in the hash map. Returns the DA.
        """

        # Create an array and iterate through non-empty linked lists, adding each key to the DA
        key_arr = DynamicArray()
        for num in range(self._capacity):
            if self._buckets[num].length() != 0:
                for node in self._buckets[num]:
                    key_arr.append(node.key)

        # Return the key array
        return key_arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes a Dynamic Array as a parameter. Uses the hash map class to find the mode of the dynamic array (if there are
    multiple modes they are all recorded). Returns a new Dynamic Array containing the mode(s) and the frequency.
    """

    # Create a map
    map = HashMap(da.length() // 3, hash_function_1)

    # Iterate through the DA, adding objects as keys with a value of 1 (starting frequency)
    for num in range(da.length()):
        if not map.contains_key(str(da[num])):
            map.put(str(da[num]), 1)

        # If the map already has an object as a key, update its value to be one higher
        else:
            current_freq = map.get(str(da[num]))
            current_freq += 1
            map.put(str(da[num]), current_freq)

    # Create an array of the keys and an array for recording modes and a temporary frequency tracker
    keys = map.get_keys()
    mode_da = DynamicArray()
    total_freq = -1

    # Iterate through the key array and use the values stored in the map to determine the mode
    for num in range(keys.length()):
        temp_freq = map.get(keys[num])

        # If the frequency of a value is more than the current frequency, reset the mode array and add the value
        if temp_freq > total_freq:
            mode_da = DynamicArray()
            mode_da.append(keys[num])
            total_freq = temp_freq

        # If they are equal, add the value to the mode array
        elif temp_freq == total_freq:
            mode_da.append(keys[num])

    # Return the mode array and the frequency of the mode(s)
    return mode_da, total_freq




# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
