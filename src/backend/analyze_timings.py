import re


# Regular expression to match the output lines
pattern = re.compile(r"import time:\s+(\d+)\s\|\s+(\d+)\s\|\s+(\S+)")

# Dictionary to store the cumulative times
cumulative_times = {}

# Parse the output
with open("import_time.txt") as f:
    output = f.read()
    for line in output.splitlines():
        match = pattern.match(line)
        if match:
            time, cumulative_time, module = match.groups()
            cumulative_times[module] = int(cumulative_time) /1000000 

    # Find the module with the largest cumulative time
    largest_module = max(cumulative_times, key=cumulative_times.get)

    print(f"The module with the largest cumulative time is {largest_module} with a time of {cumulative_times[largest_module]} seconds.")
    # print(sorted(cumulative_times.items(), key=lambda x: x[1], reverse=True)[:100])        
    # Sort the cumulative times in descending order
    sorted_times = sorted(cumulative_times.items(), key=lambda x: x[1], reverse=True)

    # Print the sorted times
    for module, time in sorted_times[:10]:
        print(f"{module}: {time} seconds")
    print("total time is ", sum(cumulative_times.values()), " seconds")
        