# A function to read the input file and return a list of processes
def read_input(filename):
    processes = []
    with open(filename, "r") as f:
        for line in f:
            # Split the line by commas and convert to integers
            pid, arrival, priority, burst = line.split(',')
            # Remove the 'P' from the pid and convert to integer
            pid = int(pid.strip('P'))
            # Convert the other values to integers
            try:
                arrival = int(arrival)
                priority = int(priority)
                burst = int(burst)
            except ValueError:
                print(f"Error: Invalid data format in line {line}")
                exit()
            # Create a process dictionary with the given attributes
            process = {"pid": pid, "arrival": arrival, "priority": priority, "burst": burst}
            # Append the process to the list
            processes.append(process)
    return processes
# A function to sort the processes by arrival time
def sort_by_arrival(processes):
    return sorted(processes, key=lambda p: p["arrival"])

# A function to calculate the FCFS statistics and write the output file
def fcfs(processes, filename):
    # Initialize the variables
    n = len(processes) # Number of processes
    time = 0 # Current time
    waiting = 0 # Total waiting time
    turnaround = 0 # Total turnaround time
    response = 0 # Total response time
    executed = 0 # Number of executed processes
    utilization = 0 # CPU utilization
    output = "" # Output string
    prev_pid = None # Previous process id

    # Loop through the processes in order of arrival
    for process in sort_by_arrival(processes):
        # Get the process attributes
        pid = process["pid"]
        arrival = process["arrival"]
        priority = process["priority"]
        burst = process["burst"]

        # Update the current time to the maximum of the previous time and the arrival time
        time = max(time, arrival)

        # Calculate the waiting time for this process
        wait = time - arrival

        # Calculate the turnaround time for this process
        turn = wait + burst

        # Calculate the response time for this process
        resp = wait

        # Update the total waiting, turnaround and response time
        waiting += wait
        turnaround += turn
        response += resp

        # Update the number of executed processes
        executed += 1

        # Update the CPU utilization
        utilization += burst

        # Write the process information to the output string
        # If the previous process id is different from the current one, write a new line
        if prev_pid != pid:
            output += f"\nP{pid}, "
        # Write the start and end time of the execution
        output += f"{time}, {time + burst}, "

        # Update the previous process id
        prev_pid = pid

        # Update the current time to the end of the execution
        time += burst

    # Calculate the throughput
    throughput = executed / time

    # Calculate the average waiting, turnaround and response time
    avg_waiting = waiting / n
    avg_turnaround = turnaround / n
    avg_response = response / n

    # Calculate the CPU utilization percentage
    utilization = utilization / time * 100

    # Write the statistics to the output string
    output += f"\n\nThroughput: {throughput:.2f}\n"
    output += f"CPU Utilization: {utilization:.2f}%\n"
    output += f"Average Waiting Time: {avg_waiting:.2f}\n"
    output += f"Average Turnaround Time: {avg_turnaround:.2f}\n"
    output += f"Average Response Time: {avg_response:.2f}\n"

    # Write the output string to the output file
    with open(filename, "w") as f:
        f.write(output)

# Read the input file
processes = read_input("list.txt")

# Call the fcfs function with the output file name

def run():
    fcfs(processes, "FCFS.txt")
    print("Done. please check the outputfile.")

