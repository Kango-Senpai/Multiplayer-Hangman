myFile = open("list1.txt",'r+')
newFile = open("list2.txt",'w')
sortedWords = []
length = int(input("Length: "))
for line in myFile:
    if len(line.strip()) >= length:
        sortedWords.append(line)
newFile.writelines(sortedWords)

myFile.close()
newFile.close()
print("Sorting complete!")