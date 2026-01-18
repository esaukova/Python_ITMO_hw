num_test_cases = int(input())
for i in range(num_test_cases):
    num_digits = int(input())
    digits = list(map(int, input().split()))

    max_value = 0
    for digit_idx in range(num_digits):
        modified_digits = digits.copy()
        modified_digits[digit_idx] += 1
        current_value = 1
        for digit in modified_digits:
            current_value *= digit
        max_value = max(max_value, current_value)

    print(max_value)