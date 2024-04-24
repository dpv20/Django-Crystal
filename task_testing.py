import datetime

# Get the current time
current_time = datetime.datetime.now()

# Open the file in append mode, or create it if it doesn't exist
with open("time_log.txt", "a") as file:
    # Write the hour to the file and a newline character
    file.write(f"{current_time.strftime('%H:%M:%S')}\n")
