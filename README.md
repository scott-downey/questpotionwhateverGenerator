# questpotionwhateverGenerator
Generates Whatever you want at (weighted) random

## How to call it
Try out this function call and follow the description given in the src/* files.
`./plotg.py -l start task reward`
the -l parameters are the different files from which random entries are selected

## How to write src-files
`_` stands for another random entry from the written file in the src files
Example: `SomeQuest_SomeFile`

`|` stands for weighted. The standard weight is 100
Example: `SomeQuest_SomeFile|32`
