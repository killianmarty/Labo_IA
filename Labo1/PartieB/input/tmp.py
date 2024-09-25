f = open("file.txt", 'r')
text = ""
i=0
a=0
for line in f.readlines():
    if(line.startswith("Difficulty")):
        text+=line
        file = open('input' + str(i) + '.txt', 'w')
        file.write(text)
        file.close()
        text = ""
        i+=1
        a=0
    else:
        text += line