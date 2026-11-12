from time import time
openBFS = [] #Where the nodes that haven't been visited will be stored
closedBFS = [] #Where the nodes that have been visited will be stored
leftSideBFS =[] #The current node being visited
rightSideBFS = [] #Where the different of the current values of leftSideBFS will be stored
initialNode = [3, 3, 1] #nodes will follow [M, C, B] format
TargetNode = [0, 0, 0]

def isValid(leftsideBFS, rightsideBFS):
    #add the code that will have it so that the leftside and the rightside will be compared with each other
    #in order to see if the numbers of Cannibals do not outnumber the numbers of missionaries
    valid = True

    LMissionaries = leftsideBFS[0][0]
    LCannibals = leftsideBFS[0][1]
    RMissionaries = rightsideBFS[0][0]
    RCannibals = rightsideBFS[0][1]

    if (LMissionaries < LCannibals and LMissionaries != 0):
        valid = False

    if(RMissionaries < RCannibals and RMissionaries != 0):
        valid = False

    return valid   

def RightSide(leftsideBFS):
    #this will take the difference of the missionaries and cannibals by subtracting their respective node by 3 and for
    #the boat, it will check to see if it is 0 or 1 to set the third value in the node as 0 or 1
    RightSide = []

    RightSide.append(initialNode[0] - leftsideBFS[0][0])
    RightSide.append(initialNode[1] - leftsideBFS[0][1])

    if (leftsideBFS[0][2] == 0):
        RightSide.append(1)
    elif (leftsideBFS[0][2] == 1):
        RightSide.append(0)

    return RightSide

def leftside():
    #this function will add the first element in openBFS into leftSideBFS but the first element is popped out.
    #when that node is popped into openBFS, it will be also run RightSide(leftsideBFS) to get right side calculation as well
    CurrentNode = openBFS.pop(0)

    #first we need to see if the left side list is empty 
    if not leftSideBFS:
        leftSideBFS.append(CurrentNode)
        rightSideBFS.append(RightSide(leftSideBFS))
    else:
        VisitedNode = leftSideBFS.pop(0)
        rightSideBFS.pop(0)
        closedBFS.append(VisitedNode)
        leftSideBFS.append(CurrentNode)
        rightSideBFS.append(RightSide(leftSideBFS))

def addToOpen(node):
    openBFS.append(node)

def createNodes(node):
    #the node parameter is used in a way to where it will be leftSideBFS
    #the possible actions that be taken to create new nodes are
    #(2,0), (0,2), (1,0), (0,1), (1,1)
    #Those actions will follow (M, C) format
    #when the boat goes to the other side the actions will use subtraction while when the boat returns that will be addition

    #when looking at how the logic would look when the boat is going, it goes as follow:
    #When looking at the actions that can be taken with the missionaries:
    #if the current amount of missionaries on that node has a difference that is a negative when substracted by two then (2,0) can not be used
    #if the current amount of missionaries on that node has a difference that is a negative when subtracted by 1 then (1,0) and (1,1) can not be used
    #this would leave (0,1) and (0,2) as the only actions in that case 
    #When looking at the actions that can be taken with the cannibals:
    #if the current amount of cannibals on that node has a difference that is negative when substracted by two then (0,2) can not be used
    #if the current amount of cannibals on that node has a difference that is negative when substracted by one then (0,1) and (1,1) can not be used
    #this would leave (1,0) and (2,0) as the only action in that case 

    #when looking at how the logic would look when the boat is returning, it goes as follow:
    #if the current amount of missionaries and/or cannibals is set to the amount that was set in initialNode then there is no addition
    #When looking at the actions that can be taken with the missionaries:
    #if the current amount of missionaries on that node has a sum that is over the initial amount when being adding by two then (2,0) can not be used
    #if the current amount of missionaries on that node has a sum that is over the initial amount when being adding by one then (1,0) and (1,1) can not be used
    #this would leave (0,1) and (0,2) as the only actions in that case 
    #When looking at the actions that can be taken with the cannibals:
    #if the current amount of cannibals on that node has a sum that is over the initial amount when being adding by two then (0,2) can not be used
    #if the current amount of cannibals on that node has a sum that is over the initial amount when being adding by one then (0,1) and (1,1) can not be used 
    #this would leave (1,0) and (2,0) as the only action in that case 

    #if there any action that is unable to be used then it will be popped out from the PossibleAction list and into the NotUsed list

    PossibleAction = [[2, 0], [0, 2], [1, 0], [0, 1], [1, 1]]

    #this part will refer to when (M, C, 1)
    if (node[0][2] == 1):
        #subtraction will occur
        #looking for the actions that can't be used
        for x in PossibleAction:
            currentActionM = x[0]
            currentActionC = x[1]

            if (((node[0][0] - currentActionM) < 0) or ((node[0][1]- currentActionC) < 0)):
                PossibleAction.remove(x)

        #another loop used to make the nodes
        for y in PossibleAction:
            newNode = []
            NewM = node[0][0] - y[0]
            NewC = node[0][1] - y[1]
            newNode.append(NewM)
            newNode.append(NewC)
            newNode.append(0)
            addToOpen(newNode)
    elif (node[0][2] == 0):
        #this part above will refer to when (M, C, 0)
        #addition will occur
        #looking for actions that can't be used
        for x in PossibleAction:
            currentActionM = x[0]
            currentActionC = x[1]

            if (((node[0][0] + currentActionM) > initialNode[0]) or ((node[0][1] + currentActionC) > initialNode[1])):
                PossibleAction.remove(x)

        #another loop used to make the nodes
        for y in PossibleAction:
            newNode = []
            NewM = node[0][0] + y[0]
            NewC = node[0][1] + y[1]
            newNode.append(NewM)
            newNode.append(NewC)
            newNode.append(1)
            addToOpen(newNode)           
    

