from functions.run_python_file import run_python_file


def main() -> None:
    # Test 1: Main execution without arguments
    print("--- Test 1: main.py ---")
    print(run_python_file("calculator", "main.py"))

    # Test 2: Main execution with calculator expression argument
    print("\n--- Test 2: main.py '3 + 5' ---")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    # Test 3: Running unit tests file
    print("\n--- Test 3: tests.py ---")
    print(run_python_file("calculator", "tests.py"))

    # Test 4: Path traversal attempt outside working directory
    print("\n--- Test 4: ../main.py ---")
    print(run_python_file("calculator", "../main.py"))

    # Test 5: Non-existent file
    print("\n--- Test 5: nonexistent.py ---")
    print(run_python_file("calculator", "nonexistent.py"))

    # Test 6: Non-python file execution
    print("\n--- Test 6: lorem.txt ---")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()