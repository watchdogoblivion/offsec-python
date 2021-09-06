## Below are the standards I have set for the code ##

#### _DRY_ ####
    Do not repeat yourself. 
    Whenever possible duplicate code fragments are extracted into new
    methoda or variablea to be reused.

    Additional references:
    https://en.wikipedia.org/wiki/Don%27t_repeat_yourself

#### _KISS_ ####
    Keep the code simple. 
    I know python has some cool expressions like comprehensions, but abusing 
    nesting them makes it unnecessarily strenous to read.
    This also goes for deep nesting if/else statements.
    If the repeated nesting is neccessary, then possible extraction should be
    considered.
    Plain and simple, there is no need for high cognitive complexity.

    In a few commits, the code was using alot general objects, such as dicts, tuples
    etc. While there is nothing technically wrong with this, it because strenous to
    read. Also, it makes it easy to overlook better approaches since there is so much
    focus following the repeated use of general objects i.e (v[0], v[a[1]]),{"c":"d"})
    Using OOP to represent these objects and forming relationships helps makes 
    everything easier to read, manaage, and enahance.

    Additional references:
    https://en.wikipedia.org/wiki/KISS_principle

#### _OOP_ ####
    Object Oriented Principles
    These principles help refine the code and make it easier to maintain, extend, debug etc.

    Additional references:
    https://en.wikipedia.org/wiki/Object-oriented_programming

#### _Typing_ ####
    I understand the appeal that people have with the "Any" and "Object" types across
    various languages especially considering type erasure.
    However, the downside to these can become quite apparent while
    scaling and debugging large scale apps.
    Even for small scale apps, I am not a fan.
    Typing helps define strict rules whenever possible which makes it quite clear what
    an object is suppose to hold and what a method is supposed to excpect at all times
    which helps REDUCE(not stop) the risk of random events occurring AND makes it much
    easier to follow the flow.
    This is probably why it is one of the pillars of OOP (even though it is a minor one).

    Additional references:
    https://www.tutorialspoint.com/object_oriented_analysis_design/ooad_object_oriented_principles.htm

#### _Modularity/Modular Programming_ ####
    Ensure that the methods perform a single aspect of the entire
    intended functionality. This makes it easier to both debug and 
    write unit tests for various areas and aspects of the code.

    Additional reference:
    https://en.wikipedia.org/wiki/Modular_programming

#### _Documentation_ ####
    Code should be self-documenting. The fields and function names
    should accurately and clearly display what they are and what 
    they do. This way anyone can clearly follow, modify, and/or debug
    the code easier.
    Comments should be added to anycomplex method to make it clear what
    is occurring.

    Additional reference:
    https://en.wikipedia.org/wiki/Self-documenting_code

#### _Linting_ ####
    Enforcing linting for code quality.

    The IDE/Code editor is VSCode.

    The library used for python linting is pylint.

See all the configurations in the [Dev Setup folder](dev-setup)

#### _Formatting_ ####
    I am enforcing a formatting standard.
    This way the code will always be readable and follow PEP standards.

    The IDE/Code editor is VSCode.

    The library used for python formatting is yapf.

    For markdown and json formatting, prettier is used.

See all the configurations in the [Dev Setup folder](dev-setup)

#### _Custom_ ####
    I have explictly set the standard, that all methods should aim
    for no more than 30 lines of code unless absolutely neccessary.
    If a method is longer than 30 lines, there is a good chance that
    the block can have methods extracted from it to modularize,
    simply functional perception and/or increase readability.
    50 lines should be the absolute upper limit. Any more than that
    and one may possibly be introducing uncessary complexity to the
    method and should definitely consider extraction.

#### _To implement_ ####
    Tests need to added for quick regression testing.
    For now TestCases.MD was created as a possible future reference.