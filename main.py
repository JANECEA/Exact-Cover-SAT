#!/usr/bin/env python
import os
import subprocess
from argparse import ArgumentParser


class CnfParser:
    element_occurrences: list[list[int]]
    subset_count: int
    cnf: list[list[int]]

    def __init__(self, element_occurences: list[list[int]], subset_count: int) -> None:
        self.element_occurrences = element_occurences
        self.subset_count = subset_count

    def encode_to_cnf(self) -> None:
        self.cnf = list()

        # Every element needs to be present in at least one out of the chosen subsets
        for occurrences in self.element_occurrences:
            self.cnf.append([subset_index + 1 for subset_index in occurrences])

        # Every element needs to be present in at most one out of the chosen subsets
        for occurrences in self.element_occurrences:
            for i in range(len(occurrences)):
                for j in range(i + 1, len(occurrences)):
                    self.cnf.append([-occurrences[i] - 1, -occurrences[j] - 1])

    def write_to_file(self, output_path: str):
        with open(output_path, "w") as output_file:
            output_file.write(f"p cnf {str(self.subset_count)} {str(len(self.cnf))}\n")
            for clause in self.cnf:
                output_file.write(" ".join(str(literal) for literal in clause) + " 0\n")

    def call_solver(self, solver_path: str, output_path: str, verbosity: int):
        if not os.path.isfile(output_path):
            raise Exception(f"File {output_path} has not been found")

        solver_name: str = solver_path

        if os.path.isfile(solver_path):
            solver_name = "./" + solver_name

        return subprocess.run(
            [solver_name, "-model", "-verb=" + str(verbosity), output_path],
            stdout=subprocess.PIPE,
        )


class InstanceParser:
    path_to_file: str
    main_set: list[str]
    element_occurrences: list[list[int]]
    subsets: list[set[int]]
    __main_set_dict: dict[str, int]

    def __init__(self, path_to_file: str) -> None:
        self.path_to_file = path_to_file

    def load_instance(self) -> None:
        with open(self.path_to_file) as input_file:
            main_set_str: str = input_file.readline()
            subsets_str: str = input_file.read()

        self.__set_main_set(main_set_str)
        self.element_occurrences = [[] for _ in range(len(self.main_set))]
        self.__set_subsets(subsets_str)

    def __set_main_set(self, main_set_str: str) -> None:
        main_set_str = main_set_str.strip()
        if main_set_str[0] != "{" or main_set_str[-1] != "}":
            raise Exception("Invalid input file format")
        main_set_str = main_set_str.strip("{}")

        self.main_set = main_set_str.split()
        self.__main_set_dict = {}
        for index, element in enumerate(self.main_set):
            if element not in self.__main_set_dict:
                self.__main_set_dict[element] = index
            else:
                raise Exception(f"Element {element} is repeated in the main set.")

    def __set_subsets(self, subsets_str: str) -> None:
        subsets_str = subsets_str.strip()
        if subsets_str[0] != "{" or subsets_str[-1] != "}":
            raise Exception("Invalid input file format")
        subsets_str = subsets_str.strip("{}")

        self.subsets = []
        set_start_index = -1
        for index, char in enumerate(subsets_str):
            if char == "{":
                if set_start_index == -1:
                    set_start_index = index
                else:
                    raise Exception("Invalid input file format")

            if char == "}":
                if set_start_index != -1:
                    subset_str: str = subsets_str[set_start_index + 1 : index]
                    self.subsets.append(
                        self.__parse_subset(subset_str, len(self.subsets))
                    )
                    set_start_index = -1
                else:
                    raise Exception("Invalid input file format")

        if set_start_index != -1:
            raise Exception("Invalid input file format")

    def __parse_subset(self, subset_str: str, subset_index: int) -> set[int]:
        subset_str = subset_str.strip()
        subset: set[int] = set()

        if subset_str == "":
            return subset

        for element in subset_str.split():
            if element not in subset:
                if element in self.__main_set_dict:
                    subset.add(self.__main_set_dict[element])
                    self.element_occurrences[self.__main_set_dict[element]].append(
                        subset_index
                    )
                else:
                    raise Exception(
                        f"Element {element} has not been found in the main set"
                    )
            else:
                raise Exception(
                    f'Element {element} is repeated in the "{{{subset_str}}}" set.'
                )

        return subset


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help=("The instance file."),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.cnf",
        type=str,
        help=("Output file for the DIMACS format (i.e. the CNF formula)."),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help=("The SAT solver to be used."),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0, 2),
        help=("Verbosity of the SAT solver used."),
    )
    args = parser.parse_args()

    instance_parser: InstanceParser = InstanceParser(args.input)
    instance_parser.load_instance()
    cnf_parser: CnfParser = CnfParser(
        instance_parser.element_occurrences,
        len(instance_parser.subsets),
    )
    cnf_parser.encode_to_cnf()
    cnf_parser.write_to_file(args.output)
    cnf_parser.call_solver(args.solver, args.output, args.verb)


if __name__ == "__main__":
    main()
