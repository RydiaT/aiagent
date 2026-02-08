from config import MAX_CHARS
from functions.get_file_content import get_file_content

lorem = get_file_content("calculator", "../lorem.txt")

print(f"Lorem Length: {len(lorem)} - Valid Ending: {f"...File 'lorem.txt' truncated at {MAX_CHARS} characters]" == lorem.split("[")[1]}")

print(get_file_content("calculator", "../main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))