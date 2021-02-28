#------ CSCI 561 Homework #3 - Ahmad Fallahpour

from timeit import default_timer
start = default_timer()

import copy as mycopy

def Decode(EV):
    e = []
    value = []
    for i in range(0, len(EV)):
        x = EV[i].split('.')
        e.append(x[0])
        value.append(x[1])
    return [e, value]

def SortVar(QU, Var):
    sortedQU = []
    [e, value] = Decode(QU)
    sort = sorted(e, key=Var.index)
    for i in range(0, len(QU)):
        for j in range(0, len(QU)):
            if sort[i] == e[j]:
                sortedQU.append(QU[j])
    return sortedQU

def VarEvidenceUpdate(QQQ, Var, Evidencess, Decision):
    QQ = mycopy.deepcopy(QQQ)
    if QQ[0] == 'MEU':
        for i in range(1,len(QQ)):
            Chert20 = list(QQ[i])
            if len(Chert20) == 1 and Chert20[0]!='|':
                QQ[i] = ''.join([Chert20[0],'.','+'])

    del QQ[0]
    while '|' in QQ: QQ.remove('|')
    [e, value] = Decode(QQ)
    index = []
    indexE = []
    for i in range(0, len(e)):
        if e[i] in Decision:
            index.append(i)
            for j in range(len(Evidencess)):
                if e[i] == Evidencess[j][0]:
                    indexE.append(j)

    e = [v for i, v in enumerate(e) if i not in index]
    Evidencess = [v for i, v in enumerate(Evidencess) if i not in indexE]
    sort = sorted(e, key=Var.index)
    if len(sort) > 0:
        YY = Var.index(sort[-1])
        UpdatedVar = Var[0:YY+1]
        UpdatedEvidencess = Evidencess[0:YY+1]
    else:
        UpdatedVar = Var
        UpdatedEvidencess = Evidencess

    return [UpdatedVar, UpdatedEvidencess]

def FindVarParentDecision(Evidencess):
    Chert2 = mycopy.deepcopy(Evidencess)
    Var = []
    Parent = []
    Decision = []
    for i in range(0,len(Chert2)):
        if 'decision' in Chert2[i]:
            Decision.append(Chert2[i][0])
        else:
            Chert3=Chert2[i][0].split(' ')
            Var.append(Chert3[0])
            if '|' in Chert3:
                while ' ' in Chert3: Chert3.remove(' ')
                while '|' in Chert3: Chert3.remove('|')
            Parent.append(Chert3)
    return [Var, Parent, Decision]

def ReadingQueries(Queries):
    Chert4 = mycopy.deepcopy(Queries)
    PolishedQ = []
    for i in range(0, len(Chert4)):
        Chert5 = Chert4[i].split('(')
        PolishedQ.append([Chert5[0]])
        Chert6 = list(Chert4[i])
        while '(' in Chert6: Chert6.remove('(')
        while ')' in Chert6: Chert6.remove(')')
        while ' ' in Chert6: Chert6.remove(' ')
        # print Chert6
        if Chert5[0] == 'P' or Chert5[0] == 'EU':
            for j in range(0,len(Chert6)):
                if Chert6[j] == '=':
                    PolishedQ[i].append("{q}.{w}".format(q=Chert6[j-1], w=Chert6[j+1]))
                elif Chert6[j] == '|':
                    PolishedQ[i].append('|')

        elif Chert5[0] == 'MEU':
            Chert16 = list(Chert5[1])
            while ')' in Chert16: Chert16.remove(')')
            while ' ' in Chert16: Chert16.remove(' ')
            while ',' in Chert16: Chert16.remove(',')
            if '|' in Chert16:
                YY = Chert16.index('|')
                for k in range(0, YY):
                    PolishedQ[i].append(Chert16[k])
                PolishedQ[i].append('|')
                Chert17 = Chert16[YY+1:]
                for j in range(0, len(Chert17)):
                    if Chert17[j] == '=':
                        PolishedQ[i].append("{q}.{w}".format(q=Chert17[j - 1], w=Chert17[j + 1]))
            else:
                for k in range(0, len(Chert16)):
                    PolishedQ[i].append(Chert16[k])
    return PolishedQ

