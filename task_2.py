import random
import sys

# Constants
DISK_SIZE = 5000
NUM_REQUESTS = 1000

def generate_requests():
    return random.sample(range(DISK_SIZE), NUM_REQUESTS)

def fcfs(requests, head):
    movement = 0
    for r in requests:
        movement += abs(r - head)
        head = r
    return movement

def scan(requests, head, direction='up'):
    movement = 0
    requests.sort()
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    if direction == 'up':
        for r in right:
            movement += abs(r - head)
            head = r
        if left:
            movement += abs(head - (DISK_SIZE - 1))
            head = DISK_SIZE - 1
            for r in reversed(left):
                movement += abs(r - head)
                head = r
    else:
        for r in reversed(left):
            movement += abs(r - head)
            head = r
        if right:
            movement += abs(head - 0)
            head = 0
            for r in right:
                movement += abs(r - head)
                head = r

    return movement

def c_scan(requests, head, direction='up'):
    movement = 0
    requests.sort()
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    if direction == 'up':
        for r in right:
            movement += abs(r - head)
            head = r
        if left:
            movement += abs(head - (DISK_SIZE - 1))  # Go to end
            movement += DISK_SIZE - 1  # Jump to start (circular)
            head = 0
            for r in left:
                movement += abs(r - head)
                head = r
    else:
        for r in reversed(left):
            movement += abs(r - head)
            head = r
        if right:
            movement += abs(head - 0)
            movement += DISK_SIZE - 1  # Jump to end
            head = DISK_SIZE - 1
            for r in reversed(right):
                movement += abs(r - head)
                head = r

    return movement

def main():
    if len(sys.argv) != 2:
        print("Usage: python disk_schedule.py <initial_head_position>")
        return

    try:
        initial_head = int(sys.argv[1])
        if not 0 <= initial_head < DISK_SIZE:
            raise ValueError
    except ValueError:
        print(f"Initial head position must be an integer between 0 and {DISK_SIZE - 1}")
        return

    requests = generate_requests()

    print(f"Initial Head Position: {initial_head}")
    print(f"FCFS Total Movement: {fcfs(requests, initial_head)}")
    print(f"SCAN Total Movement: {scan(requests, initial_head)}")
    print(f"C-SCAN Total Movement: {c_scan(requests, initial_head)}")

if __name__ == "__main__":
    main()
