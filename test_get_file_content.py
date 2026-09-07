
from functions.get_file_content import get_file_content

def test_file_reading():
    # Test 1: Truncation check on large file
    result_lorem = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result_lorem)}")
    print(f"lorem.txt truncated: {'truncated' in result_lorem}\n")

    # Test 2: Standard existing file
    result_main = get_file_content("calculator", "main.py")
    print("--- calculator/main.py ---")
    print(result_main, "\n")

    # Test 3: Subdirectory file
    result_pkg = get_file_content("calculator", "pkg/calculator.py")
    print("--- calculator/pkg/calculator.py ---")
    print(result_pkg, "\n")

    # Test 4: Outside directory restriction
    result_outside = get_file_content("calculator", "/bin/cat")
    print("--- Directory Security Check ---")
    print(result_outside, "\n")

    # Test 5: Missing file
    result_missing = get_file_content("calculator", "pkg/does_not_exist.py")
    print("--- Missing File Check ---")
    print(result_missing)

if __name__ == "__main__":
    test_file_reading()