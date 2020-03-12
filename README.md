# Crypto_projet

WORK DONE BY Théophile Freixa & Ronan le tilly      and also Mathieu de Reynal & Samuel Uzan

Exam : https://vqhuy.github.io/teaching/crypto/project?fbclid=IwAR2G5p4KW-x2Mrk1-C102QnReWPyCaw7PDTp7l0i6dqDjazrSS57GMNLdmI

Warning :  Sometimes it works sometime it doesn’t with no reason

We add the ImportAccounts.py file wich contains the functions we have created to change the database file
We add comments in the each file


Theorical questions : 

1/- To safely store the passwords we coul hash them with a strong hash function like SHA-256 and then compare it with the hash of the password received in input. 

2/-We should use authentificated encryption, because it's the most secure way to transfer data. Moreover no need for the bank to communicate the common password. 
In different way, we can also use AES>128, TDES min dbl length keys, RSA > 2048 bits, ElGamal >1024 bits taht are actually used by banks.

The problem of CBC is that a one-bit change to the ciphertext causes complete corruption of the corresponding block of plaintext, and inverts the corresponding bit in the following block of plaintext, but the rest of the blocks remain intact.
