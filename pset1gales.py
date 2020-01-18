import json
with open("responses.json") as f:
    data = json.load(f)

#Re-defined the score function without referring to gender, because
#I just used that the first 500 people were male and last 500 were female

def match (a,  b):
    temp = 0
    for i in range(10):
        temp += abs(a[u'answers'][i] - (b[u'answers'])[i])
    fscore = a[u'f'] + b[u'f']/2
    year_diff = abs(a[u'year'] - b[u'year'])
    temp += 2*year_diff
    return 1- abs(fscore - (1 - temp/46.0))

gs = {}
waitlist = []
nonwaitlist = []
scorelistb = {}

#Applied Gale-Schapley below; first made a list of lists storing the scores between every boy-girl pair

for b in data.keys():
    temp0 = 0
    temp1 = 0
    if b < u'500':
        temp = []
        for g in data.keys():
            if g >= u'500':
                temp.append(match(data[b], data[g]))
        scorelistb[b] = temp

#used the list of lists created above to add pairings to a dict called 'gs' (which takes a person ID as key and has person ID as value)
#compared the scores between each boy and his first choice to the score
#between the first choice girl and her current match (if there was one); set the
#match of the girl to be the boy with the higher score and put whoever was rejected into a 'waitlist'

for b in data.keys():
    if b < u'500':
        temp0 = 0
        temp1 = 0
        waitlist.append(b)
        for g in data.keys():
            if(g >= u'500'):
                if (scorelistb[b])[int(g) - 500] > temp0:
                    temp0 = (scorelistb[b])[int(g) - 500]
                    temp1 = g
        if temp1 not in gs.keys():
            gs[temp1] = [temp0, b]
            waitlist.remove(b)
        else:
            if temp0 >= gs[temp1][0]:
                waitlist.append(gs[temp1][1])
                waitlist.remove(b)
                gs[temp1] = [temp0, b]
        (scorelistb[b])[int(temp1) - 500] = -1

#Used the waitlist created from the first "round of proposals" to repeat the process only
#with boys on the waitlist, updating the waitlist each time. Continued this until waitlist was empty

while len(waitlist) > 0:
    for boy in waitlist:
        temp0 = 0
        temp1 = 0
        for girl in data.keys():
            if(girl >= u'500'):
                if (scorelistb[boy])[int(girl) - 500] > temp0:
                    temp0 = (scorelistb[boy])[int(girl) - 500]
                    temp1 = girl
        (scorelistb[boy])[int(temp1) - 500] = -1
        if temp1 not in gs.keys():
            gs[temp1] = [temp0, boy]
            waitlist.remove(boy)
        else:
            if temp0 >= gs[temp1][0]:
                waitlist.append(gs[temp1][1])
                waitlist.remove(boy)
                gs[temp1] = [temp0, boy]

counter = 0
gs1 = {}

#defined function for getting key from value in a dictionary

def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key
    return "key doesn't exist"

#created new dict storing only the boy-girl pairs from "gs", excluding the score

for g in gs:
    gs1[g] = (gs[g])[1]

print(gs1)

#checked that the pairings made in "gs" dict were stable; this was done by taking each
#pair of boys and girls, and seeing if the score between them was higher than both the
#score between the boy and his current match and the score between the girl and her current match.
#Counter would measure how many such pairs there were, and since counter was 0, there were no such unstable pairs.

for boi in data.keys():
    if boi < u'500':
        for gal in data.keys():
            if gal >= u'500':
                temp = match(data[boi], data[gal])
            if gal in gs.keys() and gs1[get_key(gs1, boi)] in gs.keys():
                if temp > (gs[gs1[get_key(gs1, boi)]])[0] and temp > (gs[gal])[0]:
                    counter +=1

print(counter)
