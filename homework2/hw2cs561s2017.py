#------ CSCI 561 Homework #2 - Ahmad Fallahpour
import copy as mycopy

def Decoder(ID):
    SplitID = ID.split('.')
    GuestID = int(SplitID[1])
    TableID = int(SplitID[2])
    return [SplitID[0], GuestID, TableID]

def RemoveRepeated(Assignment):
    list1 =  mycopy.deepcopy(Assignment)
    list2 = []
    for a in list1:
        if a not in list2:
            list2.append(a)
    return list2

def GuestAssignment(Assignment):
    Guest = []
    Table = []
    for i in range(0, len(Assignment)):
        Decode = Decoder(Assignment[i][0])
        if Assignment[i][1] == 1:
            Guest.append(Decode[1])  # Save the assigned Guest ID
            Table.append(Decode[2])  # Save the assigned Table ID

    GuestSorted = []
    TableSorted = []
    for i in range(0, M):
        for j in range(0, len(Guest)):
            if i == Guest[j] and i not in GuestSorted:
                GuestSorted.append(Guest[j])
                TableSorted.append(Table[j])
    Guest1 = [x + 1 for x in GuestSorted]
    Table1 = [y + 1 for y in TableSorted]
    return [Guest1, Table1]

def SearchPureSimilar(sentencePS,X):
    Decode = Decoder(X)
    indexX=0
    indexZ=0
    for i in range(0,len(sentencePS)):
        for j in range(0,len(sentencePS[i])):
            NewDecode = Decoder(sentencePS[i][j])
            if indexX>=1 and indexZ>=1:
                return ['X','False']
            if NewDecode[1] == Decode[1] and NewDecode[2] == Decode[2]:
                if NewDecode[0]=='X':
                    indexX += 1
                else:
                    indexZ += 1
    if indexX>=1 and indexZ==0:
        return ['X','True']
    elif indexX==0 and indexZ>=1:
        return ['Z','True']
    else:
        return ['Z','False']

def SentenceUpdate(sentenceUC, UnitClause, Value):
    Decode = Decoder(UnitClause)
    sentenceUpdate = mycopy.deepcopy(sentenceUC)
    index = []
    Flag = 0
    for i in range(0,len(sentenceUC)):
        for j in range(0,len(sentenceUC[i])):
            NewDecode = Decoder(sentenceUC[i][j])
            if NewDecode[1]==Decode[1] and NewDecode[2]==Decode[2]:
                # print [i,j,sentenceUC[i][j]]
                if (NewDecode[0]==Decode[0] and Value==1) or (NewDecode[0]!=Decode[0] and Value==0):
                    index.append(i)
                elif (NewDecode[0]==Decode[0] and Value==0) or (NewDecode[0] != Decode[0] and Value == 1):
                    if len(sentenceUC[i])==1:
                        Flag = 'False'
                        return [sentenceUpdate, Flag]
                    else:
                        del sentenceUpdate[i][j]
    sentenceUpdate = [v for i, v in enumerate(sentenceUpdate) if i not in index]
    return [sentenceUpdate, Flag]

def Find_Unit_Clause(sentenceD,symbolsD, AssignmentD):
    sentenceUC = mycopy.deepcopy(sentenceD)
    symbolsUC = mycopy.deepcopy(symbolsD)
    AssignmentUC = mycopy.deepcopy(AssignmentD)
    Flag = 0
    for i in range(0,len(sentenceUC)):
        if len(sentenceUC[i])==1:
            UnitClause = sentenceUC[i][0]
            Decode = Decoder(UnitClause)
            if Decode[0]=='X':
                AssignmentUC.append([symbolsUC[Decode[1]][Decode[2]], 1])
            else:
                AssignmentUC.append([symbolsUC[Decode[1]][Decode[2]], 0])

    for i in range(0,len(AssignmentUC)):
        [sentenceUC , Flag] = SentenceUpdate(sentenceUC, AssignmentUC[i][0], AssignmentUC[i][1])
        if Flag=='False':
            return [sentenceUC, AssignmentUC, Flag]
    return [sentenceUC, AssignmentUC, Flag]

def Find_Pure_Symbol(sentenceD,symbolsD, AssignmentD, M, N):
    sentencePS = mycopy.deepcopy(sentenceD)
    symbolsPS = mycopy.deepcopy(symbolsD)
    AssignmentPS = mycopy.deepcopy(AssignmentD)

    Flag = 0
    for i in range(0,M):
        for j in range(0,N):
            [letter, state] = SearchPureSimilar(sentencePS,symbolsPS[i][j])
            if state=='True':
                if letter=='X':
                    AssignmentPS.append([symbolsPS[i][j], 1])
                else:
                    AssignmentPS.append([symbolsPS[i][j], 0])

    AssignmentPS = RemoveRepeated(AssignmentPS)
    for i in range(0,len(AssignmentPS)):
        [sentencePS , Flag] = SentenceUpdate(sentencePS, AssignmentPS[i][0], AssignmentPS[i][1])
        if Flag=='False':
            return [sentencePS, AssignmentPS, Flag]

    return [sentencePS, AssignmentPS, Flag]

