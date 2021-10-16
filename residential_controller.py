#from time import sleep

class Column:

    def __init__(self, _id, _amountOfFloors, _amountOfElevators, _status='online', _bottomFloor=1):
        self.ID = _id
        self.status = _status
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.bottomFloor = _bottomFloor
        self.topFloor = self.bottomFloor + self.amountOfFloors - 1
        self.elevatorList = []
        self.callButtonList = []
        self.createElevators()
        self.createCallButtons()

    def createCallButtons(self):
        
        callButtonID = 1
        for floor in range(1,self.amountOfFloors):    
            self.callButtonList.append(CallButton(callButtonID, floor, 'up'))
            callButtonID += 1
        for floor in range(2, self.amountOfFloors + 1):
            self.callButtonList.append(CallButton(callButtonID, floor, 'down'))
            callButtonID += 1
            

    def createElevators(self):
        
        for id in range(1, self.amountOfElevators + 1):
            self.elevatorList.append(Elevator(id, self.amountOfFloors, 'idle', 1))
            

    def requestElevator(self, requestedFloor, direction):

        bestElevator = self.findElevator(requestedFloor, direction)
        bestElevator.floorRequestList.append(requestedFloor)
        bestElevator.move()
        bestElevator.operateDoors()
        return bestElevator

    def findElevator(self, requestedFloor, requestedDirection):

        comparedElevator = {
            'elevator' : None,
            'score' : 5,
            'referenceGap' : 10000000
        }
        for elevator in self.elevatorList:
            score = 4
            if requestedFloor == elevator.currentFloor and elevator.status == 'stop' and requestedDirection == elevator.direction:
                score = 1
            elif requestedFloor > elevator.currentFloor and elevator.direction == 'up' and requestedDirection == elevator.direction:
                score = 2
            elif requestedFloor < elevator.currentFloor and elevator.direction == 'down' and requestedDirection == elevator.direction:
                score = 2
            elif elevator.status == 'idle':
                score = 3
            bestElevator = elevator.compareElevator(score, comparedElevator, requestedFloor)
            comparedElevator = bestElevator

        return bestElevator['elevator']

class Elevator:

    def __init__(self, _id, _amountOfFloors, _status='idle', _currentFloor=1):
        self.ID = _id
        self.status = _status
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = _currentFloor
        self.direction = None
        self.overweightAlarm = False
        self.overweightSensor = 'OFF'
        self.door = Door(self.ID)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        self.createFloorRequestButtons()

    def createFloorRequestButtons(self):

       for idAndFloor in range(1, self.amountOfFloors + 1):
           self.floorRequestButtonList.append(FloorRequestButton(idAndFloor, idAndFloor))

    def compareElevator(self, scoreToCheck, bestElevator, floor):

        if scoreToCheck < bestElevator['score']:
            bestElevator['score'] = scoreToCheck
            bestElevator['elevator'] = self
            bestElevator['referenceGap'] = abs(self.currentFloor - floor)
        elif scoreToCheck == bestElevator['score'] :
            gap = abs(self.currentFloor - floor)
            if bestElevator['referenceGap'] > gap:
                bestElevator['elevator'] = self
                bestElevator['referenceGap'] = gap
        return bestElevator

    def requestFloor(self, requestedFloor):    

        self.floorRequestList.append(requestedFloor)
        self.move()
        self.operateDoors()

    def move(self):

        while len(self.floorRequestList) > 0:
            destination = self.floorRequestList.pop(0)
            self.status = 'moving'
            if self.currentFloor < destination:
                self.direction = 'up'
                self.sortFloorList()
                while self.currentFloor < destination:
                    self.currentFloor += 1
                    self.screenDisplay = self.currentFloor
            elif self.currentFloor > destination:
                self.direction = 'down'
                self.sortFloorList()
                while self.currentFloor > destination:
                    self.currentFloor -= 1
                    self.screenDisplay = self.currentFloor
            self.status = 'stop'
        self.status = 'idle'

    def sortFloorList(self):

        if self.direction == 'up':
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)

    def operateDoors(self):

        self.door.status = 'opened'
        #sleep(5)
        if not self.isOverweight():
            self.door.status = 'closing'
            if not self.door.isObstructed():
                self.door.status = 'closed'
            else:
                self.operateDoors()
        else:
            while self.isOverweight():
                self.overweightAlarm = True
            self.overweightAlarm = False
            self.operateDoors()

    def isOverweight(self):
        
        return self.overweightSensor == 'ON' 


class CallButton:

    def __init__(self, _id, _floor, _direction, _status='OFF'):

        self.ID = _id
        self.floor = _floor
        self.direction = _direction
        self.status = _status

class FloorRequestButton:

    def __init__(self, _id, _floor, _status='OFF'):

        self.ID = _id
        self.floor = _floor
        self.status = _status


class Door:

    def __init__(self, _id, _status='closed'):

        self.ID = _id
        self.status = _status
        self.obstructionSensorState = 'OFF'
    

    def isObstructed(self): 

        return self.obstructionSensorState == 'ON'
