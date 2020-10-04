class Venue:
    def __init__(self, capacity, space=True):
        self._capacity = capacity
        self._space = True
        self._count = 0
    def person_entered(self):
        self._count += 1
    def person_left(self):
        self._count -= 1
    def get_count(self):
        return self._count
    def get_capacity(self):
        return self._capacity
    def get_space(self):
        return self._space
    def is_full(self):
        self._space = False
    def not_full(self):
        self._space = True
    def print_cur_visitors(self):
        print("there are ", self._count, " people at the venue")