def FindParent(child, QU, Parent):
    potentialPar = mycopy.deepcopy(QU)
    potentialPar.remove(child)
    RealParents = []
    RealParentsName = []
    Chert7 = child.split('.')
    par = []
    for i in range(0,len(potentialPar)):
        Chert8 = potentialPar[i].split('.')
        par.append(Chert8[0])
    for i in range(0, len(Parent)):
        lp = len(Parent[i])
        if Chert7[0] == Parent[i][0] and lp > 1:
            for j in range(1, lp):
                if Parent[i][j] in par:
                    RealParents.append(potentialPar[par.index(Parent[i][j])])
                    RealParentsName.append(par[par.index(Parent[i][j])])
    return [RealParents, RealParentsName, Chert7[0]]

def FindParentName(n , Parent):
    parent = []
    for i in range(0, len(Parent)):
        lp = len(Parent[i])
        if n == Parent[i][0] and lp > 1:
            for j in range(1, lp):
                parent.append(Parent[i][j])

    return parent

def VarUpdate(QQQ, Var, Decision, Parent):
    QQ = mycopy.deepcopy(QQQ)
    if QQ[0] == 'MEU':
        for i in range(1, len(QQ)):
            Chert20 = list(QQ[i])
            if len(Chert20) == 1 and Chert20[0] != '|':
                QQ[i] = ''.join([Chert20[0], '.', '+'])
    del QQ[0]
    while '|' in QQ: QQ.remove('|')
    [e, value] = Decode(QQ)
    index = []

    UpdatedVar = mycopy.deepcopy(e)
    chert =  mycopy.deepcopy(e)

    while len(chert)>0:
        n = chert[0]
        del chert[0]
        p = FindParentName(n , Parent)
        for i in range(0, len(p)):
            if p[i] not in UpdatedVar:
                UpdatedVar.append(p[i])
                chert.append(p[i])

    for i in range(0, len(UpdatedVar)):
        if UpdatedVar[i] in Decision:
            index.append(i)
    UpdatedVar = [v for i, v in enumerate(UpdatedVar) if i not in index]

    UpdatedVar = sorted(UpdatedVar, key=Var.index)
    return UpdatedVar

def FindProb(Child, Parent, Chert10):
    Prob = []
    c1 = Child.split('.')
    L = len(Parent)
    if L==0:
        if c1[1] == '+':
            Prob = float(Chert10[1])
            Prob = round(Prob, 2)
        else:
            Prob = 1-float(Chert10[1])
            Prob = round(Prob, 2)
    else:
        c2 = Chert10[0].split(' ')
        sequecnce = []
        for i in range(2, len(c2)):
            for j in range(0,L):
                c3 = Parent[j].split('.')
                if c3[0] == c2[i]:
                    sequecnce.append(c3[1])
        c4 = ''.join(sequecnce)

        for k in range(1, len(Chert10)):
            c5 = Chert10[k].split(' ')
            c6 = ''.join(c5[1:])
            if c4 == c6:
                if c1[1] == '+':
                    Prob = float(c5[0])
                    Prob = round(Prob, 2)
                else:
                    Prob = 1 - float(c5[0])
                    Prob = round(Prob, 2)
                break
    return Prob

def LookupTable(Child, Parent, ChildName, ParentName, Evidencess):
    ParentCopy = mycopy.deepcopy(Parent)
    DeleteIndex = []
    index=100000
    for i in range(0,len(Evidencess)):
        root = mycopy.deepcopy(Evidencess[i])
        Chert9 = root[0].split(' ')
        while ' ' in Chert9: Chert9.remove(' ')
        if ChildName == Chert9[0]:
            if '|' in Chert9 and len(ParentName)>0:
                if set(Chert9[2:]) <= set(ParentName):
                    index = i
                    for j in range(0, len(ParentName)):
                        if ParentName[j] not in Chert9[2:]:
                            DeleteIndex.append(j)
            elif '|' not in Chert9 and len(ParentName)==0:
                index = i
    if index < 100000:
        Chert10 = mycopy.deepcopy(Evidencess[index])
        ParentCopy = [v for i, v in enumerate(ParentCopy) if i not in DeleteIndex]
        Prob = FindProb(Child, ParentCopy, Chert10)
    else:
        Prob = 'no'

    return Prob

