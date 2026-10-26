# DSA — Pancake Sort

A focused Python implementation of **Pancake Sort** that **sorts an array using only prefix flips** (reversing the first `k` elements) and **prints the array after every flip**. Clean, minimal, and correct — this program is the entry point to understanding the **pancake flipping pattern**, the idea that **two flips can place one element in its final position**, and the important distinction between **sorting with arbitrary swaps** and **sorting with a restricted operation**. The same "find the maximum, bring it to the front, flip it into place" idea shows up whenever an operation is limited to the start of a sequence.

---

## Problem Statement

Given an array of `n` integers entered by the user, **sort it in ascending order** using only **pancake flips**. A flip of size `k` reverses the **first `k` elements** of the array and leaves the rest untouched. Print the array after every flip, then print the final sorted array.

**Example Input:**

```
Enter numbers separated by spaces: 3 6 1 9 4
```

**Example Output:**

```
--- Starting Pancake Sort ---
Original array: [3, 6, 1, 9, 4]
------------------------------
Flip #1: [9, 1, 6, 3, 4]
Flip #2: [4, 3, 6, 1, 9]
Flip #3: [6, 3, 4, 1, 9]
Flip #4: [1, 4, 3, 6, 9]
Flip #5: [4, 1, 3, 6, 9]
Flip #6: [3, 1, 4, 6, 9]
Flip #7: [1, 3, 4, 6, 9]
------------------------------
Final Sorted array: [1, 3, 4, 6, 9]
```

---

## The Code

```python
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
```

---

## The Critical Distinction — Two Flips Place One Element

This is the most important thing to understand about this program.

The only operation allowed is a **prefix flip**: you can reverse the first `k` elements, never an arbitrary pair. That rules out ordinary swapping, so the program uses a **two-flip trick** to put the largest unsorted element into its final position:

1. **Flip 1** reverses the prefix that ends at the maximum, so the maximum moves to the **front**.
2. **Flip 2** reverses the whole unsorted prefix, so the maximum moves from the front to the **end** of the unsorted part.

```
curr_size = 5          unsorted part = the whole array

Start:          [3, 6, 1, 9, 4]       max = 9, at index 3
Flip first 4:   [9, 1, 6, 3, 4]       9 is now at the front
Flip first 5:   [4, 3, 6, 1, 9]       9 is now at the end, in its final place
                                ↑
                          sorted part
```

The sorted part grows from the **right**, and the unsorted prefix shrinks by one each round: `5 → 4 → 3 → 2`. The array is sorted when only one element is left unsorted.

| Approach                     | Allowed move              | Moves per placed element | Total moves (worst case) |
| ---------------------------- | ------------------------- | ------------------------ | ------------------------ |
| Selection sort               | Swap **any** two elements | 1 swap                   | `n - 1` swaps            |
| **Pancake sort (this code)** | Reverse a **prefix** only | up to 2 flips            | at most `2(n - 1)` flips |

Both are O(n²) overall. Pancake sort accepts about twice as many moves because each move is far less powerful.

---

## How the Loops Work

```python
for curr_size in range(n, 1, -1):
    max_idx = 0
    for i in range(1, curr_size):
        if arr[i] > arr[max_idx]:
            max_idx = i
```

- **Outer loop:** `curr_size` runs `n, n-1, …, 2` — the length of the still-unsorted prefix
- **Find the max:** `max_idx` starts at `0`, and the inner loop scans `1 … curr_size-1`; the strict `>` keeps the **first** occurrence of the maximum

```python
    if max_idx == curr_size - 1:
        continue
```

- **Already in place:** if the maximum is already last in the unsorted part, no flips are needed

```python
    if max_idx > 0:
        # reverse arr[0 .. max_idx]          ← Flip 1: max goes to the front
        ...
    # reverse arr[0 .. curr_size - 1]        ← Flip 2: max goes to the end
```

- **Flip 1:** only when the maximum is **not already at the front** (`max_idx > 0`)
- **Flip 2:** always, to send the maximum to position `curr_size - 1`
- **Counting and printing:** `flip_count` increases after each flip, and the array is printed so every step is visible

Each flip is done in place with the **two-pointer swap**: `start` moves right, `end` moves left, swapping until they meet.

> **Off-by-one note:** The outer loop is `range(n, 1, -1)`, which stops at `2`, because a prefix of size `1` is trivially sorted and needs no work. The first flip reverses `arr[0 .. max_idx]`, which has `max_idx + 1` elements, and the second reverses `arr[0 .. curr_size - 1]`, which has `curr_size` elements. Confusing an **index** with a **size** here is the most common bug.

> **Skipped flips:** when `max_idx == 0`, Flip 1 is skipped, because reversing a one-element prefix changes nothing. That is why a reverse-sorted array such as `[3, 2, 1]` needs only **1** flip, not 2.

