import requests
import random

numVerses = 3

class Line:
    tag = ""
    line = ""
    endword = ""

def getRhymes(word):
    r = requests.get('https://www.rhymezone.com/r/rhyme.cgi?Word=' + word + '&org1=syl&org2=l&org3=y&typeofrhyme=perfect')
    rtext = r.text
    rhymes = []
    for line in rtext.splitlines():
        if "More ideas" in line: break
        if "<a class=\"d r\" href=\"" in line or "<a class=r href=\"" in line:
            word = line.split(">")[1].split("<")[0]
            word = word.replace("&nbsp;"," ")
            word = word.split(" ")[-1]
            if word == "": continue
            rhymes.append(word)
    return rhymes

def randBlock(lines):
    restart = True
    rhymingLines = []
    while restart:
        restart = False
        randnum = random.randint(0,totlines - 1)
        randLine = allLines[randnum]
        rhymes = getRhymes(randLine.endword)
        firstLine = randLine.line
        endWord = randLine.endword
        foundRhymingLines = 0
        for line in allLines:
            if line.endword in rhymes:
                #print("Found a rhyme: " + line.endword)
                rhymingLines.append(line)
                foundRhymingLines += 1
        if foundRhymingLines < lines:
            restart = True
    alreadyDone = []
    returnRhymes = []
    while True:
        randnum = random.randint(0,len(rhymingLines) - 1)
        #print(str(randnum))
        #print(alreadyDone)
        if randnum in alreadyDone: continue
        alreadyDone.append(randnum)
        returnRhymes.append(rhymingLines[randnum])
        if len(alreadyDone) >= lines: break
    return returnRhymes
     
file = "kanye.txt"
f = open(file, "r", encoding="utf8")
currenttag = ""
totlines = 0
allLines = []
chorusTags = []
verseTags = []
for line in f:
    line = line.strip()
    if line == "": continue
    if "[" in line:
        currenttag = line
        if "[Verse" in line and ":" in line:
            versetag = line.split(":")[1].replace(']','')
            verseTags.append(versetag)
        if "[Chorus" in line and ":" in line:
            chorustag = line.split(":")[1].replace(']','')
            chorusTags.append(chorustag)
        continue
    thisLine = Line()
    thisLine.tag = currenttag
    thisLine.line = line.split('(')[0]
    thisLine.endword = thisLine.line.split(' ')[-1]
    thisLine.endword = thisLine.endword.replace('.','').replace('?','').replace('-','').replace('!','').replace(',','').replace('"','').replace('\'','')
    allLines.append(thisLine)
    totlines+=1

chorus = randBlock(8)
verse = []
for i in range(0,numVerses):
    verse.append(randBlock(4) + randBlock(4))

for i in range(0,numVerses):
    randnum = random.randint(0,len(verseTags) - 1)
    versetag = verseTags[randnum]
    print("Verse " + str(i+1) + ":" + versetag + "\n")
    for line in verse[i]:
        print(line.line)
    print("")
    if (i+1) % 2 == 0:
        randchorusnum = random.randint(0,len(chorusTags) - 1)
        chorustag = chorusTags[randchorusnum]
        print("Chorus:" + chorustag)
        for line in chorus:
            print(line.line)
        print("")

f.close()