class Process:
    def __init__(self, pid, arrival, priority, burst):
        self.pid = pid
        self.arrival = arrival
        self.priority = priority
        self.burst = burst
        self.remaining = burst
        self.start = -1
        self.finish = -1
        self.waiting = 0
        self.turnaround = 0
        self.response = 0

    def __str__(self):
        return f"{self.pid} {self.start} {self.finish}"

def read_input(filename):
    processes = []
    with open(filename, "r") as f:
        for line in f:
            pid, arrival, priority, burst = line.split(',')
            try:
                arrival = int(arrival)
                priority = int(priority)
                burst = int(burst)
            except ValueError:
                print(f"Error: Invalid data format in line {line}")
                exit()
            processes.append(Process(pid, arrival, priority, burst))
    return processes

def write_output(filename, processes, throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response, sequence):
    with open(filename, "w") as f:
        f.write(f"Throughput: {throughput}\n")
        f.write(f"CPU Utilization: {cpu_utilization}\n")
        f.write(f"Average Waiting Time: {avg_waiting}\n")
        f.write(f"Average Turnaround Time: {avg_turnaround}\n")
        f.write(f"Average Response Time: {avg_response}\n")
        f.write("Sequence of execution of processes:\n")
        for processID, start, end in sequence:
            f.write(f"{processID}, {start}, {end}\n")

def calculate_statistics(processes):
    throughput = 0
    cpu_utilization = 0
    avg_waiting = 0
    avg_turnaround = 0
    avg_response = 0
    total_waiting = 0
    total_turnaround = 0
    total_response = 0
    total_burst = 0
    for p in processes:
        p.waiting = p.finish - p.arrival - p.burst
        p.turnaround = p.finish - p.arrival
        p.response = p.start - p.arrival
        total_waiting += p.waiting
        total_turnaround += p.turnaround
        total_response += p.response
        total_burst += p.burst
    throughput = len(processes) / processes[-1].finish
    cpu_utilization = (total_burst / processes[-1].finish)*100
    avg_waiting = total_waiting / len(processes)
    avg_turnaround = total_turnaround / len(processes)
    avg_response = total_response / len(processes)
    return throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response

def priority_preemption(processes):
    # Initialize the time, the ready queue, and the finished processes list

    time = 0
    queue = []
    finished_processes = []
    sequence = [] # initialize the sequence of execution list
    # Loop until all processes are finished
    while processes or queue:
        # Add the processes that have arrived to the queue
        while processes and processes[0].arrival <= time:
            queue.append(processes.pop(0))
        # If the queue is not empty, select the process with the highest priority
        if queue:
            queue.sort(key=lambda p: p.priority)
            # sort the queue by priority
            p = queue[0] # get the first process in the queue
            # If the process has not started yet, set its start time
            if p.start == -1:
                p.start = time
            # Execute the process for one unit of time
            p.remaining -= 1
            time += 1
            # If the process is finished, set its finish time,
            # remove it from the queue, and add it to the finished processes list
            if p.remaining == 0:
                p.finish = time
                queue.pop(0)
                finished_processes.append(p)
            # update the sequence of execution list
            if sequence and sequence[-1][0] == p.pid: # if the last tuple in the list has the same process ID as the current process
                sequence[-1] = (p.pid, sequence[-1][1], time) # update the end time of the last tuple
            else: # if the last tuple in the list has a different process ID or the list is empty
                sequence.append((p.pid, time - 1, time)) # append a new tuple with the current process ID and start and end time
        # If the queue is empty, increment the time
        else:
            time += 1
    return finished_processes, sequence # return the sequence of execution list along with the finished processes list

def run():
    # Read the input file and get the list of processes
    processes = read_input("list.txt")
    # Simulate the priority with preemption algorithm and get the list of processes
    processes, sequence = priority_preemption(processes) # get the sequence of execution list from the function
    # Calculate the statistics and get them
    throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response = calculate_statistics(processes)
    # Write the output file with the statistics
    write_output("Priority_P.txt", processes, throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response, sequence) # pass the sequence of execution list to the write_output function
    # Call the main function
    print("Done. please check the outputfile.")


if __name__ == "__main__":
    run()
