class Process:
    def __init__(self, pid, arrival, priority, burst):
        self.pid = pid # process ID
        self.arrival = arrival # arrival time
        self.priority = priority # priority
        self.burst = burst # CPU burst
        self.start = -1 # start time
        self.finish = -1 # finish time
        self.waiting = 0 # waiting time
        self.turnaround = 0 # turnaround time
        self.response = 0 # response time

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

def write_output(filename, processes, throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response):
    with open(filename, "w") as f:
        f.write(f"Throughput: {throughput}\n")
        f.write(f"CPU Utilization: {cpu_utilization}\n")
        f.write(f"Average Waiting Time: {avg_waiting}\n")
        f.write(f"Average Turnaround Time: {avg_turnaround}\n")
        f.write(f"Average Response Time: {avg_response}\n")
        f.write("Sequence of execution of processes:\n")
        for p in processes:
            f.write(str(p) + "\n")

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

    # Calculate the throughput, CPU utilization, and average times
    throughput = len(processes) / processes[-1].finish
    cpu_utilization = (total_burst / processes[-1].finish)*100
    avg_waiting = total_waiting / len(processes)
    avg_turnaround = total_turnaround / len(processes)
    avg_response = total_response / len(processes)

    return throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response

def non_preemptive_priority(processes):
    time = 0
    queue = []
    finished_processes = []
    while processes or queue:
        while processes and processes[0].arrival <= time:
            queue.append(processes.pop(0))
        if queue:
            queue.sort(key=lambda p: p.arrival) # sort the queue by arrival time
            p = min(queue, key=lambda p: p.priority) # get the process with the highest priority
            queue.remove(p) # remove the process from the queue
            if p.start == -1:
                p.start = time
            time += p.burst # increment the time by the burst time of the process
            p.finish = time # set the finish time of the process
            finished_processes.append(p) # add the process to the list of finished processes
        # If the queue is empty, increment the time
        else:
            time += 1

    # Return the list of finished processes
    return finished_processes


# Main function
def run():
    # Read the input file and get the list of processes
    processes = read_input("list.txt")

    # Simulate the priority with preemption algorithm and get the list of processes
    processes = non_preemptive_priority(processes)

    # Calculate the statistics and get them
    throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response = calculate_statistics(processes)

    # Write the output file with the statistics
    write_output("Priority_NP.txt", processes, throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response)
    # Call the main function
    print("Done. please check the outputfile.")


if __name__ == "__main__":
    run()
# def read_input(filename):
#     processes = []
#     with open(filename, "r") as f:
#         for line in f:
#             # Split the line by commas and convert to integers
#             pid, arrival, priority, burst = line.split(',')
#             # Remove the 'P' from the pid and convert to integer
#             pid = int(pid.strip('P'))
#             # Convert the other values to integers
#             arrival = int(arrival)
#             priority = int(priority)
#             burst = int(burst)
#             # Create a process dictionary with the given attributes
#             process = {"pid": pid, "arrival": arrival, "priority": priority, "burst": burst}
#             # Append the process to the list
#             processes.append(process)
#     return processes
#
# # A function to sort the processes by priority
# def sort_by_priority(processes):
#     return sorted(processes, key=lambda p: p["priority"])
#
# # A function to calculate the Non-preemptive priority statistics and write the output file
# def non_preemptive_priority(processes, filename):
#     # Initialize the variables
#     n = len(processes) # Number of processes
#     time = 0 # Current time
#     waiting = 0 # Total waiting time
#     turnaround = 0 # Total turnaround time
#     response = 0 # Total response time
#     executed = 0 # Number of executed processes
#     utilization = 0 # CPU utilization
#     output = "" # Output string
#     ready = [] # Ready queue
#     # Create a dictionary to map the process ids to the process names
#     names = {1: "T1", 2: "T2", 3: "T3", 4: "T4", 5: "T5"}
#
#     # Loop until all processes are executed
#     while executed < n:
#         # Add the processes that have arrived to the ready queue
#         for process in processes:
#             if process["arrival"] <= time and process["burst"] > 0:
#                 ready.append(process)
#
#         # Sort the ready queue by priority
#         ready = sort_by_priority(ready)
#
#         # Check if the ready queue is empty
#         if not ready:
#             # Increment the current time
#             time += 1
#
#             # Continue the loop
#             continue
#
#         # Dequeue the highest priority process from the ready queue
#         current = ready.pop(0)
#
#         # Write the process name, start time and finish time for this process to the output string
#         output += f"{names[current['pid']]} {time} {time + current['burst']}\n"
#
#         # Calculate the response time for this process
#         resp = time - current["arrival"]
#
#         # Update the total response time
#         response += resp
#
#         # Execute the current process for its burst time
#         time += current["burst"]
#
#         # Calculate the turnaround time for this process
#         turn = time - current["arrival"]
#         turnaround += turn
#         wait = turn - current["burst"]
#         waiting += wait
#         executed += 1
#         utilization += current["burst"]
#         current["burst"] = 0
#     throughput = executed / time
#     avg_waiting = waiting / n
#     avg_turnaround = turnaround / n
#     avg_response = response / n
#     utilization = utilization / time * 100
#     output += f"Throughput: {throughput:.2f}\n"
#     output += f"CPU Utilization: {utilization:.2f}%\n"
#     output += f"Average Waiting Time: {avg_waiting:.2f}\n"
#     output += f"Average Turnaround Time: {avg_turnaround:.2f}\n"
#     output += f"Average Response Time: {avg_response:.2f}\n"
#     with open(filename, "w") as f:
#         f.write(output)
# processes = read_input("list.txt")
#
# def run():
#     non_preemptive_priority(processes, "Priority_NP.txt")
#     print("Done. please check the outputfile.")
