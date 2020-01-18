import json
with open("responses.json") as f:
    data = json.load(f)

import matplotlib.pyplot as plt
plt.show(block = True)

print(data)

#Score Function

def match (a,  b):
    if(((a[u'gender'] in b[u'gender_preferences']) == False) or (b[u'gender'] in a[u'gender_preferences']) == False):
        return 0
    else:
        temp = 0
        for i in range(10):
            temp += abs(a[u'answers'][i] - (b[u'answers'])[i])
        fscore = a[u'f'] + b[u'f']/2
        year_diff = abs(a[u'year'] - b[u'year'])
        temp += 2*year_diff
        return 1- abs(fscore - (1 - temp/46.0))

#Making histogram of distribution of scores for each pair of people where the
#score was NOT equal to 0 (because having those scores made it difficult to see the distribution)

my_list = []

for i in data.keys():
    for j in data.keys():
        if(i != j and i < j and match(data[i], data[j]) != 0):
            my_list.append(match(data[i], data[j]))

plt.hist(my_list, color = 'blue', edgecolor = 'red', bins = 40)

#histogram for distribution from point of view of one specific person

spec_list = []

for i in data.keys():
    if(match(data[u'344'], data[i]) !=0):
        spec_list.append(match(data[u'344'], data[i]))

plt.hist(spec_list, color = 'blue', edgecolor = 'red', bins = 40)
plt.show()
