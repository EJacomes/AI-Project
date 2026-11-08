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


time1 = time()
BFS(initialNode)
time2 = time() - time1
print("The time it took for BFS to reach the goal was", time2, "seconds")

#time3 = time()
#initialNode = [6, 6, 1]
#BFS(initialNode)
#time4 = time() - time3
#print("The time it took for BFS to reach the goal was", time4, "seconds")

#A* search version
openA = []
closedA = []