def RestSymbols(AssignmentD, symbolsD, M, N):
    [Guest, Table] = GuestAssignment(AssignmentD)
    if len(Guest)==M:
        return 'Done'
    else:
        AssignmentRS = mycopy.deepcopy(AssignmentD)
        AssignmentRSset = RemoveRepeated(AssignmentRS)
        AllTable = range(N)
        AllGuest = range(M)
        Total = []
        for i in range(0,M): Total.append(range(N))
        index=[]
        for i in range(0, len(AssignmentRSset)):
            Decode = Decoder(AssignmentRSset[i][0])
            if AssignmentRSset[i][1]==1:
                index.append(Decode[1]) #Save the assigned Guest ID
            else:
                if Decode[1] in index:
                    w = 'Do nothing'
                else:
                    Total[Decode[1]][Decode[2]]=-1

        for j in range(0,len(Total)):
            aaa = Total[j]
            bbb = [i for i, x in enumerate(aaa) if x == -1]
            Total[j] = [v for i, v in enumerate(Total[j]) if i not in bbb]

        AllGuest = [v for i, v in enumerate(AllGuest) if i not in index]

        if len(AllGuest)>0:
            NextAssignment = symbolsD[AllGuest[0]][Total[AllGuest[0]][0]]
        else:
            NextAssignment = 'Done'

    return NextAssignment

def DPLL(sentence, symbols, Assignment, M, N):
    sentenceD = mycopy.deepcopy(sentence)
    symbolsD = mycopy.deepcopy(symbols)
    AssignmentD = mycopy.deepcopy(Assignment)

    [sentenceD, AssignmentD, Flag] = Find_Pure_Symbol(sentenceD, symbolsD, AssignmentD, M, N)
    if Flag == 'False':
        return ['No', AssignmentD]

    [sentenceD, AssignmentD, Flag] = Find_Unit_Clause(sentenceD, symbolsD, AssignmentD)
    if Flag == 'False':
        return ['No', AssignmentD]

    NextAssignment = RestSymbols(AssignmentD, symbolsD, M, N)
    if NextAssignment == 'Done':
        return ['Yes', AssignmentD]
    else:
        AssignmentD1 = mycopy.deepcopy(AssignmentD)
        AssignmentD2 = mycopy.deepcopy(AssignmentD)
        AssignmentD1.append([NextAssignment, 1])
        AssignmentD2.append([NextAssignment, 0])
        XXXX = mycopy.deepcopy(AssignmentD1)
        YYYY = mycopy.deepcopy(AssignmentD2)
        [status1, AssignmentD1] = DPLL(sentenceD, symbolsD, XXXX, M, N)
        [Guest, Table] = GuestAssignment(AssignmentD1)
        if status1=='Yes':
            AssignmentD = mycopy.deepcopy(AssignmentD1)
            return ['Yes', AssignmentD]

        [status2, AssignmentD2] = DPLL(sentenceD, symbolsD, YYYY, M, N)
        [Guest, Table] = GuestAssignment(AssignmentD2)
        if status2=='Yes':
            AssignmentD = mycopy.deepcopy(AssignmentD2)
            return ['Yes', AssignmentD]

        if status1=='No' and status1=='No':
            return ['No', AssignmentD]

#------ Open the file and read the content
f = open('./Samples test cases/input1.txt','r')
Content = f.read().split()
M = int(Content[0]) #number of guests
N = int(Content[1]) #number of tables

symbols = []
for i in range(0,M):
    symbolsTable = []
    for j in range(0,N):
        symbolsTable.append("X.{q}.{w}".format(q=i, w=j))
    symbols.append(symbolsTable)

#------ Initial Constraints
sentence = []
for i in range(0,M):
    clause = []
    for j in range(0,N):
        clause.append("X.{q}.{w}".format(q=i,w=j))
        for k in range(j+1,N):
            sentence.append(["Z.{q}.{w}".format(q=i,w=j), "Z.{q}.{w}".format(q=i,w=k)])
    sentence.append(clause)
#------ Relationship Constraints
R = [[0] * M  for _ in range(M)] #relationship matrix
ConstraintsNum = (len(Content)-2)/3
for i in range(0,int(ConstraintsNum*3),3):
    Relation = Content[i+4]
    G1 = int(Content[i+2])-1
    G2 = int(Content[i+3])-1
    if Relation == 'F':
        R[G1][G2] = 1
        R[G2][G1] = 1
    else:
        R[G1][G2] = -1
        R[G2][G1] = -1

for i in range(0,M):
    for j in range(i+1, M):
        if R[i][j]==1:
            for k in range(0,N):
                sentence.append(["Z.{q}.{w}".format(q=i, w=k), "X.{q}.{w}".format(q=j, w=k)])
                sentence.append(["X.{q}.{w}".format(q=i, w=k), "Z.{q}.{w}".format(q=j, w=k)])
        elif R[i][j]==-1:
            for k in range(0, N):
                sentence.append(["Z.{q}.{w}".format(q=i, w=k), "Z.{q}.{w}".format(q=j, w=k)])

Assignment=[]
[status, Assignment] = DPLL(sentence, symbols, Assignment, M, N)
[Guest, Table] = GuestAssignment(Assignment)

file = open("./Samples test cases/output.txt", "w")
if status=='No':
    file.write("no")
else:
    file.write("yes\n")
    for i in range(0,len(Guest)):
        file.write("%d %d\n" % (Guest[i],Table[i]))
file.close()