def BFS(StartingNode):
    numNodes = 0 
    #for the initial node, the logic will be as followed node -> addToOpen -> leftside -> RightSide -> isValid
    #The whole BFS function will be a loop until there is a node that is equal to [0, 0, 0]

    #initial node setup will be outside of the loop
    addToOpen(StartingNode)
    print(openBFS)
    leftside()
    ClearToGo = isValid(leftSideBFS, rightSideBFS)
    numNodes = numNodes + 1
    print(numNodes)
    print(ClearToGo)

    if (ClearToGo == True):
        while (TargetNode not in leftSideBFS):
            #Now that the initial node is in leftSideBFS, we can go ahead and use createNodes(node) to make the new nodes from the initial
            createNodes(leftSideBFS)
            print("Before:",openBFS)
            #now that the new nodes are made, the leftside() function is called
            leftside()
            print("After:",openBFS)
            CanContinue = False
            while CanContinue == False:
                if (isValid(leftSideBFS, rightSideBFS) == True):
                    CanContinue = True
                else:
                    leftside()
                    print("In-between:",openBFS)
            numNodes = numNodes + 1
    
    print("BFS was able to reach to goal node [0, 0, 0] in",numNodes,'nodes')


#time1 = time()
#BFS(initialNode)
#time2 = time() - time1
#print("The time it took for BFS to reach the goal was", time2, "seconds")

#time3 = time()
#initialNode = [6, 6, 1]
#BFS(initialNode)
#time4 = time() - time3
#print("The time it took for BFS to reach the goal was", time4, "seconds")

#A* search version
openA = []
closedA = []
#leftSideA = []
#most likely leftSideA will not be used since A* search since the process will involving looking at a grouping of nodes instead of a individual nodes
rightSideA = []
#var initialNode and TargetNode will be used for A* Search as well

#This A* search will use f(n) = g(n) + h(n) which will calculate the total amount of actions that are used
#g(n) is the number of trips that was taken from the starting node to the current node being looked at (i.e. 3, 3, 1 -> 2, 2, 0 then g(n) = 1)
#since one trip was taken from the beginning side to the other side
#h(n) is the number of trips that could be taken from the current node to the goal node (i.e. 3, 3, 1 -> 0, 0, 0 then h(n) = 9)
#since there were 9 trips taken in order to move the missionaries from the beginning to the other side

#when looking at the nodes which has the smalles f(n), we will first need to get rid of any nodes that will be breaking the rule of having
#more cannibals then missionaries in either side. 
#once there are only valid nodes left then we look at the g and h values of each node and sum it up to see which node has the smallest f(n) value
#once the node with the smallest f(n) value is selected then all of the other nodes in that grouping will sent to the closed list
#that selected node will have the new nodes made of it and the process will repeat until the goal is reached

def RightSideA(openlist):
    rightNode = []
    rightSideA.clear() #Since this method is looking at it as a group, then each time this method is called, rightSideA needs to be cleared out for the next grouping to go in
    #openlist will be a lists of lists i.e. [[1,1,1], [3,1,0]]
    #this method will use a for loop to pull each node
    #the M and the C sections of the node will be subtracted by 3 and the B will have 1 or 0 set in their depending on the current B value in the node
    #the results will be added onto the rightNode then that node will be added to the rightSideA list 
    for x in openlist:
        rightNode.append(initialNode[0] - x[0])
        rightNode.append(initialNode[1] - x[1])

        if (x[2] == 0):
            rightNode.append(1)
        elif (x[2] == 1):
            rightNode.append(0)

        rightSideA.append(rightNode)
        rightNode.clear()

