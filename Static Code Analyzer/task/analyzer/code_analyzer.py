import logging
import pathlib
import sys
import time
from dataclasses import dataclass
import checks


# @dataclass
# class CheckResult:
#     def __init__(self, code=None, subject=None):
#         self.success = True
#         self.code = code
#         self.subject = subject


class Rule:
    def __init__(self, code, criteria):
        self.code = code
        self.criteria = criteria

    def check(self, line: str) -> bool:
        return self.criteria(line)


@dataclass
class Issue():
    issue_names = {
        'S001': 'Too long',
        'S002': 'Indentation is not a multiple of four',
        'S003': 'Unnecessary semicolon after a statement',
        'S004': 'Less than two spaces before inline comments',
        'S005': 'TO_DO found',
        'S006': 'More than two blank lines preceding a code line',
        'S007': 'Too many spaces after construction_name (def or class)',
        'S008': 'Class name class_name should be written in CamelCase',
        'S009': 'Function name function_name should be written in snake_case',
        'S010': 'Argument name arg_name should be written in snake_case',
        'S011': 'Variable var_name should be written in snake_case',
        'S012': 'The default argument value is mutable',
    }

    line: int
    issue_code: str
    issue_name: str
    code_line: str
    file_path: pathlib.Path

    def __init__(self, line, issue_code, file_path):
        self.line = line
        self.issue_code = issue_code
        self.issue_name = Issue.issue_names[issue_code]
        self.file_path = file_path

    def __repr__(self):
        return f"{self.file_path}: Line {self.line}: {self.issue_code} {self.issue_name}"


def process(file_path, rules):
    logging.debug(file_path)
    issues = []
    with open(file_path, 'r') as code:
        for i, line in enumerate(code):
            logging.debug(f"Line {i+1}: \"{line.expandtabs(4).rstrip()}\"")
            for rule in rules:
                if rule.check(line):
                    logging.debug("^^^ Faulty ^^^\n")
                    issues.append(Issue(i + 1, rule.code, file_path))

    return issues


if __name__ == '__main__':
    logging_path = 'C:\\Users\\schv\\Documents\\samples\\debug.log'
    open(logging_path, 'w').close()

    logging.basicConfig(filename=logging_path, level=logging.DEBUG)
    logging.debug("Starting execution")
    if not len(sys.argv) > 1 and not sys.argv[1]:
        raise ValueError("Directory path was not specified")

    path = pathlib.Path(sys.argv[1])

    issues = []
    rules = [
        Rule("S001", checks.long_line),
        Rule("S002", checks.bad_indent),
        Rule("S003", checks.eol_semicolon),
        Rule("S004", checks.no_spaces_before_inline_comment),
        Rule("S005", checks.todo_found),
        Rule("S006", checks.too_many_blank_lines),
        Rule("S007", checks.too_many_spaces_after_construction_name),
        Rule("S008", checks.class_naming_incorrect),
        Rule("S009", checks.func_naming_incorrect),
        Rule("S010", checks.arg_name_incorrect),
        Rule("S011", checks.var_name_incorrect),
        Rule("S012", checks.default_argument_mutable),
    ]

    logging.debug(path)
    if path.is_dir():
        for file_path in sorted(path.glob("**/*.py")):
            issues += process(file_path, rules)
    else:
        issues += process(path, rules)

    if issues:
        print(*issues, sep='\n')
        logging.debug(*issues)