---

## Algorithm (Pseudocode)

```
read the array arr
n = length of arr

for curr_size from n down to 2:
    max_idx = index of the largest element in arr[0 .. curr_size-1]

    if max_idx == curr_size - 1:
        continue                          (already in place)

    if max_idx > 0:
        flip(arr, max_idx + 1)            (bring the max to the front)
    flip(arr, curr_size)                  (send the max to the end)

print arr
```

Here `flip(arr, k)` reverses the first `k` elements.

---

## Dry Run

**Input:** `arr = [3, 6, 1, 9, 4]`, `n = 5`

| `curr_size` | Unsorted part     | `max_idx` (value) | Flip 1 (size `max_idx+1`)    | Flip 2 (size `curr_size`)  | Array after the round |
| ----------- | ----------------- | ----------------- | ---------------------------- | -------------------------- | --------------------- |
| 5           | `[3, 6, 1, 9, 4]` | 3 (`9`)           | size 4 → `[9, 1, 6, 3, 4]`   | size 5 → `[4, 3, 6, 1, 9]` | `[4, 3, 6, 1, 9]`     |
| 4           | `[4, 3, 6, 1]`    | 2 (`6`)           | size 3 → `[6, 3, 4, 1, 9]`   | size 4 → `[1, 4, 3, 6, 9]` | `[1, 4, 3, 6, 9]`     |
| 3           | `[1, 4, 3]`       | 1 (`4`)           | size 2 → `[4, 1, 3, 6, 9]`   | size 3 → `[3, 1, 4, 6, 9]` | `[3, 1, 4, 6, 9]`     |
| 2           | `[3, 1]`          | 0 (`3`)           | **skipped** (`max_idx == 0`) | size 2 → `[1, 3, 4, 6, 9]` | `[1, 3, 4, 6, 9]`     |

**Total flips:** 7 (2 + 2 + 2 + 1)

**Output:** `Final Sorted array: [1, 3, 4, 6, 9]` ✅

---

## Visual Walkthrough — Watch the Pancakes Flip

Every line the program prints has a matching picture of the stack. Each picture shows the stack **after** that flip, for the input `3 6 1 9 4`. Everything is drawn with plain text, so it works anywhere this README is shown, with no extra image files.

**How to read the pictures:**

| What you see                   | Meaning                                                       |
| ------------------------------ | ------------------------------------------------------------- |
| First row                      | The **top** of the stack — `arr[0]`                           |
| Last row, above the `━━━` line | The **bottom** of the stack — `arr[-1]`, sitting on the plate |
| Width of a pancake `(▒▒ 6 ▒▒)` | Its value — wider means larger                                |
| `┌ │ └` bracket on the left    | The prefix that was **just flipped**                          |
| `✓` on the right               | The pancake is already in its **final place**                 |

**Start** — `Original array: [3, 6, 1, 9, 4]`

```
        (▒▒▒ 3 ▒▒▒)
     (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)
          (▒ 1 ▒)
  (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒)
       (▒▒▒▒ 4 ▒▒▒▒)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Flip #1** — `Flip #1: [9, 1, 6, 3, 4]`

Flip the top 4 pancakes so the biggest unsorted one (9) jumps to the top.

```
┌ (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒)
│         (▒ 1 ▒)
│    (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)
└       (▒▒▒ 3 ▒▒▒)
       (▒▒▒▒ 4 ▒▒▒▒)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Flip #2** — `Flip #2: [4, 3, 6, 1, 9]`

Flip the top 5 pancakes so 9 sinks into its final place.

```
┌      (▒▒▒▒ 4 ▒▒▒▒)
│       (▒▒▒ 3 ▒▒▒)
│    (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)
│         (▒ 1 ▒)
└ (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒) ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Flip #3** — `Flip #3: [6, 3, 4, 1, 9]`

Flip the top 3 pancakes so the biggest unsorted one (6) jumps to the top.

```
┌    (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)
│       (▒▒▒ 3 ▒▒▒)
└      (▒▒▒▒ 4 ▒▒▒▒)
          (▒ 1 ▒)
  (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒) ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Flip #4** — `Flip #4: [1, 4, 3, 6, 9]`

Flip the top 4 pancakes so 6 sinks into its final place.

```
┌         (▒ 1 ▒)
│      (▒▒▒▒ 4 ▒▒▒▒)
│       (▒▒▒ 3 ▒▒▒)
└    (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)    ✓
  (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒) ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Flip #5** — `Flip #5: [4, 1, 3, 6, 9]`

Flip the top 2 pancakes so the biggest unsorted one (4) jumps to the top.

