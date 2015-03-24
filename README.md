Extract-MD-A
=================
Scan all the 10ks in the same folder and extract MD&A

How to use:
1. create ./MD&A folder
2. run the script

Rationale:
- split docments based on keywords 'item'
- found out text segments between 'Item 7' and 'Item 7A'
- score those segments by its length and contains
- selected best one

* This methods is quite robust in our test.

Feature:
- High accuracy for most 10ks
- Debug mode support: scan(filename, debug = True)

Known Bugs:
- doesn't work when the 10k didn't include Item 7A
