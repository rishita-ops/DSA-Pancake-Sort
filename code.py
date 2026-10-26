user_input = input("Enter numbers separated by spaces: ")
arr = [int(x) for x in user_input.split()]

print("\n--- Starting Pancake Sort ---")
print("Original array:", arr)
print("------------------------------")

n = len(arr)
flip_count = 0

for curr_size in range(n, 1, -1):
    max_idx = 0
    for i in range(1, curr_size):
        if arr[i] > arr[max_idx]:
            max_idx = i
            
    if max_idx == curr_size - 1:
        continue
        
    if max_idx > 0:
        start = 0
        end = max_idx
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1
        flip_count += 1
        print(f"Flip #{flip_count}: {arr}")
            
    start = 0
    end = curr_size - 1
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1
    flip_count += 1
    print(f"Flip #{flip_count}: {arr}")

print("------------------------------")
print("Final Sorted array:", arr)