def EnumerateALL(Var, EV, Parent, Evidencess):
    if len(Var)==0:
        return 1
    VarCopy = mycopy.deepcopy(Var)
    EVcopy = mycopy.deepcopy(EV)
    Y = VarCopy[0]
    RestVars = VarCopy[1:]
    [e, value] = Decode(EVcopy)

    if Y in e:
        YY = ''.join([Y, '.', value[e.index(Y)]])
        [RealParents, RealParentsName, ChildName] = FindParent(YY, EVcopy, Parent)
        Prob = LookupTable(YY, RealParents, ChildName, RealParentsName, Evidencess)
        return Prob*EnumerateALL(RestVars, EVcopy, Parent, Evidencess)
    else:
        YYp = ''.join([Y, '.', '+'])
        YYn = ''.join([Y, '.', '-'])
        EVcopyp = mycopy.deepcopy(EVcopy)
        EVcopyp.append(YYp)
        EVcopyn = mycopy.deepcopy(EVcopy)
        EVcopyn.append(YYn)

        [RealParents1, RealParentsName1, ChildName1] = FindParent(YYp, EVcopyp, Parent)
        Prob1 = LookupTable(YYp, RealParents1, ChildName1, RealParentsName1, Evidencess)

        [RealParents2, RealParentsName2, ChildName2] = FindParent(YYn, EVcopyn, Parent)
        Prob2 = LookupTable(YYn, RealParents2, ChildName2, RealParentsName2, Evidencess)
        return Prob1*EnumerateALL(RestVars, EVcopyp, Parent, Evidencess) + Prob2*EnumerateALL(RestVars, EVcopyn, Parent, Evidencess)

def UtilityUpdate(UtilityParents, UtilityParentValues, index, ObservedEvidence):
    UtilityParentValuesUpdate=[]
    [e, value] = Decode(ObservedEvidence)
    for i in range(0, len(index)):
        A = index[i]
        removingU = UtilityParents[A]
        YY = e.index(removingU)
        removingUvalue = value[YY]
        for j in range(0, len(UtilityParentValues)):
            chert = UtilityParentValues[j].split(' ')
            if chert[A+1] == removingUvalue:
                del chert[A+1]
                UtilityParentValuesUpdate.append(' '.join(chert))

    UtilityParentsUpdate = [v for i, v in enumerate(UtilityParents) if i not in index]
    return [UtilityParentsUpdate, UtilityParentValuesUpdate]

def ExpectedUtility(Utilities, ObservedEvidence, Var, Parent, Decision, Evidencess):
    UtilityParent = Utilities[0]
    UtilityParentValues = Utilities[1:]
    UtilityParents = UtilityParent.split(' ')
    UtilityParents.remove('utility')
    UtilityParents.remove('|')
    index = []
    [e, value] = Decode(ObservedEvidence)
    for i in range(0, len(UtilityParents)):
        if UtilityParents[i] in e:
            index.append(i)

    if len(index) > 0:
        [UtilityParents, UtilityParentValues] = UtilityUpdate(UtilityParents, UtilityParentValues, index, ObservedEvidence)
    ProbParent = []
    ValueParent = []
    Sum = 0
    FinalUtility = 0
    if len(UtilityParents) == 0:
        values = UtilityParentValues[0].split(' ')
        FinalUtility = values[0]
        return FinalUtility
    elif len(UtilityParents) == 1:
        for i in range(0, len(UtilityParentValues)):
            EV = mycopy.deepcopy(ObservedEvidence)
            values = UtilityParentValues[i].split(' ')
            # print ['valus', values , UtilityParents[0] , values[1]]
            EV.append("".join([UtilityParents[0], '.', values[1]]))
            xxx = EnumerateALL(Var, EV, Parent, Evidencess)
            ProbParent.append(xxx)
            ValueParent.append(values[0])
            Sum = Sum + xxx
        for i in range(0, len(UtilityParentValues)):
            FinalUtility = FinalUtility + ProbParent[i]*float(ValueParent[i])/Sum
        return FinalUtility

    elif len(UtilityParents) == 2:
        for i in range(0, len(UtilityParentValues)):
            EV = mycopy.deepcopy(ObservedEvidence)
            values = UtilityParentValues[i].split(' ')
            EV.append("".join([UtilityParents[0], '.', values[1]]))
            EV.append("".join([UtilityParents[1], '.', values[2]]))
            xxx = EnumerateALL(Var, EV, Parent, Evidencess)
            ProbParent.append(xxx)
            ValueParent.append(values[0])
            Sum = Sum + xxx
        for i in range(0, len(UtilityParentValues)):
            FinalUtility = FinalUtility + ProbParent[i]*float(ValueParent[i])/Sum
        return FinalUtility

    elif len(UtilityParents) == 3:
        for i in range(0, len(UtilityParentValues)):
            EV = mycopy.deepcopy(ObservedEvidence)
            values = UtilityParentValues[i].split(' ')
            EV.append("".join([UtilityParents[0], '.', values[1]]))
            EV.append("".join([UtilityParents[1], '.', values[2]]))
            EV.append("".join([UtilityParents[2], '.', values[3]]))
            xxx = EnumerateALL(Var, EV, Parent, Evidencess)
            ProbParent.append(xxx)
            ValueParent.append(values[0])
            Sum = Sum + xxx
        for i in range(0, len(UtilityParentValues)):
            FinalUtility = FinalUtility + ProbParent[i]*float(ValueParent[i])/Sum
        return FinalUtility

