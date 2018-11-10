a = 10
b = 20
c = a+b


def MakeListWithBracket(strList):
    lenth = len(strList)
    if strList[0]=="[" and strList[lenth-1]=="]":
        strList = strList.replace("[" , "")
        strList = strList.replace("]" ,"")
        newList = strList.split(" ")
    else:
        print("wrong syntax")
    return newList

def MakeListWithOutBracket(strList):
    lenth = len(strList)
    newList = strList.split(" ")
    return newList


strList = "a b c d"
List = MakeListWithOutBracket(strList)
print(List)
