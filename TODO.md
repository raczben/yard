## Destination folder of generated sources.
The start (=default) should be as simple as possible, user has a descriptor file (ie.: *.yard) in a
given folder. The user will expect the result in this folder at the first time. Then  (designing
more complicated modules) user wants to set precisely  the destination files, to suit them into his
structure.

 - Default: relative to descriptor file:
    - ./sw/<modulename>.c/h
    - ./hdl/<modulename>_<subblock>.vhd/v
    - ./tcl/<modulename>.tcl
    - ...
  - TODO:
    - should be set file level.
    - company default is important at this property.

## Should be Copied regutil to destination folder?
The start should be as simple as possible, if we copy utils, user dont need to set include folders, 
but then (designing more complicated modules) utils should be copied only once, so user should
disable/set the way of the copy.

 - Default: Yes
 - TODO: Should be optional: User shold decide to copy

New flags introduced:
    targets -> software -> copyUtil

## dword size handling 


## Generators and settings:
 - Several files closely linked (header + source; pif + core) therefore one generator class/task should
   be able to generate multiple files.
 - Modularity requres to add/set new generator classes.