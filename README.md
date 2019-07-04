# OverlapperSlapper
Given a list of Reddit submissions, the script will output a list of Reddit users who have either created or commented in a submission and the frequency at which they appear in the submissions.

The script reads the list of submissions from the "links.txt" file and there must be one link per line. The "links.txt" file must be located in the same directory the script is located. The output file "overlappers.csv" will be written to the same location as well.
In order to use the script, [PRAW](https://praw.readthedocs.io/) is required as well as completing the authentication in "praw_config.py".
