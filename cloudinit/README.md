# CloudInit

## What is CloudInit

https://help.ubuntu.com/community/CloudInit

## How to use
Put your userdata input in `userdata` with the formats you like, then run:

    ./write-mime-multipart userdata/** -o combined-userdata.txt

then use the `combined-userdata.txt` on demand.
For example:

    OS_USER_DATA_FILE=/path/to/combined-userdata.txt