```
┌      (▒▒▒▒ 4 ▒▒▒▒)
└         (▒ 1 ▒)
        (▒▒▒ 3 ▒▒▒)
     (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)    ✓
  (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒) ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Flip #6** — `Flip #6: [3, 1, 4, 6, 9]`

Flip the top 3 pancakes so 4 sinks into its final place.

```
┌       (▒▒▒ 3 ▒▒▒)
│         (▒ 1 ▒)
└      (▒▒▒▒ 4 ▒▒▒▒)      ✓
     (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)    ✓
  (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒) ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Flip #7** — `Flip #7: [1, 3, 4, 6, 9]`

3 is already on top, so a single flip of the top 2 pancakes sends it to its final place.

```
┌         (▒ 1 ▒)
└       (▒▒▒ 3 ▒▒▒)       ✓
       (▒▒▒▒ 4 ▒▒▒▒)      ✓
     (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)    ✓
  (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒) ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Finish** — `Final Sorted array: [1, 3, 4, 6, 9]`

Smallest on top, biggest on the bottom, done in 7 flips.

```
          (▒ 1 ▒)         ✓
        (▒▒▒ 3 ▒▒▒)       ✓
       (▒▒▒▒ 4 ▒▒▒▒)      ✓
     (▒▒▒▒▒▒ 6 ▒▒▒▒▒▒)    ✓
  (▒▒▒▒▒▒▒▒▒ 9 ▒▒▒▒▒▒▒▒▒) ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Complexity Analysis

| Metric | Complexity                                                                                                                           |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| Time   | **O(n²)** — finding each maximum costs O(`curr_size`), and each flip also costs O(`curr_size`); summed over all rounds this is O(n²) |
| Space  | **O(1)** — extra variables only; the array is sorted **in place**                                                                    |
| Flips  | **at most `2(n − 1)`** — two flips per round, over `n − 1` rounds                                                                    |

The time is O(n²) **even for an already sorted array**, because the maximum is still searched for in every round. In that case, though, **no flips** happen at all.

---

## Edge Cases

| Scenario                               | Behavior                                                          |
| -------------------------------------- | ----------------------------------------------------------------- |
| Empty input                            | `n = 0`, so the loop is skipped — prints `[]` ✅                  |
| Single element `[5]`                   | `range(1, 1, -1)` is empty — no flips ✅                          |
| Two elements `[2, 1]`                  | `max_idx = 0`, skip Flip 1, then one flip of size 2 — `[1, 2]` ✅ |
| Already sorted `[1, 2, 3]`             | Maximum always already last — **0 flips** ✅                      |
| Reverse sorted `[3, 2, 1]`             | One flip of size 3 gives `[1, 2, 3]` — **1 flip** ✅              |
| Duplicates `[3, 3, 1]`                 | Strict `>` picks the first `3`; one flip gives `[1, 3, 3]` ✅     |
| Negative numbers `[-1, -5, -3]`        | Comparisons work normally — sorted in 2 flips ✅                  |
| Extra spaces between numbers           | `split()` ignores them ✅                                         |
| Commas or letters in the input `1,2,3` | `int()` raises a `ValueError` ⚠️                                  |
| Very large `n`                         | O(n²) work, plus one printed line per flip — slow and noisy ⚠️    |

---

## Code-Quality Notes

**The same reversal loop is written twice.** Both flips use an identical two-pointer block. Moving it into a small function removes the duplication and makes the main loop read like the algorithm:

```python
def flip(arr, k):
    """Reverse the first k elements of arr, in place."""
    start, end = 0, k - 1
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1
```

With it, the two flips become `flip(arr, max_idx + 1)` and `flip(arr, curr_size)`.

**Input and output are mixed into the algorithm.** The sorting logic, the `input()` call, and the `print` calls all live at the top level. That is perfect for demonstrating each flip, but a reusable version would put the sort in a function and return the result.

**There is no input validation.** Any token that is not an integer stops the program with a `ValueError`.

**This is a demonstration, not a fast sort.** For ordinary sorting, Python's built-in `sorted()` is far faster. Pancake sort matters when **prefix reversal is the only operation available**.

---

## The Natural Extension — Return the Flip Sequence

Many versions of this problem do not ask for the printed arrays, but for the **sequence of flip sizes** that sorts the array. This returns them from a reusable function:

```python
def pancake_sort(arr):
    flips = []
    for size in range(len(arr), 1, -1):
        max_idx = arr.index(max(arr[:size]))
        if max_idx == size - 1:
            continue
        if max_idx > 0:
            arr[:max_idx + 1] = arr[:max_idx + 1][::-1]
            flips.append(max_idx + 1)
        arr[:size] = arr[:size][::-1]
        flips.append(size)
    return flips
```

**Trace for `[3, 6, 1, 9, 4]`:**

