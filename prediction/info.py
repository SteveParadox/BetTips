def write_to_txt(data, filename):
    try:
        with open(filename, 'w') as file:
            for item in data:
                file.write(f"{item}\n")
        print(f"Data written to {filename} successfully.")
    except Exception as e:
        print(f"Error writing to {filename}: {e}")

