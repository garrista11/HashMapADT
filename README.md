# HashMapADT
Contains script for creating HashMap's using different hashing techniques

This is a program that allows for the creation of two HashMap data structures that use different systems for storing data. One uses a separate chaining technique, in
which each 'bucket' in the map is a linked list, and any data with the same hashed key is entered into the same linked list. The other uses open addressing, in which an attempt is made to enter new data into its corresponding bucket based on its hashed key. If the bucket is filled, the script will perform quadratic probing in order to find an empty bucket in which to place the new data. Various methods are implemented for performing different actions using the two HashMaps, such as clearing them, adding new data, removing data, and searching for specific data. 

Both HashMap data structures need the 'hash_map_include' file in order to run correctly.
