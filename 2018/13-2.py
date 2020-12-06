import argparse
import re
import string
from datetime import datetime
import operator
import copy
from html import escape


htmlTemplate = """
<html>
<head>
    <style>
        body {
            background-color: black;
            font-family: monospace;
        }
        .track {
            display: block;
            position: absolute;
            height: 7px;
            width: 7px;
            color: #444;
            line-height: 7px;
            z-index: 1;
        }
        .truck {
            display: block;
            position: absolute;
            height: 7px;
            width: 7px;
            color: red;
            font-weight: bold;
            line-height: 7px;
            z-index: 2;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js" type="text/javascript"></script>
</head>
<body>
    TRACK
    TRUCKS
    <script type="text/javascript">
        SCRIPTS
    </script>
</body>
</html>
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('--html', action='store_true')
    args = parser.parse_args()

    layout = []
    y = 0
    with open(args.infile) as infile:
        for line in infile:
            if len(line.strip()) > 0:
                layout.append([])
                for char in line.rstrip('\n'):
                    layout[y].append(char)
                y += 1

    layoutHeight = len(layout)
    layoutWidth = len(layout[0])

    def getTrack(x, y):
        return layout[y][x]

    compass = ['<', '^', '>', 'v']
    curveMap = {
        '/': {
            '>': '^',
            '^': '>',
            'v': '<',
            '<': 'v',
        },
        '\\': {
            '>': 'v',
            '^': '<',
            'v': '>',
            '<': '^',
        },
    }

    class Truck:
        def __init__(self, x, y, direction, truckId):
            self.x = x
            self.y = y
            self.direction = direction
            self.id = truckId
            self.turns = 0

        def move(self):
            self.moveInDirection(self.direction)
            newTrack = getTrack(self.x, self.y)
            self.setDirectionForTrack(newTrack)

        def moveInDirection(self, direction):
            vectorMap = {
                '>': [1, 0],
                '<': [-1, 0],
                '^': [0, -1],
                'v': [0, 1],
            }
            self.x += vectorMap[direction][0]
            self.y += vectorMap[direction][1]

        def setDirectionForTrack(self, trackType):
            if self.id == 1:
                truck1 = True
            currentDirection = self.direction
            if trackType in '/\\':
                self.direction = curveMap[trackType][currentDirection]
            elif trackType == '+':
                compassChange = [-1, 0, 1][self.turns % 3]
                currentCompassIndex = compass.index(self.direction)
                self.direction = compass[(currentCompassIndex + compassChange) % 4]
                self.turns = self.turns + 1

        def __str__(self):
            return self.direction

    trucks = []
    for y in range(0, layoutHeight):
        for x in range(0, layoutWidth):
            char = layout[y][x]
            if char in '<>^v':
                trucks.append(Truck(x, y, char, len(trucks)))
                if char in '<>':
                    layout[y][x] = '-'
                elif char in '^v':
                    layout[y][x] = '|'

    if args.html:
        trackHtml = ''
        y = 0
        while y < layoutHeight:
            x = 0
            while x < layoutWidth:
                if layout[y][x] != ' ':
                    xpos = 7 * x
                    ypos = 7 * y
                    trackHtml += """    <div class="track" style="left: {0:4}px; top: {1:4}px;">{2}</div>  
                        """.format(xpos, ypos, layout[y][x])
                x += 1
            trackHtml += '\n    '
            y += 1
        html = htmlTemplate.replace('TRACK', trackHtml)

        truckHtml = ''
        for truck in trucks:
            truckHtml += """
                <div class="truck" id="truck-{0}">{1}</div>""".format(
                truck.id, escape(truck.direction))

        html = html.replace('TRUCKS', truckHtml)

    def getTrucks(trucksList, x, y):
        trucksAtXY = []
        for truck in trucksList:
            if (truck.x, truck.y) == (x, y):
                trucksAtXY.append(truck)
        return trucksAtXY

    def draw(trucksList):
        image = ''
        y = 0
        while y < layoutHeight:
            x = 0
            while x < layoutWidth:
                trucksHere = getTrucks(trucksList, x, y)
                if len(trucksHere) == 1:
                    image += str(trucksHere[0])
                elif len(trucksHere) > 1:
                    image += 'X'
                else:
                    image += layout[y][x]
                x += 1
            image += '\n'
            y += 1
        return image

    tick = 0
    print(draw(trucks))
    lastTickTrucks = []
    for truck in trucks:
        lastTickTrucks.append(copy.deepcopy(truck))

    scriptJs = ''
    while len(trucks) > 1:
        tick += 1
        tickJsFunctionBody = ''

        trucksToMove = sorted(trucks, key=operator.attrgetter('y', 'x'))
        crashAverted = False
        while trucksToMove:
            truck = trucksToMove.pop(0)
            truck.move()
            trucksAtNewLocation = getTrucks(trucks, truck.x, truck.y)
            if len(trucksAtNewLocation) > 1:
                for truckHere in trucksAtNewLocation:
                    trucks.remove(truckHere)
                    if truck in trucksToMove:
                        trucksToMove.remove(truckHere)
                print('Prevented crash at {0:>3},{1:<3} at tick {2:,}'.format(truck.x, truck.y, tick))
                crashAverted = True

        # endangeredTrucks = set()
        # for truck in trucks:
        #     trucksAtNewLocation = getTrucks(trucks, truck.x, truck.y)
        #     if len(trucksAtNewLocation) > 1:
        #         endangeredTrucks |= set(trucksAtNewLocation)

        # for truck in endangeredTrucks:
        #     print('Prevented crash at {0:>3},{1:<3} at tick {2:,}'.format(truck.x, truck.y, tick))
        #     trucks.remove(truck)
        #     if args.html and tick < 500:
        #         tickJsFunctionBody += """$('#truck-{0}').hide(2000)\n""".format(truck.id)
        # if endangeredTrucks:
        if crashAverted:
            print(draw(lastTickTrucks))

        if args.html and tick < 500:
            for truck in trucks:
                tickJsFunctionBody += """
                    $('#truck-{0}').animate({{
                        left: '{1}px',
                        top: '{2}px'
                    }}, 200).html('{3}')
                """.format(truck.id, truck.x * 7, truck.y * 7, escape(truck.direction))

        if len(trucks) == 1:
            print(draw(trucks))
            print('Last truck is at {0},{1}'.format(trucks[0].x, trucks[0].y))

        if args.html and tick < 500:
            scriptJs += """
            // Tick {0}
            setTimeout(() => {{
                {1}
            }}, {2});
            """.format(tick, tickJsFunctionBody, tick * 200)

        trucksAfterAction = []
        for truck in trucks:
            trucksAfterAction.append(copy.deepcopy(truck))
        lastTickTrucks = trucksAfterAction

    if args.html:
        html = html.replace('SCRIPTS', scriptJs)
        with open('13-2-output.html', 'w') as htmlFile:
            htmlFile.write(html)

    print()
    print('Finish')


if __name__ == "__main__":
    main()
