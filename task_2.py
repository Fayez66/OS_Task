class Block:
    def __init__(self, start, size, pid=None):
        self.start = start
        self.size = size
        self.pid = pid  # None if free

    def __str__(self):
        if self.pid:
            return f"[{self.start}-{self.start+self.size-1}] PID: {self.pid}"
        else:
            return f"[{self.start}-{self.start+self.size-1}] FREE"

class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size
        self.memory = [Block(0, total_size)]

    def stat(self):
        print(" Current Memory Layout:")
        for block in self.memory:
            print(str(block))

    def allocate(self, pid, size):
        for i, block in enumerate(self.memory):
            if block.pid is None and block.size >= size:
                new_block = Block(block.start, size, pid)
                remaining_size = block.size - size
                if remaining_size > 0:
                    self.memory[i] = new_block
                    self.memory.insert(i+1, Block(block.start + size, remaining_size))
                else:
                    self.memory[i] = new_block
                print(f" Allocated {size} units to PID {pid}")
                return
        print(f" Allocation failed for PID {pid}, insufficient memory")

    def deallocate(self, pid):
        for block in self.memory:
            if block.pid == pid:
                block.pid = None
                print(f"🗑 Deallocated memory of PID {pid}")
                return
        print(f"️ PID {pid} not found")

    def compaction(self):
        print(" Running compaction...")
        new_memory = []
        current = 0
        for block in self.memory:
            if block.pid is not None:
                new_memory.append(Block(current, block.size, block.pid))
                current += block.size
        if current < self.total_size:
            new_memory.append(Block(current, self.total_size - current))
        self.memory = new_memory
        print(" Compaction complete")

def main():
    manager = MemoryManager(100)

    print(" Memory Manager Interactive Console")
    print("Commands: stat, allocate <pid> <size>, deallocate <pid>, compaction, exit")

    while True:
        cmd = input(">>> ").strip().split()
        if not cmd:
            continue
        action = cmd[0]

        if action == "stat":
            manager.stat()
        elif action == "allocate" and len(cmd) == 3:
            pid = cmd[1]
            size = int(cmd[2])
            manager.allocate(pid, size)
        elif action == "deallocate" and len(cmd) == 2:
            pid = cmd[1]
            manager.deallocate(pid)
        elif action == "compaction":
            manager.compaction()
        elif action == "exit":
            print(" Exiting Memory Manager.")
            break
        else:
            print(" Invalid command")

if __name__ == "__main__":
    main()
