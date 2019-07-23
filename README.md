# awkg

`awkg` is an `awk` like utility using modern day python language.
`awk` is amazingly simple, fast and quite handy. However, its domain specific constrain 
sometimes get in our way. `awkg` follows the steps of  `awk`'s design (including its convention for name😉)
and exposes full power of the modern day python. 
Python's large set of off-the-shelf existing libraries can of course be imported and used. 

# Installation 
```bash

# Install from pypy 
$ pip install awkg

# Install from github
$ pip install git+https://github.com/thammegowda/awkg.git

```

# CLI usage: 

```
$ awkg -h 
usage: awkg [-h] [-i INP] [-o OUT] [-F FS] [-OFS OFS] [-ORS ORS]
            [-b BEGIN_SCRIPT] [-e END_SCRIPT] [-im IMPORTS] [-it INIT_PATH]
            [-v]
            inline_script

awkg is an awk-like text-processing tool powered by python language

positional arguments:
  inline_script         Inline python script

optional arguments:
  -h, --help            show this help message and exit
  -i INP, --inp INP     Input file path; None=STDIN
  -o OUT, --out OUT     Output file path; None=STDOUT
  -F FS, -FS FS, --field-sep FS
                        the input field separator. Default=None implies white
                        space
  -OFS OFS, --out-field-sep OFS
                        the out field separator. Default=None implies same as
                        input FS.
  -ORS ORS, --out-rec-sep ORS
                        the output record separator. Default=None implies same
                        as input RS.
  -b BEGIN_SCRIPT, --begin BEGIN_SCRIPT
                        BEGIN block. initialize variables or whatever
  -e END_SCRIPT, --end END_SCRIPT
                        END block. Print summaries or whatever
  -im IMPORTS, --import IMPORTS
                        Imports block. Specify a list of module names to be
                        imported.Semicolon (;) is the delimiter. Ex:
                        json;numpy as np
  -it INIT_PATH, --init INIT_PATH
                        The rc file that initializes environment.Default is
                        $HOME/.awkg.py
  -v, --version         show program's version number and exit
                        
```
# Example

### Compute mean and std of words per sequence
```bash
 
cat data/train.src | awkg -b 'arr=[]; import numpy as np' 'arr.append(NF)' \
   -e 'arr=np.array(arr); print(f"{NR} lines from {FNAME}, mean={arr.mean():.2f}; std={arr.std():.4f}")'
```
### Filter records
```
# use print() explicitely 
cat data/train.src  | awkg  'if NF >= 25: print(*R)' 

Assign boolean expression to special variable RET to trigger implicit print 
cat data/train.src  | awkg  'RET = NF >= 25'

# print respects the OFS value
cat data/train.src  |  awkg  'if NF >= 25: print(NR, NF)' -OFS='\t'
```

## Special Variables
+ `NF`  : Number of fields
+ `NR`  : Record number 
+ `R`   : An array having all the columns of current record.
+ `R0`  : analogous to `$0` it stores the input line before splitting into `R`; since python does
 not permit `$` in the identifiers, it is renamed as `R0`
+ `RET` : When this variable is set to Truth value of `true` implicit `print(*R)` is triggered
+ `FS` : Input Field separator
+ `OFS` : Output Field separator; Unless explicitly set, `OFS=FS`
+ `ORS` : Output Record separator
+ `RS` (Currently Not in use)
+ `_locals` , `_globals` - all variables in local and global scope

You are allowed to use any valid python identifiers, than the above variables

## Default import modules 
These modules are imported by default
+ `sys`
+ `os`
+ `re`
+ `from pathlib import Path`


## Author:
+ [Thamme Gowda](https://twitter.com/thammegowda)

## Related tools
+ [pawk](https://github.com/alecthomas/pawk) similar to this repository, slightly different implementation.
+ [gawk](https://www.gnu.org/software/gawk/manual/gawk.html) GNU awk
 

