# BinaryPythonBackground
 Python program to make a binary encoded backgroud pattern

important: !!! due to this project making use of transparancy all source files must be png or zip filled with png

 2 modes: 
 1. directory search. If the 4th argument is missing the program will automatically search for a "patterns" folder in the pwd, if it is found it will geneate a background for any image tile it finds png or zip. 
    - Ex: python3 backgroundGen.py 2070 1200 binary.txt 
    - this will generate many 2070 px wide, 1200 pix tall images based on the binary string in binary.txt with base tiles based on all the tiles/tile sets found in ./patterns
 2. single item. if you include a path to a specific image tile png or zip the program will only generate a background with that image
    - Ex: python3 backgroundGen.py 2070 1200 binary.txt ./patterns/circuit.zip 
    - this will generate an 2070 px wide, 1200 pix tall image based on the binary string in binary.txt with just the circuit.zip file as a set of base tiles. 

2 types of generation: 
1. single tile, with just a png file each binary 1 will have that tile placed, and any binary 0 will be blank.
2. multi tile, with a zip file the program looks for a set of images titled to match the below description and places them where other binary "pixels" surround them in the correct patterns. 
    - possible files for multi direction zip
    - directions will be assigned a binary number based on:
    - 1111 = urld 
    - meaning something that has up, right and downwould be 1101 or 13
    - 0.png  - 0b0000 - isl - island, no connections
    - 1.png  - 0b0001 - do  - down only 
    - 2.png  - 0b0010 - lo  - left only 
    - 3.png  - 0b0011 - ld  - left and down 
    - 4.png  - 0b0100 - ro  - right only
    - 5.png  - 0b0101 - rd  - right and down
    - 6.png  - 0b0110 - rl  - right and left
    - 7.png  - 0b0111 - rld - right, left, and down 
    - 8.png  - 0b1000 - uo  - up only 
    - 9.png  - 0b1001 - ud  - up and down
    - 10.png - 0b1010 - ul  - up and left 
    - 11.png - 0b1011 - uld - up, left, and down
    - 12.png - 0b1100 - ur  - up and right 
    - 13.png - 0b1101 - urd - up, right, and down
    - 14.png - 0b1110 - url - up, right, and left
    - 15.png - 0b1111 - all - all directions 
