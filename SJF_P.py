
def main(MODE):
    # Initialize, Get .txt file and turn it into nested lists
    # Get process count
    # This code snippet opens a file named list.txt in read mode and assigns it to a variable named fp.
    # Then, it loops through each line of the file and assigns the line number to Pcount and the line content to line
    with open('list.txt') as fp:
        for Pcount, line in enumerate(fp):
            pass

    # initialize our lists
    # It initializes three empty lists: reallist, proglist, and reportlist.
    # Each list has Pcount + 1 sublists, where Pcount is the number of lines in the file.
    # PROCESS, ARRIVAL, PRIORITY, BURST
    reallist = [[] for i in range(Pcount + 1)]

    # PROCESS, START1, FINISH1, START2, FINISH2 ...
    proglist = [[] for i in range(Pcount + 1)]

    # PROCESS, TURNAROUND, WAITING, RESPONSE
    reportlist = [[] for i in range(Pcount + 1)]

    # It opens the file list.txt again and loops through each line.
    # For each line, it splits the line by whitespace and removes any commas from the elements.
    # Then, it appends the elements to the corresponding sublist in reallist.
    with open('list.txt') as fp:
        for Pcount, line in enumerate(fp):
            for i in line.split():
                reallist[Pcount].append(i.replace(',', ''))
            pass

    # It loops through each sublist in reallist and converts the elements from index 1 to 3 to integers.
    # index zero is the name of the process that needs no conversion, hence starting from 1
    # This is done because the elements in reallist are strings,
    # and they need to be converted to numbers for calculations.
    for i in range(len(reallist)):
        for y in range(1, 4):
            try:
                reallist[i][y] = int(reallist[i][y])
            except ValueError:
                print("ERROR: Malformed input in index [" + str(i) + '][' + str(y) + '] as "' + reallist[i][y] + '"')
                exit()

    # It loops through each sublist in reallist again and appends the first element
    # (which is the process ID) to the corresponding sublists in proglist and reportlist.
    # This is done to initialize the lists for storing the calculated values for each process.
    # setup lists for modification and reports
    for i in range(len(reallist)):
        proglist[i].append(reallist[i][0])
        reportlist[i].append(reallist[i][0])

    # It loops through each sublist in reportlist and appends three values: 0, 0, and -1.
    # These are the initial values for the turnaround time, waiting time, and response time for each process.
    # The response time is set to -1 to indicate that the process has not been responded to yet.
    # Setup report list to PROCESS 0 0 -1
    for i in range(len(reportlist)):
        reportlist[i].append(0)
        reportlist[i].append(0)
        # response time -1 if hasnt been responded to
        reportlist[i].append(-1)

    # It assigns reallist to fakelist.
    # This creates a reference to the same list object, not a copy.
    # Any changes made to fakelist will also affect reallist, and vice versa.
    fakelist = reallist

    loop = True
    # TIMER: This keeps track of the current time in the simulation.
    TIMER = 0
    # NOTHINGCOUNTER: This counts how many times the CPU does nothing because no process has arrived or is ready to run.
    NOTHINGCOUNTER = 0

    # X:This is a variable that is used to store the index of the process that is currently running
    # or has just finished running.
    X = 0
    # DEBUG: This is a flag that controls whether to print some debugging information or not.
    DEBUG = 1

    # It uses the match statement to assign the appropriate file name to fname based on the value of MODE.
    match MODE:

        case 6:
            fname = "SJF_P.txt"


    # It enters the main loop, which runs until loop is set to False. Inside the loop, it does the following:
    # It calls a function named NoArrival to check if there is any process that has arrived at the current time.
    # If not, it increments TIMER by 1, increments NOTHINGCOUNTER by 1,
    # and calls two functions named addTurnaroundtime and addWaitingtime
    # to update the turnaround time and waiting time for all the processes in reportlist.
    # Main Loop
    while loop:
        # IF NOTHING HAS ARRIVED, TIMER + 1
        if NoArrival(fakelist, TIMER, Pcount + 1):
            TIMER = TIMER + 1
            # CPU DOES NOTHING
            NOTHINGCOUNTER = NOTHINGCOUNTER + 1
            # THESE WILL GET REDUCED IN THE END
            addTurnaroundtime(fakelist, reportlist, 1)
            addWaitingtime(-5, fakelist, reportlist, 1)

        # It loops through each sublist in fakelist and checks if the process has arrived and has a positive burst time.
        # If not, it skips the process and moves on to the next one.
        for i in range(len(fakelist)):
            # IF ARRIVAL TIME IS HIGHER THAN CURRENT TIMER OR BURST TIME = 0 GO TO THE NEXT PROCESS
            if not isArrived(i, fakelist, TIMER) or fakelist[i][3] <= 0:
                continue

            match MODE:

                case 6:
                    # If there is a active process with a burst time lower than the current one, skip.
                    if compareBurst(fakelist[i][0], fakelist, fakelist[i][3], timer=TIMER):
                        continue
                    TIMER = SJF_P(fakelist[i][0], i, flist=fakelist, plist=proglist, rlist=reportlist, timer=TIMER)


        # If there is no burst available in all processes, EXIT the while loop!
        # It breaks the loop if noBurstAvailable returns True,
        # meaning that all the processes have finished their execution.
        if noBurstAvailable(fakelist, Pcount + 1):
            break

        # It increments the loop counter X by 1 after each cycle.
        X = X + 1

    # WHILE LOOP HAS ENDED
    # Finish the calculation of turnaround and waiting by decreasing arrival timer from all
    # t calls two functions named finishTurnaroundtime and finishWaitingtime
    # to finalize the calculation of the turnaround time and waiting time for each process in reportlist.
    # These functions take the list of processes and the report list as parameters,
    # and subtract the arrival time from the turnaround time and waiting time.
    finishTurnaroundtime(fakelist, reportlist)
    finishWaitingtime(fakelist, reportlist)

    # Generate report and put into file
    # It calls a function named generateReport to write the output of the program to a file.
    # This function takes the report list, the prog list, the number of processes, the timer,
    # the nothing counter, and the file name as parameters, and formats the data into a table and a chart.
    generateReport(reportlist, proglist, Pcount + 1, TIMER, NOTHINGCOUNTER, fname)


