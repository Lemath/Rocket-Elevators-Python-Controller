class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators, _status='online'):
        self.ID = _id
        self.status = _status
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.elevatorList = []
        self.callButtonList = []
        self.createElevators()
        self.createCallButtons()

    def createCallButtons(self):
        buttonFloor = 1
        callButtonID = 1
        for i in range(self.amountOfFloors):
            if buttonFloor < self.amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, 'up')
                self.callButtonList.append(callButton)
            if buttonFloor > 1:
                callButton = CallButton(callButtonID, buttonFloor, 'down')
                self.callButtonList.append(callButton)
            callButtonID += 1
            buttonFloor += 1

    def createElevators(self):
        elevatorID = 1
        for i in range(self.amountOfElevators):
            elevator = Elevator(elevatorID, self.amountOfFloors, 'idle', 1)
            self.elevatorList.append(elevator)
            elevatorID += 1

    def requestElevator(self, requestedFloor, direction):
        bestElevator = self.findElevator(requestedFloor, direction)
        bestElevator.floorRequestList.append(requestedFloor)
        bestElevator.move()
        bestElevator.operateDoors()
        return bestElevator

    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = {
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
            bestElevator = elevator.checkIfElevatorIsBetter(score, bestElevator, requestedFloor)
        return bestElevator['elevator']

class Elevator:
    def __init__(self, _id, _amountOfFloors, _status='idle', _currentFloor=1):
        self.ID = _id
        self.status = _status
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = _currentFloor
        self.direction = None
        self.overweightAlarm = False
        self.overweight = False
        self.door = Door(self.ID)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        self.createFloorRequestButtons()

    def createFloorRequestButtons(self):
        buttonFloor = 1
        floorRequestButtonID = 1
        for i in range(self.amountOfFloors):
            self.floorRequestButtonList.append(FloorRequestButton(floorRequestButtonID, buttonFloor))
            buttonFloor += 1
            floorRequestButtonID += 1

    def checkIfElevatorIsBetter(self, scoreToCheck, bestElevator, floor):
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
        # Wait 5 Seconds
        if not self.overweight:
            self.door.status = 'closing'
            if not self.door.obstructed:
                self.door.status = 'closed'
            else:
                self.operateDoors()
        else:
            while self.overweight:
                self.overweightAlarm = True
            self.overweightAlarm = False
            self.operateDoors()


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
        self.obstructed = False
    

    def isObstructed(): 
        return False