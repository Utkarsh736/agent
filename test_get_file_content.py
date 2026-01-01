from functions.get_file_content import get_file_content

def test():
    print("get_file_content('calculator', 'lorem.txt'):")
    content = get_file_content("calculator", "lorem.txt")
    print(f"Length: {len(content)}")  # Should be ~10000 + truncation msg
    print(content[-100:])  # Last 100 chars (shows truncation)
    print()
    
    print("get_file_content('calculator', 'main.py'):")
    print(get_file_content("calculator", "main.py"))
    print()
    
    print("get_file_content('calculator', 'pkg/calculator.py'):")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()
    
    print("get_file_content('calculator', '/bin/cat'):")
    print(get_file_content("calculator", "/bin/cat"))
    print()
    
    print("get_file_content('calculator', 'pkg/does_not_exist.py'):")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    test()

