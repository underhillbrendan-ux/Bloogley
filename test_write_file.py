from functions.write_file import write_file


def main() -> None:
    # Test 1: Overwrite existing file
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    # Test 2: Write to a file inside a subdirectory (creating parent dir if needed)
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    # Test 3: Attempt writing outside permitted directory
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    main()