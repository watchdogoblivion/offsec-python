### This file is for referencing possible test suites to create in the future.

### It can also be used to check against changes.

##### _FileFuzzer:_

1. JSON Post
2. Form Post
3. File Upload
4. Fuzzing endpoint, header, and body individually
5. Multiple Fuzzes at once
6. Multiple Fuzzes across endpoint, header, and body in no particular
   order.
7. Fuzzing a value that occurs in the original string multple times:
   For instance, fuzzing 127.0.0.1:FUZZ1 with ports 1-65535
   Ensuring that the request goes through correctly during swaps.
   Example failure to avoid:
   127.0.0.1:FUZZ1 -> 127.0.0.1:1 ->
   FUZZ127.0.0.FUZZ1:FUZZ1 -> 227.0.0.2:2

##### _OracleCredConverter:_

1. Test cred converson ll
2. Test cred converson lu
3. Test cred converson ul
4. Test cred converson uu

##### _FileEncoder:_

1. Test base64 encoding
2. Test all three url encoding variations
3. Test base64 and url encoding combination

##### _EncodingViewer:_

1. Test encode from works with default encode to
2. Test that both encoding to and from work together
3. Test multiple encoding variations from built in encodings list

##### _CharacterConverter:_

1. Test new character succesfully swaps.
2. Test new character swaps with line increments
3. Test new character swaps with word increments
4. Test new character gets upper cased
5. Test new character gets lower cased
6. Test multiple combinations of the above
