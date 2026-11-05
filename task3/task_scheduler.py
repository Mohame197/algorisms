from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Task:
    name: str
    priority: int
    arrival_time: int

    def key(self):
        return self.priority, -self.arrival_time, self.name


class MaxHeap:
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def insert(self, task):
        self.data.append(task)
        i = len(self.data) - 1
        while i > 0:
            parent = (i - 1) // 2
            if self.data[parent].key() >= self.data[i].key():
                break
            self.data[parent], self.data[i] = self.data[i], self.data[parent]
            i = parent

    def extract_max(self):
        if not self.data:
            raise IndexError("extract_max from empty heap")
        maximum = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._max_heapify(0)
        return maximum

    def _max_heapify(self, i):
        n = len(self.data)
        while True:
            left = 2 * i + 1
            right = left + 1
            largest = i
            if left < n and self.data[left].key() > self.data[largest].key():
                largest = left
            if right < n and self.data[right].key() > self.data[largest].key():
                largest = right
            if largest == i:
                return
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            i = largest


def heap_schedule(tasks):
    queue = MaxHeap()
    for task in tasks:
        queue.insert(task)
    order = []
    while queue:
        order.append(queue.extract_max())
    return order


def sorted_list_schedule(tasks):
    queue = []
    for task in tasks:
        queue.append(task)
        queue.sort(key=lambda item: item.key(), reverse=True)
    return [queue.pop(0) for _ in range(len(queue))]


def format_order(tasks):
    return " -> ".join(
        f"{task.name}(p={task.priority}, t={task.arrival_time})"
        for task in tasks
    )


def main():
    generator = random.Random(314)
    tasks = [
        Task(f"T{i:02d}", generator.randint(1, 10), i)
        for i in range(1, 21)
    ]
    heap_order = heap_schedule(tasks)
    list_order = sorted_list_schedule(tasks)
    print("Generated tasks:")
    print(", ".join(f"{t.name}(p={t.priority}, t={t.arrival_time})" for t in tasks))
    print("\nMax-heap run order:")
    print(format_order(heap_order))
    print("\nSorted-list run order:")
    print(format_order(list_order))
    print("\nOrders match:", heap_order == list_order)


if __name__ == "__main__":
    main()
