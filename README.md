# Exact-Cover-SAT
Encodes, solves, and decodes he exact cover problem via reduction to SAT.

# Documentation

## Problem description

*"Given a collection* $S$ *of subsets of a set* $X$ *, an exact cover is a subcollection* $S^∗$ *of* $S$ *such that each element in* $X$ *is contained in exactly one subset in* $S^∗$ *.
It is a non-deterministic polynomial time (NP) complete problem and has a variety of applications, ranging from the optimization of airline flight schedules, cloud computing, and electronic circuit design."* \
[Source](https://en.wikipedia.org/wiki/Exact_cover).

Example of a valid input file format:
```
{1 2 3 4}
{
    { }
    {1 3}
    {1 2 3}
    {2 4}
}
```

**Input format**:
* First line only contains the main set: $X$.
* Following lines only contain the set of subsets of the main set: $S$.
* Both subsets of literals and the set of subsets $S$ need to be contained in `{ }`.
* Lines can contain multiple subsets.
* Literals need to be delimited by (one or more) spaces.
* Literals can be strings of various length but without whitespace.

This input file format is also valid:
```
{alpha bravo charlie delta}
{ { } {alpha charlie} {alpha bravo charlie} {bravo delta} }
```

*Any deviation from the problem's specifications (e.g., subset contains an element that is not present in the main set) should trigger an exception during parsing.*

## Encoding

The problem is encoded using one set of variables. Variable $s_i$ represents that subset $S_i$ is included in the exact cover $S^*$.   
Analogically, variable $\neg s_i$ means the subset is not included in $S^*$.

The conditions for a collection of subsets to be an exact cover of the main set $X$ can be written as the following constraints:

- Every element of the main set $X$ has to be included in at least one subset in $S^*$.

```math
\bigwedge_{e \in X} \left( \bigvee_{\substack{ S_i \in S \\ e \in S_i}}  (s_i) \right)
```

- Every element of the main set $X$ can be included in at most one subset in $S^*$.

```math
     \bigwedge_{e \in X}
    \left(
        \bigwedge_{\substack{S_i, S_j \in S\\ S_i \neq S_j}} 
        \left(\neg s_i \lor \neg s_j \right) 
    \right)
```

## User documentation


Basic usage: 
```
main.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The instance file. Default: "input.in".
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS cnf formula. Default: "output.cnf".
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used. Default "glucose-syrup" *
*  `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.

\* *If the provided path cannot be found, the script assumes this to be a global command.* 

## Example instances
* `input-easy-sat.in`: Simple satisfiable instance provided in the [Exact cover wikipedia page](https://en.wikipedia.org/wiki/Exact_cover) where $|X| = 4$, $|S| = 4$.
* `input-easy-unsat.in`: Simple unsatisfiable instance where $|X| = 5$, $|S| = 5$. 
* `input-hard-sat.in`: Complex satisfiable instance generated using [instance_generator.py](instance_generator.py) where $|X| = 100$, $|S| = 560$. 
* `input-hard-unsat.in`: Complex unsatisfiable instance generated using [instance_generator.py](instance_generator.py) where $|X| = 100$, $|S| = 500$.

## Experiments

Experiments were run on Intel Core i7-7500U CPU (2.70GHz) and 12 GB RAM on Fedora Linux 40. \
$\dots$