| `size` | `max_idx` | Flips recorded | Array afterwards  |
| ------ | --------- | -------------- | ----------------- |
| 5      | 3         | `4`, `5`       | `[4, 3, 6, 1, 9]` |
| 4      | 2         | `3`, `4`       | `[1, 4, 3, 6, 9]` |
| 3      | 1         | `2`, `3`       | `[3, 1, 4, 6, 9]` |
| 2      | 0         | `2`            | `[1, 3, 4, 6, 9]` |

**Result:** `flips = [4, 5, 3, 4, 2, 3, 2]` and the array is sorted ✅ — the same 7 flips as the printed version.

| Property                       | Printing version (this code) | Function that returns the flips           |
| ------------------------------ | ---------------------------- | ----------------------------------------- |
| Shows every intermediate array | ✅ Yes                       | ❌ No (only the sizes)                    |
| Reusable from other code       | ❌ No                        | ✅ Yes                                    |
| Easy to test                   | ❌ No                        | ✅ Yes                                    |
| Time                           | O(n²)                        | O(n²)                                     |
| Extra space                    | O(1)                         | O(n) for the list of flips                |
| When to use                    | Learning and visualizing     | Tests, other programs, interview problems |

---

## Repository Structure

```
DSA-Pancake-Sort/
│
├── pancake_sort.py      # Main Python implementation
└── README.md            # Project documentation (all pictures are inside it)
```

---

## How to Compile and Run

**Prerequisites:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/rishita-ops/DSA-Pancake-Sort.git
cd DSA-Pancake-Sort

# Run
python3 pancake_sort.py
```

**On Windows:**

```bash
python pancake_sort.py
```

**Sample session:**

```
Enter numbers separated by spaces: 3 6 1 9 4

--- Starting Pancake Sort ---
Original array: [3, 6, 1, 9, 4]
------------------------------
Flip #1: [9, 1, 6, 3, 4]
Flip #2: [4, 3, 6, 1, 9]
Flip #3: [6, 3, 4, 1, 9]
Flip #4: [1, 4, 3, 6, 9]
Flip #5: [4, 1, 3, 6, 9]
Flip #6: [3, 1, 4, 6, 9]
Flip #7: [1, 3, 4, 6, 9]
------------------------------
Final Sorted array: [1, 3, 4, 6, 9]
```

---

## Key Concepts Covered

- **Pancake flip** — reversing the first `k` elements of an array
- **Restricted operations** — sorting when ordinary swaps are not allowed
- **Two-flip placement** — one flip brings the maximum to the front, the second sends it to its final position
- **Shrinking unsorted prefix** — `curr_size` goes from `n` down to `2`, and the sorted suffix grows
- **Finding the maximum** — a linear scan, keeping the first occurrence with strict `>`
- **Skipped flips** — no flip when the maximum is already in place or already at the front
- **Two-pointer in-place reversal** — the swap loop used for each flip
- **O(n²) time, O(1) space, at most `2(n − 1)` flips**
- **Helper function** — extracting `flip(arr, k)` to remove duplicated code
- **Visualization** — redrawing the stack after every flip to see the algorithm work

---

## Why This Problem Matters in DSA

The prefix-reversal idea and the "place one element at a time" pattern appear across a broad family of problems:

| Problem / Concept                                             | Connection                                                                  |
| ------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Pancake Sorting** (LeetCode #969)                           | The same algorithm, returning the list of flip sizes                        |
| **Reverse String** (LeetCode #344)                            | The two-pointer in-place reversal used inside every flip                    |
| **Rotate Array** (LeetCode #189)                              | Achieves a rotation using three reversals                                   |
| **Reverse Linked List II** (LeetCode #92)                     | Reversing a segment of a linked list, the pointer version of a flip         |
| **Minimum Number of K Consecutive Bit Flips** (LeetCode #995) | Another problem built around a fixed flipping operation                     |
| **Sort an Array** (LeetCode #912)                             | General sorting, where pancake sort is a teaching example, not a competitor |

Every problem that limits you to a small set of operations and asks you to reach a target arrangement traces back to the construct-with-restricted-moves idea introduced here.

---

## Contributing

Contributions are welcome. Consider adding:

- A version that uses a **`flip(arr, k)` helper function**
- The **`pancake_sort` function** that returns the list of flip sizes
- A version that **counts flips without printing** each array
- A **burnt pancake** variant, where each pancake also has a burnt side
- **Picture versions** of each flip (for example drawn with matplotlib) to go with the text stacks
- A script that **prints the text stack** after every flip while the program runs
- Input validation for non-integer input
- Implementations in C++, Java, or JavaScript

```bash
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
# Then open a Pull Request
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

_Part of a structured DSA practice series — fundamentals, done right._
