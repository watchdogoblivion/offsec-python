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
            127.0.0.1:FUZZ1 ->
            127.0.0.1:1 ->
            FUZZ127.0.0.FUZZ1:FUZZ1 ->
            227.0.0.2:2
