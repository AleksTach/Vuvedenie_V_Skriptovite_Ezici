import os

def average_file_size(*file_names: str) -> None:
    total_size = 0
    count = 0

    for file_name in file_names:
        if not os.path.isfile(file_name):
            print(f"File not found: {file_name}")
            continue

        size = os.path.getsize(file_name)
        print(f"File: {file_name}, Size: {size} bytes")
        total_size += size
        count += 1

    if count == 0:
        print("No input files.")
        return

    print(f"Total size of files: {total_size} bytes")
    average_size = total_size / count
    print(f"Average file size: {average_size} bytes")


def main():
    file_names = []

    while True:
        print(f"Current file names: {file_names}")
        file_name = input("Enter file name or 'stop' to end: ")

        if file_name.lower() == 'stop':
            print("Ending input(...)")
            os.system('cls')
            break

        if os.path.isfile(file_name):
            file_names.append(file_name)
        else:
            print("Invalid file name. Please try again.")

        os.system('cls')

    if file_names:
        average_file_size(*file_names)
        print("\nProcess completed successfully.")
    else:
        print("\nNo files provided.")


if __name__ == '__main__':
    main()