#-- Open the file and read the content
f = open('./Sample test cases/input01.txt','r')
Content = f.read().split('******')
#-- Separation
Query = Content[0]
Evidence = Content[1]
if len(Content) == 3:
    Utility = Content[2]
    Utilities = Utility.split('\n')
    while '' in Utilities: Utilities.remove('')

Queries = Query.split('\n')
Evidences = Evidence.split('***')
while '' in Queries: Queries.remove('')

Evidencess = []
for i in range(0,len(Evidences)):
    Chert1 = Evidences[i].split('\n')
    while '' in Chert1: Chert1.remove('')
    Evidencess.append(Chert1)

[Var, Parent, Decision] = FindVarParentDecision(Evidencess)

PolishedQueries = ReadingQueries(Queries)


Result = []
for i in range(0, len(PolishedQueries)):
    QQQ = mycopy.deepcopy(PolishedQueries[i])
    VarCopy = mycopy.deepcopy(Var)
    EvidencessCopy = mycopy.deepcopy(Evidencess)
    ParentCopy = mycopy.deepcopy(Parent)
    UpdatedVar = VarUpdate(QQQ, VarCopy, Decision, ParentCopy)

    varvar = Var
    evievi = Evidencess

    if QQQ[0] == 'P':
        varvar = UpdatedVar
        EV = []
        result = 1
        if '|' in QQQ:
            YY = QQQ.index('|')
            EV = QQQ[YY+1:]
            QU = QQQ[1:YY]
            QUp = QQQ[1:]
            QUp.remove('|')
        else:
            QU = QQQ[1:]
            QUp = QU

        sortedQU = SortVar(QU, varvar)
        for j in range(0,len(QU)):
            QUQU = sortedQU[j]  #QU[j]
            [RealParents, RealParentsName, ChildName] = FindParent(QUQU, QUp, Parent)
            #-----------------------------
            RealParents = []
            for ll in range(0,j):
                RealParents.append(sortedQU[ll])
            [RealParentsName, chert] = Decode(RealParents)
            #-----------------------------
            if len(EV)>0:
                for k in range(0,len(EV)):
                    Chert11 = mycopy.deepcopy(EV[k])
                    Chert12 = Chert11.split('.')
                    if Chert11 not in RealParents:
                        RealParents.append(Chert11)
                        RealParentsName.append(Chert12[0])
            Prob = LookupTable(QUQU, RealParents, ChildName, RealParentsName, evievi)


            if Prob == 'no':
                EVv = mycopy.deepcopy(EV)
                for p in range(0, len(RealParents)):
                    if RealParents[p] not in EVv:
                        EVv.append(RealParents[p])
                Chert13 = mycopy.deepcopy(QUQU)
                Chert14 = Chert13.split('.')
                if Chert14[1] == '+':
                    Chert15 = "".join([Chert14[0], '.', '-'])
                else:
                    Chert15 = "".join([Chert14[0], '.', '+'])

                EVoriginal = mycopy.deepcopy(EVv)
                EVprime = mycopy.deepcopy(EVv)
                EVoriginal.append(Chert13)
                EVprime.append(Chert15)

                XXX = EnumerateALL(varvar, EVoriginal, Parent, evievi)
                YYY = EnumerateALL(varvar, EVprime, Parent, evievi)
                result = result * XXX / (XXX + YYY)
            else:
                result = result*Prob
        result = round(result, 2)

    elif QQQ[0] == 'EU':
        ObservedEvidence = mycopy.deepcopy(QQQ)
        ObservedEvidence.remove('EU')
        while '|' in ObservedEvidence: ObservedEvidence.remove('|')
        result = ExpectedUtility(Utilities, ObservedEvidence, varvar, Parent, Decision, evievi)
        result = round(result)

    elif QQQ[0] == 'MEU':
        ObservedEvidence = []
        Decisions = QQQ
        if '|' in QQQ:
            YY = QQQ.index('|')
            ObservedEvidence = QQQ[YY+1:]
            Decisions = QQQ[1:YY]
        else:
            Decisions = QQQ[1:]

        if len(Decisions)==1:
            EVp = mycopy.deepcopy(ObservedEvidence)
            EVp.append(''.join([Decisions[0], '.', '+']))
            EVn = mycopy.deepcopy(ObservedEvidence)
            EVn.append(''.join([Decisions[0], '.', '-']))
            EUp = ExpectedUtility(Utilities, EVp, varvar, Parent, Decision, evievi)
            EUn = ExpectedUtility(Utilities, EVn, varvar, Parent, Decision, evievi)
            if EUp > EUn:
                result = ''.join(['+ ', str(int(round(EUp)))])
            else:
                result = ''.join(['- ', str(int(round(EUn)))])


        elif len(Decisions)==2:
            code = [0, 1, 2, 3]
            value = [['+','+'], ['+','-'], ['-','+'], ['-','-']]
            EUs = []
            for i in range(0, 4):
                EV = mycopy.deepcopy(ObservedEvidence)
                sign = value[i]
                EV.append(''.join([Decisions[0], '.', sign[0]]))
                EV.append(''.join([Decisions[1], '.', sign[1]]))
                EU = ExpectedUtility(Utilities, EV, varvar, Parent, Decision, evievi)
                EUs.append(EU)
            max = 0
            for i in range(0,4):
                if EUs[i] > max:
                    index = i
                    max = EUs[i]
            result = ' '.join([ value[index][0], value[index][1], str(int(round(EUs[index]))) ])


        elif len(Decisions)==3:
            code = [0, 1, 2, 3, 4, 5, 6, 7]
            value = [['+','+','+'], ['+','+','-'], ['+','-','+'], ['+','-','-'],         ['-','+','+'], ['-','+','-'], ['-','-','+'], ['-','-','-']]
            EUs = []
            for i in range(0, 4):
                EV = mycopy.deepcopy(ObservedEvidence)
                sign = value[i]
                EV.append(''.join([Decisions[0], '.', sign[0]]))
                EV.append(''.join([Decisions[1], '.', sign[1]]))
                EV.append(''.join([Decisions[2], '.', sign[2]]))
                EU = ExpectedUtility(Utilities, EV, varvar, Parent, Decision, evievi)
                EUs.append(EU)
            max = 0
            for i in range(0, 8):
                if EUs[i] > max:
                    index = i
                    max = EUs[i]
            result = ' '.join([value[index][0], value[index][1], value[index][1], str(int(round(EUs[index])))])

    Result.append(result)

file = open("./Sample test cases/output.txt", "w")
for i in range(0, len(Result)):
    TYPE = type(Result[i])
    if TYPE == int:
        file.write("%d\n" % Result[i])
    elif TYPE == float:
        if Result[i] >= 1:
            file.write("%d\n" % Result[i])
        else:
            file.write("%.2f\n" % Result[i])
    elif TYPE == str:
        file.write("%s\n" % Result[i])
file.close()


#print default_timer() - start