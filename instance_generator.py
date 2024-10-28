import random

MAIN_SET_SIZE = 5
SUBSET_COUNT_MULT = 1
GUARANTEED_SAT = False
OUTPUT_FILE_NAME = "input.in"


# Write the main set
output_file = open(OUTPUT_FILE_NAME, "w")
output_file.write("{ ")
for i in range(1, MAIN_SET_SIZE + 1):
    output_file.write(str(i) + " ")
output_file.write("}\n")


# Generate random subsets
main_set: list[int] = [i for i in range(MAIN_SET_SIZE)]
subsets: list[list[int]] = [[] for _ in range(SUBSET_COUNT_MULT * MAIN_SET_SIZE)]
for i in range(SUBSET_COUNT_MULT * MAIN_SET_SIZE):
    set_copy = main_set.copy()
    random.shuffle(set_copy)
    subsets[i] = set_copy[: random.randint(1, MAIN_SET_SIZE - 1)]
    subsets[i].sort()


# Add subsets guaranteed to solve the problem
if GUARANTEED_SAT:
    distribution: list[int] = [
        random.randint(0, MAIN_SET_SIZE - 1) for _ in range(MAIN_SET_SIZE)
    ]
    target_subsets: list[list[int]] = [[] for _ in range(MAIN_SET_SIZE)]
    for element, subset_index in enumerate(distribution):
        target_subsets[subset_index].append(element)
    target_subsets = [set for set in target_subsets if len(set) != 0]

    for target_subset in target_subsets:
        subsets.insert(random.randint(0, len(subsets)), target_subset)


# Output subsets to file and close
output_file.write("{\n")
for subset in subsets:
    output_file.write(
        f"    {{ {' '.join(str(element_index + 1) for element_index in subset)} }}\n"
    )
output_file.write("}\n")
output_file.close()
