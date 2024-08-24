import FCFS
import Priority_NP
import Priority_P
import RR
import SJF_NP
import SJF_P

files = {
    "1": FCFS,
    "2": Priority_NP,
    "3": Priority_P,
    "4": RR,
    "5": SJF_NP,
    "6": SJF_P
}
loop = True
while loop:
    choice = input("Which file do you want to run?  \n 1) FCFS \n 2) Priority_NP \n 3) Priority_P \n "
                   "4) RR \n 5) SJF_NP \n 6) SJF_P \n please write the number (1-6):\n "
                   "if you wish to exit the program press e: \n")
    if choice in files:
        # Run the chosen file and get the output
        output = files[choice].run()
        # Get the name of the output file
        file_name = files[choice].__name__ + ".txt" # Use the __name__ attribute of the module object
        # Open the output file in read mode
        with open(file_name, "r") as file:
            # Iterate over the lines of the file
            for line in file:
                # Print each line of the file
                print(line)

    elif choice == "e":
        loop = False

    else:
        print("Invalid choice. Please enter a number from 1 to 6.")
