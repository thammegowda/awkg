# awkg

`awkg` is a `awk` like utility using modern day python language.
`awk` is amazingly simple, fast and quite handy. However, its domain specific constrain 
sometimes get in our way. 
`awkg` follows the steps of  `awk`'s design (including its name convention😉)
and exposes full power of the modern day python. 
Python's large set of off-the-shelf existing libraries can of course be imported and used. 

# Todo: 

```
$ alias awkg="$PWD/awkg/awkg.py"
 $ awkg -h
usage: __main__.py [-h] [-i INP] [-o OUT] [-F FS] [-OFS OFS] [-RS RS]
                   [-ORS ORS] [-b BEGIN_SCRIPT] [-e END_SCRIPT] [-im IMPORTS]
                   [-it INIT_PATH]
                   inline_script

positional arguments:
  inline_script         Inline python script

optional arguments:
  -h, --help            show this help message and exit
  -i INP, --inp INP     Input file path; None=STDIN (default: None)
  -o OUT, --out OUT     Output file path; None=STDOUT (default: None)
  -F FS, -FS FS, --field-separator FS
                        the input field separator. Default=None implies white
                        space (default: None)
  -OFS OFS, --out-field-separator OFS
                        the out field separator. Default=None implies same as
                        input FS. (default: None)
  -RS RS, --record-separator RS
                        the input record separator. Default=None implies
                        universal newline. (default: None)
  -ORS ORS, --out-record-separator ORS
                        the output record separator. Default=None implies same
                        as input RS. (default: None)
  -b BEGIN_SCRIPT, --begin BEGIN_SCRIPT
                        BEGIN block. initialize variables or whatever
                        (default: None)
  -e END_SCRIPT, --end END_SCRIPT
                        END block. Print summaries or whatever (default: None)
  -im IMPORTS, --import IMPORTS
                        Imports block. Just specify the module names to be
                        imported. Semicolon (;) is the delimiter. Ex:
                        json;numpy as np (default: None)
  -it INIT_PATH, --init INIT_PATH
                        The rc file that initializes environment (default:
                        /Users/tg/.awkg.py)
                        
                        
```
# Example
(This is the earliest example; The `awkg` command be setup do to `python -m awkg`)
```bash
alias awkg="$PWD/awkg/awkg.py"
```

### Compute mean and std of words per sequence
```python
 

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
+ `R0`  : analogous to `$0` it stores the input line before splitting into `R`; since python doesnt support $ in identifiers, renamed to R0
+ `RET` : When this variable is set to Truth value of `true` implicit `print(*R)` is triggered
+ `FS` : Input Field separator
+ `OFS` : Output Field separator; Unless explicitly set, `OFS=FS`
+ `ORS` : Output Record separator
+ `RS` (Currently Not in use)
+ `_locals` , `_globals` - all variables in local and global scope

You are allowed to use any valid python identifiers, than the above variables


## Author:
+ [Thamme Gowda](https://twitter.com/thammegowda)

## Related tools
[pawk](https://github.com/alecthomas/pawk) similar to this repository, slightly different implementation.
[gawk](https://www.gnu.org/software/gawk/manual/gawk.html) GNU awk 


