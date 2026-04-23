class MinHeap:

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def is_empty(self):
        return len(self.data) == 0

    def peek(self):
        if self.is_empty():
            return None
        return self.data[0]

    def insert(self, value):
        # Adiciona no final
        self.data.append(value)

        self._heapify_up(len(self.data) - 1)

    def extract_min(self):
        if self.is_empty():
            return None

        if len(self.data) == 1:
            return self.data.pop()

        root = self.data[0]

        self.data[0] = self.data.pop()

        self._heapify_down(0)

        return root

    @staticmethod
    def _parent(i): return (i - 1) // 2

    @staticmethod
    def _left(i): return 2 * i + 1

    @staticmethod
    def _right(i): return 2 * i + 2

    def _heapify_up(self, i):
        while i > 0:
            p = self._parent(i)

            if self.data[i] < self.data[p]:
                self.data[i], self.data[p] = self.data[p], self.data[i]
                i = p
            else:
                break

    def _heapify_down(self, i):
        n = len(self.data)

        while True:
            smallest = i
            l, r = self._left(i), self._right(i)

            if l < n and self.data[l] < self.data[smallest]:
                smallest = l

            if r < n and self.data[r] < self.data[smallest]:
                smallest = r

            if smallest == i:
                break

            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest

    def build(self, lst):
        self.data = list(lst)

        for i in range(len(self.data) // 2 - 1, -1, -1):
            self._heapify_down(i)

    def __repr__(self):
        return f"MinHeap({self.data[:10]}{'...' if len(self.data)>10 else ''})"


class MaxHeap:

    def __init__(self):
        self._h = MinHeap()

    def __len__(self):
        return len(self._h)

    def is_empty(self):
        return self._h.is_empty()

    def peek(self):
        top = self._h.peek()
        if top is None:
            return None

        neg, val = top
        return (-neg, val)

    def insert(self, priority, value):
        # Insere com prioridade negativa
        self._h.insert((-priority, value))

    def extract_max(self):
        item = self._h.extract_min()
        if item is None:
            return None

        neg, val = item
        return (-neg, val)

    def build(self, pairs):
        self._h.build([(-p, v) for p, v in pairs])

    def __repr__(self):
        return f"MaxHeap(size={len(self)})"


def top_k(pairs, k):

    heap = MinHeap()

    for priority, value in pairs:
        if len(heap) < k:
            heap.insert((priority, value))

        elif priority > heap.peek()[0]:
            heap.extract_min()
            heap.insert((priority, value))

    result = []
    while not heap.is_empty():
        result.append(heap.extract_min())

    result.reverse()

    return result