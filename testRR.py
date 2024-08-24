# Define a class to store the process information
class Process:
    def __init__(self, pid, arrival, priority, burst):
        self.pid = pid # Process ID
        self.arrival = arrival # Arrival time
        self.priority = priority # Priority
        self.burst = burst # CPU burst
        self.remaining = burst # Remaining burst
        self.start = -1 # Start time
        self.finish = -1 # Finish time
        self.waiting = 0 # Waiting time
        self.turnaround = 0 # Turnaround time
        self.response = 0 # Response time

# Read the input file and store the processes in a list
processes = []
with open("list.txt", "r") as file:
    for line in file:
        pid, arrival, priority, burst = line.split(",")
        try:
            arrival= int(arrival)
            priority = int(priority)
            burst= int(burst)
        except ValueError:
            print(f"Error: Invalid data format in line {line}")

        processes.append(Process(pid, int(arrival), int(priority), int(burst)))

# Sort the processes by arrival time
processes.sort(key=lambda p: p.arrival)

# Define the time quantum for Round Robin scheduling
time_quantum = 4

# Initialize the current time and the ready queue
current_time = 0
ready_queue = []

# Define a function to check if all processes are finished
def is_all_done():
    for p in processes:
        if p.remaining > 0:
            return False
    return True

# Define a function to write the output to a file
def write_output():
    with open("testRR.txt", "w") as file:
        # Write the statistics for Round Robin algorithm
        throughput = len(processes) / current_time # Number of processes completed per unit time
        cpu_utilization = sum(p.burst for p in processes) / current_time # Fraction of time the CPU is busy
        avg_waiting = sum(p.waiting for p in processes) / len(processes) # Average waiting time
        avg_turnaround = sum(p.turnaround for p in processes) / len(processes) # Average turnaround time
        avg_response = sum(p.response for p in processes) / len(processes) # Average response time
        file.write(f"Throughput: {throughput}\n")
        file.write(f"CPU Utilization: {cpu_utilization}\n")
        file.write(f"Average Waiting Time: {avg_waiting}\n")
        file.write(f"Average Turnaround Time: {avg_turnaround}\n")
        file.write(f"Average Response Time: {avg_response}\n")

        # Write the information related to the sequence of execution of processes over time
        for p in processes:
            file.write(f"{p.pid}, {p.start}, {p.finish}\n")

# Run the Round Robin scheduling algorithm
while not is_all_done():
    # Add the processes that have arrived to the ready queue
    for p in processes:
        if p.arrival <= current_time and p.remaining > 0 and p not in ready_queue:
            ready_queue.append(p)

    # If the ready queue is not empty, select the first process and execute it
    if ready_queue:
        p = ready_queue.pop(0) # Dequeue the first process
        if p.start == -1: # If the process has not started yet, set its start time
            p.start = current_time
        if p.response == 0: # If the process has not responded yet, set its response time
            p.response = current_time - p.arrival
        # Execute the process for the minimum of time quantum and remaining burst
        execution = min(time_quantum, p.remaining)
        current_time += execution # Update the current time
        p.remaining -= execution # Update the remaining burst
        if p.remaining == 0: # If the process is finished, set its finish time
            p.finish = current_time
        # Update the waiting time and turnaround time for the other processes in the ready queue
        for q in ready_queue:
            q.waiting += execution # Increase the waiting time by the execution time
            q.turnaround += execution # Increase the turnaround time by the execution time
        # If the process is not finished, add it to the end of the ready queue
        if p.remaining > 0:
            ready_queue.append(p)
        # Update the turnaround time for the current process
        p.turnaround = current_time - p.arrival

# Write the output to the file
def run():
    write_output()
    print("Done. please check the outputfile.")


if __name__ == "__main__":
    run()