#11/10:the method isValidA() is gonna be left unused for now since there needs to be a method made to make the nodes in the open list, have their right side versions made as well
def isValidA():
    #this method will look at the nodes that is contained in the openA and rightSideA lists via a for loop and checks to see which node is valid and what isn't
    #if there is a node that is invalid then it will be stored in a list where it will be used in a .remove method to clear out the open and right side list of those nodes

    #the rule to make sure that a node is valid is that:
    #the numbers of cannibals can not outnumber the number of missionaires on either the left or right side.
    #if the numbers of missionaires is greater than or equal to the number of cannibals then it is a valid node

    notValid = []
    notValidR = []

    for node, rightnode in zip(openA, rightSideA):
        LMissionairesO = node[0]
        LCannibalsO = node[1]
        RMissionairesO = rightnode[0]
        RCannibalO = rightnode[1]

        if(LMissionairesO < LCannibalsO and LMissionairesO != 0):
            notValid.append(node)
            notValidR.append(rightnode)
        if (RMissionairesO < RCannibalO and RMissionairesO != 0):
            notValid.append(node)
            notValidR.append(rightnode)

    #once the for loop is done, the next steps will remove the invalid nodes so that the valid nodes are left in openA and rightSideA
    openA.remove(notValid)
    rightSideA.remove(notValid)
    closedA.append(notValid)

def initialValidCheck(node):
    #will be used to check to see if the initial node would be valid
    #returns a True or False
    #Its use would look like initialValidCheck(initialNode)
    LM = node[0]
    LC = node[1]

    isValid = False if LM < LC and LM != 0 else True
    
    return isValid

def countPresentTrip(CurrentCounter):
    #This method would be called up in the code it will look like:
    #count = 0
    #(In the loop) count = countPresentTrip(Count)
    CurrentCounter = CurrentCounter + 1
    return CurrentCounter #this will be the g(n) value

#11/10: the next few methods will focus on creating the next group of
#nodes based on the only node left in the open space
#the other method will focus on creating the possible trips that are
#needed for the groups of nodes to reach the goal node.
def nextNodes():
    #the node that will go through here is the last node that will stay in the open list after all of the other nodes that were valid but did not have the f(n) value
    #like the selected node is removed from open and put into closed 

    #the method for picking the desired actions will be the same as the method to create new nodes in the BFS method except that the only node left in the open list
    #will be popped out so that way the open list can be empty before the new nodes go in
    #with the creations of new nodes, there has to be the nodes for the other side as well so the RightSideA will be called here

    CurrentNode = openA.pop(0)

    possibleActions = [[2, 0], [0, 2], [1, 0], [0, 1], [1, 1]]

    if (CurrentNode[2] == 1):
        #since the value on index 2 is 1 that means subtraction will occur
        #looking for the actions that can't be used 
        for x in possibleActions:
            CurrentActionM = x[0]
            CurrentActionC = x[1]

            if (((CurrentNode[0] - CurrentActionM) < 0) or ((CurrentNode[1] - CurrentActionC) < 0)):
                possibleActions.remove(x)

        #the loop to make the nodes
        for y in possibleActions:
            newNode = []
            NewMNode = CurrentNode[0] - y[0]
            NewCNode = CurrentNode[1] - y[1]
            newNode.append(NewMNode)
            newNode.append(NewCNode)
            newNode.append(0)
            openA.append(newNode)
            newNode = []
    elif (CurrentNode[2] == 0):
        #since the value on index 2 is 0 that means addition wil occur
        #looking for actions that can't be used
        for x in possibleActions:
            CurrentActionM = x[0]
            CurrentActionC = x[1]

            if (((CurrentNode[0] + CurrentActionM) > initialNode[0]) or ((CurrentNode[1] + CurrentActionC) > initialNode[1])):
                possibleActions.remove(x)

            for y in possibleActions:
                newNode = []
                NewMNode = CurrentNode[0] + y[0]
                NewCNode = CurrentNode[1] + y[1]
                newNode.append(NewMNode)
                newNode.append(NewCNode)
                newNode.append(0)
                openA.append(newNode)
                newNode = []

    #the part of this method where RightSideA() is called
    RightSideA(openA)

