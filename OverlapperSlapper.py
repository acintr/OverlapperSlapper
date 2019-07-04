"""
Overlapper Slapper
Given a list of Reddit submissions, the script will output a list of Reddit users
who have either created or commented in a submission and the frequency at which
they appear in the submissions. The script reads the list of submissions from the
"links.txt" file and there must be one link per line. The "links.txt" file must be
located in the same directory the script is located. The output file "overlappers.csv"
will be written to the same location as well.
"""
from praw_config import config
import praw
from praw.models import MoreComments
from os import getcwd

users = {}
temp_u = []
links = []


def add_user(user):
    if not user:
        return
    if user in users:
        users.__setitem__(user, users[user]+1)
    else:
        users.__setitem__(user, 1)


def rec_child(parent):
    for kid in parent:
        if isinstance(kid, MoreComments):
            continue
        if kid.author not in temp_u:
            temp_u.append(kid.author)
        rec_child(kid.replies)


def merge_sort(arr):
    if len(arr) > 1:
        m = int(len(arr) / 2)
        l = arr[:m]
        r = arr[m:]
        merge_sort(l)
        merge_sort(r)
        i = j = k = 0
        while i < len(l) and j < len(r):
            if l[i][1] > r[j][1]:
                arr[k] = l[i]
                i += 1
            else:
                arr[k] = r[j]
                j += 1
            k += 1
        while i < len(l):
            arr[k] = l[i]
            i += 1
            k += 1
        while j < len(r):
            arr[k] = r[j]
            j += 1
            k += 1


reddit = praw.Reddit(
    user_agent=config['user_agent'],
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    username=config['username'],
    password=config['password']
)

try:
    links_file = open('links.txt', 'r')
    links = links_file.readlines()
    links_file.close()
except FileNotFoundError:
    exit('Error: "links.txt" file not found! Make sure the file exists.')
except IOError:
    exit('IOError while reading "links.txt"')

for l in links:
    try:
        submission = reddit.submission(url=l)
        temp_u.append(submission.author)
        rec_child(submission.comments)
        for u in temp_u:
            add_user(u)
        temp_u.clear()
    except:
        continue

user_list = []
for u in users:
    user_list.append((u.name, users[u]))

merge_sort(user_list)

# for u in user_list:
#     print(u[1], u[0])

try:
    out = open('overlappers.csv', 'w')
    for u in user_list:
        out.writelines(u[0]+','+str(u[1])+'\n')
    out.close()
    print('Output file location:', getcwd()+'/overlappers.csv')
except IOError:
    exit('IOError while writing results...')

print(len(users), 'users found.')
