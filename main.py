import queue
import csv

# Dataset name
data_file = "CalIt2/CalIt2.data"

# Create a queue to handle incoming data
data_queue = queue.Queue()

# Create a dictionary to store the counter
counter = {}

# Read the dataset
with open(data_file, "r") as f:
    for line in f:
        if len(line.strip().split(",")) != 4:
            continue  # Skip this line and move to the next one
        flow_id, date, time, count = line.strip().split(",")

        # Convert the date and time to the new format "yy/mm/dd hh:mm:ss"
        month, day, year = date.split("/")
        new_date = f"{year}/{month}/{day}"
        new_time = f"{new_date} {time}"

        data_queue.put((flow_id, new_time, int(count)))

# Calculate total count and count change and save the results to a CSV file
previous_date = ""
previous_total_count = 0
with open("crowd_change.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Time", "Current Total Count", "Count Change"])

    while not data_queue.empty():
        flow_id, new_time, count = data_queue.get()
        date, time = new_time.split(" ")[0], new_time.split(" ")[1]

        # Check if a new day has started, reset counters if needed
        if date != previous_date:
            previous_date = date
            previous_total_count = 0
            counter.clear()

        # Update the counter
        if flow_id == "7":
            counter[date] = counter.get(date, 0) - count
        elif flow_id == "9":
            counter[date] = counter.get(date, 0) + count

        # Calculate the current total count
        current_total_count = sum(counter.values())
        # Calculate count change
        count_change = current_total_count - previous_total_count
        previous_total_count = current_total_count

        # Write the results to the CSV file
        csv_writer.writerow([new_time, current_total_count, count_change])

        # Print the results (optional, uncomment the next line if you want to see the output on the console)
        # print(f"Time: {new_time}, Current Total Count: {current_total_count}, Count Change: {count_change}")

print("Output saved to crowd_change.csv.")
