#OO Python graph algo. implementation | 4-7-2015 (work in progress)
import copy

class Node(object):
    def __init__(self, id, next):
        self.id = id
        self.next = next #{id: (node, weight, isPassable), ...etc} - tuple within dict

    def hasPassable(self, stack):
        hasPassable = False
        node = None

        for tup in self.next.values():
            if (tup[2] and tup[0].id not in stack): #isPassable
                hasPassable = True
                node = tup[0]

        return (hasPassable, node)

    def addNext(self, node, weight, isPassable):
        self.next[node.id] = (node, weight, isPassable)

class Graph(object):
    def __init__(self, paths):
        self.paths = paths
        self.nodes = {} #{id: node}

        #build graph from inputs
        for path in self.paths:
            if (path["from"] not in self.nodes):
                self.nodes[path["from"]] = Node(path["from"], {})
            if (path["to"] not in self.nodes):
                self.nodes[path["to"]] = Node(path["to"], {})
            self.nodes[path["from"]].addNext(self.nodes[path["to"]], path["weight"], True)

    def pauseConnection(self, node1, node2):
        if (node2.id in node1.next):
            node1.next[node2.id] = (node1.next[node2.id][0], node1.next[node2.id][1], False)
        if (node1.id in node2.next):
            node2.next[node1.id] = (node2.next[node1.id][0], node2.next[node1.id][1], False)

    def resumeConnection(self, node1, node2):
        if (node2.id in node1.next):
            node1.next[node2.id] = (node1.next[node2.id][0], node1.next[node2.id][1], True)
        if (node1.id in node2.next):
            node2.next[node1.id] = (node2.next[node1.id][0], node2.next[node1.id][1], True)

    def getConnection(self, node1, node2):
        return (node1.next[node2.id] if (node2.id in node1.next) else None, node2.next[node1.id] if (node1.id in node2.next) else None)

    def printGraph(self):
        for id, node in self.nodes.items():
            print("from " + str(id))
            for tup in node.next.values():
                print("  --> " + str(tup[0].id) + ", w - " + str(tup[1]))
            print("------------")

    def pathsBetweenDFS(self, start, end):
        if (start == end or start not in self.nodes or end not in self.nodes): return None
        start = self.nodes[start]
        end = self.nodes[end]
        current = start
        pauseList = {} #{id: [id, id]}
        stack = []
        paths = []

        while (not (current is start and not current.hasPassable(stack)[0])):
            #print("At: " + str(current.id))
            if (current is end):
                #reach
                paths.append(copy.copy(stack) + [end.id])
                current = self.nodes[stack.pop()]
            elif (current.hasPassable(stack)[0]):
                #move forward
                nextNode = current.hasPassable(stack)[1]
                stack.append(current.id)
                self.pauseConnection(current, nextNode)
                pauseList[current.id] = [nextNode.id] if (current.id not in pauseList) else pauseList[current.id] + [nextNode.id]
                current = nextNode
                #print("  forward to: " + str(current.id))
            else:
                #reset passable of next nodes
                for tup in current.next.values():
                    if (tup[0].id != stack[-1] and current.id in pauseList and tup[0].id in pauseList[current.id]): #prevent inf. loop
                        self.resumeConnection(current, tup[0])
                        pauseList[current.id].remove(tup[0].id)
                #move backward
                current = self.nodes[stack.pop()]
                #print(" backward to: " + str(current.id))
            #print("------------------")

        return paths

def example():
    paths1 = [
    {"from": 0, "to": 1, "weight": 0},
    {"from": 0, "to": 3, "weight": 0},
    {"from": 1, "to": 2, "weight": 0},
    {"from": 1, "to": 4, "weight": 0},
    {"from": 1, "to": 0, "weight": 0},
    {"from": 2, "to": 1, "weight": 0},
    {"from": 2, "to": 5, "weight": 0},
    {"from": 3, "to": 0, "weight": 0},
    {"from": 3, "to": 4, "weight": 0},
    {"from": 3, "to": 6, "weight": 0},
    {"from": 4, "to": 3, "weight": 0},
    {"from": 4, "to": 1, "weight": 0},
    {"from": 4, "to": 5, "weight": 0},
    {"from": 4, "to": 7, "weight": 0},
    {"from": 5, "to": 4, "weight": 0},
    {"from": 5, "to": 2, "weight": 0},
    {"from": 5, "to": 8, "weight": 0},
    {"from": 6, "to": 3, "weight": 0},
    {"from": 6, "to": 7, "weight": 0},
    {"from": 7, "to": 6, "weight": 0},
    {"from": 7, "to": 4, "weight": 0},
    {"from": 7, "to": 8, "weight": 0},
    {"from": 8, "to": 7, "weight": 0},
    {"from": 8, "to": 5, "weight": 0},
    ]
    paths2 = [
    {"from": 0, "to": 1, "weight": 5},
    {"from": 0, "to": 2, "weight": 10},
    {"from": 1, "to": 2, "weight": 10},
    {"from": 1, "to": 3, "weight": 2},
    {"from": 2, "to": 3, "weight": 2},
    {"from": 2, "to": 4, "weight": 5},
    {"from": 3, "to": 2, "weight": 2},
    {"from": 3, "to": 4, "weight": 10}
    ]
    g = Graph(paths2)
    g.printGraph()
    print(g.pathsBetweenDFS(0, 4))

if __name__ == '__main__':
    example()