# Checks the list to see if all bursts are 0
# noBurstAvailable: This returns True if all the processes have zero burst time, and False otherwise.
# It takes the list of processes and the number of processes as parameters.
def noBurstAvailable(list, size):
    counter = 0
    for i in range(len(list)):
        if list[i][3] == 0:
            counter = counter + 1
    if counter == size:
        return True
    else:
        return False

# howmanyCompleted: This returns the number of processes that have zero burst time.
# It takes the list of processes as a parameter.
# Check how many have burst == 0
def howmanyCompleted(list):
    counter = 0
    for i in range(len(list)):
        if list[i][3] == 0:
            counter = counter + 1
    return counter

# NoArrival: This returns True if all the processes have arrival time greater than the current time,
# and False otherwise. It takes the list of processes, the current time,
# and the number of processes as parameters.
# Checks the list to see if all arrivals are bigger than the current timer
def NoArrival(list, timer, size):
    counter = 0
    size = size - howmanyCompleted(list)
    for i in range(len(list)):
        if list[i][1] > timer:
            counter = counter + 1
    if counter == size:
        return True
    else:
        return False

#  This adds the waiting time to all the processes that have arrived, except the one that is currently running.
#  It takes the process ID, the list of processes, the report list,
#  and the amount of time to add as parameters.
#  It returns the updated report list.
# Add waiting time to all processes that have arrived except the one
def addWaitingtime(process, list, rlist, n):
    for i in range(len(rlist)):
        if process == rlist[i][0]:
            continue
        # HARD-CODED -5 TO ADD WAITING TIME TO ALL
        elif list[i][3] > 0 or process == -5:
            rlist[i][2] += n
    return rlist

# This adds the turnaround time to all the processes that have positive burst time.
# It takes the list of processes, the report list, and the amount of time to add as parameters.
# It returns the updated report list.
# Add turnaround time to all processes
def addTurnaroundtime(list, rlist, n):
    for i in range(len(rlist)):
        if list[i][3] > 0:
            rlist[i][1] += n
    return list

# This finalizes the waiting time for each process by subtracting the arrival time from it.
# It takes the list of processes and the report list as parameters.
# It returns the updated list of processes.
# Final waiting time = waiting time - time before arrival
def finishWaitingtime(list, rlist):
    for i in range(len(rlist)):
        rlist[i][2] = rlist[i][2] - list[i][1]
    return list

# This finalizes the turnaround time for each process by subtracting the arrival time from it.
# It takes the list of processes and the report list as parameters.
# It returns the updated list of processes.
# Final turnaround time = turnaround time - time before arrival
def finishTurnaroundtime(list, rlist):
    for i in range(len(rlist)):
        rlist[i][1] = rlist[i][1] - list[i][1]
    return list

# This sets the response time for a process if it has not been set yet.
# It takes the index of the process, the list of processes, the report list, and the current time as parameters.
# It returns the updated report list.
# Set Response time if there is none
def addResponsetime(pnumber, list, rlist, timer):
    if rlist[pnumber][3] == -1:
        rlist[pnumber][3] = timer - list[pnumber][1]
    return rlist

