import heapq

class OpenList:
    # heap: list<(priority, node)>
    def __init__(self):
        self.heap = []

    def push(self, newItem):
        for idx in range(len(self.heap)):
            if newItem[1] == self.heap[idx][1]:
                if newItem[0] < self.heap[idx][0]:
                    self.heap[idx] = newItem
                    heapq.heapify(self.heap)
                return
        heapq.heappush(self.heap, newItem)

    def pop(self):
        if len(self.heap) > 0:
            prio, rtNode = heapq.heappop(self.heap)
            return rtNode
        return None

    def getLength(self):
        return len(self.heap)