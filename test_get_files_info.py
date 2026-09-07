from functions.get_files_info import get_files_info


def main() -> None:
    print("--- Directory Contents (.): ---")
    print(get_files_info("calculator", "."))

    print("\n--- Directory Contents (pkg): ---")
    print(get_files_info("calculator", "pkg"))

    print("\n--- Directory Contents (/bin): ---")
    print(get_files_info("calculator", "/bin"))

    print("\n--- Directory Contents (does_not_exist): ---")
    print(get_files_info("calculator", "does_not_exist"))


if __name__ == "__main__":
    main()