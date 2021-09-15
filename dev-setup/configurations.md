1. Install VSCode

2. Go to "Extensions" in VSCode and Add:
   "Python Extension Pack"
   "Prettier - Code formatter"

3. Run cli commands:
   /usr/bin/python -m pip install -U "pylint<2.0.0" --user
   /usr/bin/python -m pip install -U yapf --user

   See sample [settings](settings.json)

##### Optional

1. For debugging, prints debugging is A Okay.
   However, if you want to use python debugger for speed:
   Click "Run ad Debug" and generate launch.json
   See sample [lauch file](launch.json)
   Once setup, click Run and Debug.
   In the drop down select the script, and play.
   Reference: https://code.visualstudio.com/docs/editor/debugging

2. Go to "Extensions" in VSCode and Add:
   "Getter/Setter Generator" => 1.3.0 -> Newest 1.3.1/1.4.0 are buggy