def futureActionCosts():
    #this method will be calculating the h value of the f(n) = g(n) + h(n)
    #in order to understand how to calculate the amount of actions needed in order
    #the h value, the follow logic has been used

    #When looking at all of the valid nodes in the open list, each node will be called upon via a for loop
    #anytime a trip is made, there is a counter that will increase by 1
    #in that for loop there will be a while loop that will keep on running until the node gets to [0, 0, 0]
    #before that node will go into the while, that node will be put in a seperate variable so that way the node in the open list is not affected
    #in the while loop, there will be a list of possible actions that is taken up during the move from left side to right side.
    #There will also be two list, called UsedActionL and UsedActionR, these list represent the action that was used to get the node to left to right or right or left
    #UsedActionR is the list that will store the action of the node that went left to right
    #UsedActionL is the list that will store the action of the node that went right to left

    #there will two conditionals based on what is the boat value on the node when it begins a loop 
    #if the boat value is set to 1 then the actions to make the node for the next loop will have subtraction involved
    #if the boat value is 1 then the possible actions list will used to check which action will be used to make the node of the next loop
    #there are the conditions for the action to be used for the next action:
    #that the difference of next cannibals value will not be greater then the value of the difference of next missionaries
    #The rightside version of the node will not have the number of cannibals outnumber the number of missionaires
    #that the difference of either the cannibals or missionaries does not fall below zero
    #that the action that was used to get it to the left side can not be used again to avoid canceling the progress made
    #if the future action meets those conditions then it will be used to create the next loop node and that action will added to UsedActionL while the action that 
    #was in UsedActionR is removed
    #then there will be increase in the h value by one.

    #if the boat value is set to 0 then the action to make the node for the next loop will have addition involved
    #if the boat value is set to 0 then the possible actions list will used to check which action will be used to make the node of the next loop
    #there are the conditions for the action to be used for the next action:
    #that the sum of the next cannibals value will not be greater then the value of the sum of the next missionaries
    #The rightside version of the node will not have the number of cannibals outnumber the number of missionaires
    #that the sume of either the cannibals or missionaries does not go above the initial value
    #that the action that was used to get it to the right side can not be used again to avoid canceling the progress made
    #if the future action meets those conditions then it will be used to create the next loop node and that action will added to UsedActionR while the action that 
    #was in UsedActionL is removed
    #then there will be increase in the h value by one.

    target = [0, 0, 0]
    UsedActionR = []
    UsedActionL = []
    hValues = []
    NumofTrips = 0

    #the loops to determine h values
    for x in openA:
        Node = x
        while (Node == target):
            NextActions = [[2, 0], [0, 2], [1, 0], [0, 1], [1, 1]]

            for A in NextActions:
                if (Node[2] == 1):
                    #subtraction will occur
                    #4 conditions in one if statement broken up using and statement
                    if ((Node[1] - A[1] <= Node[0] - A[0]) and (initialNode[1] - (Node[1] - A[1]) <= initialNode[0] - (Node[0] - A[0])) and ((Node[0] - A[0] >= 0) or (Node[1] - A[1] >= 0)) and (UsedActionR[0] == A)):
                        UsedActionR = []
                        UsedActionL.append(A)
                        
                        Node[0] = Node[0] - A[0]
                        Node[1] = Node[1] - A[1]
                        Node[2] = 0
                        NumofTrips = NumofTrips + 1
                        break
                elif (Node == 0):
                    #addition will occur
                    if ((Node[1] + A[1] <= Node[0] + A[0]) and (initialNode[1] - (Node[1] + A[1]) <= initialNode[0] - (Node[0] + A[0])) and ((Node[0] + A[0] <= initialNode[0]) or (Node[1] + A[1] <= initialNode[1])) and (UsedActionL[0] == A)):
                        UsedActionL = []
                        UsedActionR.append(A)
                        Node[0] = Node[0] + A[0]
                        Node[1] = Node[1] + A[1]
                        Node[2] = 1
                        NumofTrips = NumofTrips + 1
                        break
            
        hValues.append(NumofTrips)

    return hValues

def ASearch(InitialNode):
    #this will be the function where the A search will occur
    #the logic that will be used in order to perform the A search will be
    #there will be variable that will count the number of trips that were made since the beginning and each time that g value increase then countPresentTrip method will be called
    #first the method initialValidCheck method will be used on the InitialNode to see if it is valid
    #if the InitialNode is declared as valid then it will lead to a loop that will run until the target of [0, 0, 0] is met
    #in that loop, the flow of logic will be:
    #nextNodes() -> isValidA() -> h = futureActionCosts() -> loop(f = g + h[index]) -> checking to see which node has lowest f score and remove the other nodes
    # -> countPresentTrip() and increase the nodes var -> repeat until target is reached

    PresentTrips = 0
    nodes = 0

    #the A search loop
    

    print("You reached the target node of [0, 0, 0] in", nodes, "nodes")


    

tii = [3,2,1]
itt = 2
ion = []
ion.append(tii)
ion.append(itt)
p = []
p.append(ion)
print(p)
print(p[0])
print(p[0][0])
print(p[0][0][0])