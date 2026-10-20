# UEdge

UEdge is a small programming-language project for the CIIC-4030 course. The
project is following the **Memory-Aware (Memory) track**: functions can be
annotated with memory budgets, with the goal of checking whether their memory
usage stays within those budgets.

## Current implementation

The current implementation in `src/main.py` is a lexer and parser built with
[PLY](https://www.dabeaz.com/ply/). It parses a `.uedge` source file and reports
whether parsing succeeded. It currently recognizes:

- Variable declarations and assignments (`let` and `=`)
- Function declarations, parameters, calls, and return statements
- `if`/`else`, `while`, and `for` statements
- Integer, floating-point, string, and Boolean literals
- Arithmetic and comparison operators
- `print(...)` expressions and `//` comments
- Memory annotations on functions, such as `@memory(40kb)`

**This version does not execute programs or calculate or enforce memory
budgets.** The memory-track examples document the intended budget-checking
behavior; at present, running them only parses their syntax.

## Requirements

- Python
- PLY

Install PLY if it is not already available:

```powershell
python -m pip install ply
```

## Run the parser

From the project root, pass a `.uedge` file to the parser:

```powershell
python src\main.py tests\working_examples\core\01_hello.uedge
```

For a valid file, the parser prints:

```text
Parsed successfully
```

You can also parse either memory-track example:

```powershell
python src\main.py tests\working_examples\memory_track\01_within_budget.uedge
python src\main.py tests\working_examples\memory_track\02_over_budget.uedge
```

Both commands currently report parse success; neither evaluates the example's
memory usage.

## Project layout

```text
.
├── grammars/
│   ├── uedge grammar draft.txt
│   └── uedge grammar enhanced.txt
├── src/
│   └── main.py
└── tests/
    ├── counter_examples/
    └── working_examples/
        ├── core/
        └── memory_track/
```

- `grammars/` contains the language grammar drafts.
- `src/main.py` contains the lexer, parser, and command-line entry point.
- `tests/working_examples/` contains valid parser examples, including the
  memory-track cases.
- `tests/counter_examples/` contains malformed programs for parser error
  handling.

## Memory annotation syntax

Place `@memory` immediately before a function definition. The annotation takes
an integer amount followed by a unit:

```uedge
@memory(40kb)
func readSensorBuffer() {
    let buffer = array(int, 1000);
    print("done");
}
```

The parser recognizes `kb`, `Mb`, `Gb`, `Tb`, `Pb`, `Eb`, `Zb`, and `Yb`.
Choosing and applying a cost model, measuring allocations, and reporting
budget violations are not implemented yet.