#
# This runs the process with the shortest remaining burst time among the ready processes.
# It preempts the current process if a new process arrives with a shorter burst time.
# It takes the process ID, the index, the lists, and the timer as parameters,
# and returns the updated timer value.
# It also updates the waiting time, turnaround time, and response time for the process,
# and appends the start time and finish time to the prog list.
def SJF_P(process, pnumber, flist, plist, rlist, timer):
    # Add Response time
    addResponsetime(pnumber, flist, rlist, timer)
    # Append the progress list with entering time
    plist[pnumber].append(timer)

    # Be in the current process until a process with lower burst time is detected
    # Time moves 1 unit at a time
    while True:
        # Add Turnaround and waiting time
        addWaitingtime(process, flist, rlist, 1)
        addTurnaroundtime(flist, rlist, 1)
        # Increase TIMER
        timer += 1
        # Reduce burst
        flist[pnumber][3] = flist[pnumber][3] - 1
        # If there is a lower burst time available or burst == 0, exit the loop
        if compareBurst(process, flist, flist[pnumber][3], timer) or flist[pnumber][3] <= 0:
            break

    # Append the progress list with exiting time
    plist[pnumber].append(timer)
    return timer


# This returns True if the process has arrived at or before the current time,
# and False otherwise.
# It takes the index of the process, the list of processes, and the current timer as parameters.
# Check if the process has arrived
def isArrived(pnumber, list, timer):
    if int(list[pnumber][1]) <= timer:
        return True
    else:
        return False

# This returns True if there is another process that has arrived earlier than the current process,
# and False otherwise.
# It takes the current process ID, the list of processes, and the current arrival time as parameters.
# Compares current arrival with others that also have a bursting time, if there exists one with lower time, return true
def compareArrival(process, list, arrival):
    for i in range(len(list)):
        if process == list[i][0]:
            continue
        elif list[i][1] == arrival and list[i][3] > 0 and int(list[i][0][1]) < int(process[1]):
            return True
        elif list[i][1] < arrival and list[i][3] > 0:
            return True
    else:
        return False

# This returns True if there is another process that has a shorter burst time than the current process,
# and False otherwise.
# It takes the current process ID, the list of processes, the current burst time, and the current timer as parameters.
# It also checks if the other process has arrived and has a positive burst time.
# Compares current burst time with others that have arrived, if there exists one with lower time, return true
def compareBurst(process, list, burst, timer):
    for i in range(len(list)):
        if process == list[i][0]:
            continue
        elif list[i][3] == burst and list[i][3] > 0 and int(list[i][0][1]) < int(process[1]):
            return True
        elif list[i][3] < burst and list[i][3] > 0 and isArrived(i, list, timer):
            return True
    else:
        return False

# This returns True if there is another process that has a higher priority than the current process,
# and False otherwise.
# It takes the current process ID, the list of processes, the current priority, and the current timer as parameters.
# It also checks if the other process has arrived and has a positive burst time.
# Compares current priority with others that have arrived, if there exists one with higher priority, return true
def comparePriority(process, list, prio, timer):
    for i in range(len(list)):
        if process == list[i][0]:
            continue
        elif list[i][2] == prio and list[i][3] > 0 and int(list[i][0][1]) < int(process[1]):
            return True
        elif list[i][2] < prio and list[i][3] > 0 and isArrived(i, list, timer):
            return True
    else:
        return False

# This writes the results of the CPU scheduling algorithm to a file.
# It takes the report list, the prog list, the number of processes, the timer, the nothing counter,
# and the file name as parameters.
# It calculates and writes the throughput, CPU utilization, average waiting time,
# average turnaround time, average response time, and execution of processes over time to the file.
# Generate the requested results into a .txt file
def generateReport(rlist, plist, size, timer, badcounter, filename):
    writer = open(filename, "w")
    # Throughput
    writer.write("Throughput:                         " + str(size / timer) + "\n")
    # CPU Utilization
    writer.write("CPU Utilization:                    " + str(((timer - badcounter) * 100) / timer) + "\n")
    # Average Waiting Time
    taverage = 0
    waverage = 0
    raverage = 0
    for i in range(len(rlist)):
        taverage = taverage + rlist[i][1]
        waverage = waverage + rlist[i][2]
        raverage = raverage + rlist[i][3]
    writer.write("Average Waiting Time:               " + str(waverage / size) + "\n")
    # Average Turnaround Time
    writer.write("Average Turnaround Time:            " + str(taverage / size) + "\n")
    # Average Response Time
    writer.write("Average Response Time:              " + str(raverage / size) + "\n")
    # execution of processes over time
    writer.write("Execution of processes overtime:\n")
    for i in range(len(plist)):
        for y in range(len(plist[i])):
            writer.write(str(plist[i][y]).replace('P', 'T') + ', ')
        writer.write('\n')

def run():
    main(6)
    # Print a message to indicate the completion of the program
    print("Done. please check the outputfile.")


if __name__ == "__main__":
    run()























