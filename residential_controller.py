class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = 'online'
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.elevatorsList = []
        self.callButtonsList = []
        self.createElevators()
        self.createCallButtons()

    def createCallButtons(self):
        buttonFloor = 1
        callButtonID = 1
        for i in range(self.amountOfFloors):
            if buttonFloor < self.amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, 'up')
                self.callButtonsList.append(callButton)
            if buttonFloor > 1:
                callButton = CallButton(callButtonID, buttonFloor, 'down')
                self.callButtonsList.append(callButton)
            callButtonID += 1
            buttonFloor += 1

    def createElevators(self):
        elevatorID = 1
        for i in range(self.amountOfElevators):
            elevator = Elevator(elevatorID, self.amountOfFloors)
            self.elevatorsList.append(elevator)
            elevatorID += 1

    def requestElevator(self, floor, direction):
        bestElevator = self.findElevator(floor, direction)
        bestElevator.floorRequestList.append(floor)
        bestElevator.move()
        bestElevator.operateDoors()
        return bestElevator

    def findElevator(self, requestedFloor, requestedDirection):
        bestElevator = None
        bestScore = 5
        referenceGap = 10000000
        for elevator in self.elevatorsList:
            score = 4
            if requestedFloor == elevator.currentFloor and elevator.status == 'stop' and requestedDirection == elevator.direction:
                score = 1
            elif requestedFloor > elevator.currentFloor and elevator.direction == 'up' and requestedDirection == elevator.direction:
                score = 2
            elif requestedFloor < elevator.currentFloor and elevator.direction == 'down' and requestedDirection == elevator.direction:
                score = 2
            elif elevator.status == 'idle':
                score = 3
            bestElevatorInformations = elevator.checkIfElevatorIsBetter(score, bestScore, referenceGap, bestElevator, requestedFloor)
            bestElevator = bestElevatorInformations['bestElevator']
            bestScore = bestElevatorInformations['bestScore']
            referenceGap = bestElevatorInformations['referenceGap']
        return bestElevator

class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = 'idle'
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = 1
        self.direction = None
        self.overweightAlarm = False
        self.overweight = False
        self.door = Door(self.ID)
        self.floorRequestButtonsList = []
        self.floorRequestList = []
        self.createFloorRequestButtons()

    def createFloorRequestButtons(self):
        buttonFloor = 1
        floorRequestButtonID = 1
        for i in range(self.amountOfFloors):
            self.floorRequestButtonsList.append(FloorRequestButton(floorRequestButtonID, buttonFloor))
            buttonFloor += 1
            floorRequestButtonID += 1

    def checkIfElevatorIsBetter(self, scoreToCheck, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = self
            referenceGap = abs(self.currentFloor - floor)
        elif scoreToCheck == bestScore :
            gap = abs(self.currentFloor - floor)
            if referenceGap > gap:
                bestElevator = self
                referenceGap = gap
        return {
            'bestElevator': bestElevator,
            'bestScore': bestScore,
            'referenceGap': referenceGap
        }

    def requestFloor(self, floor):
        self.floorRequestList.append(floor)
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
    def __init__(self, _id, _floor, _direction,):
        self.ID = _id
        self.floor = _floor
        self.direction = _direction
        self.status = 'OFF'

class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.floor = _floor
        self.status = 'OFF'


class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = 'closed'
        self.obstructed = False
    

    def isObstructed(): 
        return False