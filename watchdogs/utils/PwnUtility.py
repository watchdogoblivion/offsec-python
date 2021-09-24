# author: WatchDogOblivion
# description: TODO
# WatchDogs Pwn Utility

from pwnlib.util.packing import pack

# p64 and p32 method in pwnlib is dynamically generated, so pylint does not recognize it.
# This method is a way to replicate it using its base method

def p64(number): #type: (int) -> bytes
    return pack(number, 64)

def p32(number): #type: (int) -> bytes
  return pack(number, 32)