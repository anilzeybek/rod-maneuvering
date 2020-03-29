class PriorityQueue:
    def __init__(self):
        self.q = []

    def __str__(self):
        return str(self.q)

    def push(self, priority, value):
        # TODO: burasi yanlis, arka arkaya pop yapabilir!!!
        if not self.is_empty() and priority > self.q[0][0]:
            self.q.insert(0, (priority, value))
        else:
            self.q.append((priority, value))

    def pop(self):
        return self.q.pop(0)[1]

    def is_empty(self):
        return False if self.q else True
