# # A function to read the input file and return a list of processes
class Process:
    def __init__(self, pid, arrival, priority, burst):
        self.pid = pid
        self.arrival = arrival
        self.priority = priority
        self.burst = burst
        self.start = -1
        self.finish = -1
        self.waiting = 0
        self.turnaround = 0
        self.response = 0

    def __str__(self):
        return f"{self.pid}, {self.start}, {self.finish}"

def read_input(filename):
    processes = []
    with open(filename, "r") as f:
        for line in f:
            pid, arrival, priority, burst = line.split(",")

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
        f.write("Sequence of execution:\n")
        for p in processes:
            f.write(str(p) + "\n")
def non_preemptive_sjf(processes):
    processes.sort(key=lambda p: p.burst) # sort by burst time
    n = len(processes)
    time = 0
    completed = 0
    idle = True
    running = None
    ready = []
    throughput = 0
    cpu_utilization = 0
    total_waiting = 0
    total_turnaround = 0 # the total turnaround time of all processes
    total_response = 0 # the total response time of all processes

    # Loop until all processes are completed
    while completed < n:
        for p in processes:
            if p.arrival == time:
                ready.append(p)

        if idle and ready:
            running = ready.pop(0) # get the first process in the ready queue
            idle = False
            if running.start == -1:
                running.start = time
                running.response = time - running.arrival
        if not idle:
            running.burst -= 1 # decrement the burst time of the running process
            if running.burst == 0:
                running.finish = time + 1
                running.waiting = running.finish - running.arrival - running.burst
                running.turnaround = running.finish - running.arrival
                completed += 1
                idle = True

                if running is not None: # Check if the running process is not None
                    total_waiting += running.waiting
                    total_turnaround += running.turnaround
                    total_response += running.response
                running = None


        time += 1
        if idle:
            cpu_utilization += 0
        else:
            cpu_utilization += 1
        for p in ready:
            p.waiting += 1
    throughput = completed / time
    cpu_utilization = (cpu_utilization / time) * 100
    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n
    avg_response = total_response / n
    return throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response
# Main function
def run():
    # Read the input file
    input_file = "list.txt"
    processes = read_input(input_file)

    # Simulate the preemptive SJF algorithm and get the statistics
    throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response = non_preemptive_sjf(processes)

    # Write the output file
    output_file = "SJF_NP.txt"
    write_output(output_file, processes, throughput, cpu_utilization, avg_waiting, avg_turnaround, avg_response)

    # Print a message to indicate the completion of the program
    print("Done. please check the outputfile.")


# Call the main function
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
# # A function to sort the processes by burst time
# def sort_by_burst(processes):
#     return sorted(processes, key=lambda p: p["burst"])
#
# def non_preemptive_sjf(processes, filename):
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
#     current_pid = -1 # Current process id
#
#     # Loop until all processes are executed
#     while executed < n:
#         # Add the processes that have arrived to the ready queue
#         for process in processes:
#             if process["arrival"] <= time and process["burst"] > 0:
#                 ready.append(process)
#
#         # Sort the ready queue by burst time
#         ready = sort_by_burst(ready)
#
#         # Check if the ready queue is empty
#         if not ready:
#             # Increment the current time
#             time += 1
#
#             # Continue the loop
#             continue
#
#         # Dequeue the shortest process from the ready queue
#         current = ready.pop(0)
#
#         # Check if the current process id is different from the previous one
#         if current_pid != current['pid']:
#             # Write the process id and a comma to the output string
#             output += "\n"
#             output += f"T{current['pid']}, "
#
#
#         # Update the current process id
#         current_pid = current['pid']
#
#         # Write the current time and a comma to the output string
#         output += f"{time}, "
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
#         # Write the current time and a comma to the output string
#         output += f"{time}, "
#
#         # Calculate the turnaround time for this process
#         turn = time - current["arrival"]
#
#         # Update the total turnaround time
#         turnaround += turn
#
#         # Calculate the waiting time for this process
#         wait = turn - current["burst"]
#
#         # Update the total waiting time
#         waiting += wait
#
#         # Update the number of executed processes
#         executed += 1
#         utilization += current["burst"]
#         current["burst"] = 0
#
#     # Write a newline to the output string
#     output += "\n"
#
#     throughput = executed / time
#
#     # Calculate the average waiting, turnaround and response time
#     avg_waiting = waiting / n
#     avg_turnaround = turnaround / n
#     avg_response = response / n
#
#     utilization = utilization / time * 100
#
#     # Write the statistics to the output string
#     output += f"Throughput: {throughput:.2f}\n"
#     output += f"CPU Utilization: {utilization:.2f}%\n"
#     output += f"Average Waiting Time: {avg_waiting:.2f}\n"
#     output += f"Average Turnaround Time: {avg_turnaround:.2f}\n"
#     output += f"Average Response Time: {avg_response:.2f}\n"
#     with open(filename, "w") as f:
#         f.write(output)
#
# # Read the input file
# processes = read_input("list.txt")
#
# # Call the non_preemptive_sjf function with the output file name
#
# def run():
#     non_preemptive_sjf(processes, "SJF_NP.txt")
#     print("Done. please check the outputfile.")
#
