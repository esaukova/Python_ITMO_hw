num_test_cases = int(input())
for test_case in range(num_test_cases):
    number_length, digit_to_insert  = list(map(int, input().split()))
    original_number = input().strip()
    
    result_number = ""
    digit_inserted = False
    
    for char in original_number:
        current_digit = int(char)
        if not digit_inserted and current_digit < digit_to_insert:
            result_number += str(digit_to_insert)
            digit_inserted = True
        result_number += char
    
    if not digit_inserted:
        result_number += str(digit_to_insert)
    
    print(result_number)
