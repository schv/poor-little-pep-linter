import ast
import logging
import re
import string


def extract_comment_sanitized(line: str) -> (str, str, str):
    return line\
        .replace("'#'", "'rewetka'")\
        .replace('"#"', '"rewetka"')\
        .partition('#')


# S001
def long_line(line: str, limit: int = 79) -> bool:
    return len(line) > limit


# S002 : Indentation is not a multiple of four;
def bad_indent(line: str):
    spaces = 0
    for c in line.expandtabs(tabsize=4):
        if c == ' ':
            spaces += 1
        else:
            break
    return spaces % 4 != 0


# S003 : Unnecessary semicolon after a statement
# (note that semicolons are acceptable in comments);
def eol_semicolon(line: str) -> bool:
    prefix, sep, comment = extract_comment_sanitized(line)
    return prefix.strip().endswith(';')


# S004 : Less than two spaces before inline comments;
def no_spaces_before_inline_comment(line: str) -> bool:
    prefix, sep, comment = extract_comment_sanitized(line)
    return prefix and comment and not prefix.endswith('  ')


# S005 : TO_DO found (in comments only and case-insensitive);
def todo_found(line: str) -> bool:
    prefix, sep, comment = extract_comment_sanitized(line)
    return 'todo'.casefold() in comment.casefold()


# S006 : More than two blank lines preceding a code line
# (applies to the first non-empty line).
def too_many_blank_lines(line: str, state=[0]) -> bool:
    if line.isspace():
        state[0] += 1
        return False
    else:
        crit = state[0] > 2
        state[0] = 0
        return crit


# S007 : Too many spaces after construction_name (def or class)
def too_many_spaces_after_construction_name(line: str) -> bool:
    line = line.expandtabs(4).strip()
    if line.startswith('def '):
        return bool(re.match(r'def {2,}', line))
    if line.startswith('class '):
        return bool(re.match(r'class {2,}', line))

    return False


def is_camel_case(s: str) -> bool:
    vocab = string.ascii_letters + string.digits
    return s[0].isupper() and all(c in vocab for c in s)


# S008 : Class name class_name should be written in CamelCase
def class_naming_incorrect(line: str) -> bool:
    if (line := line.strip()).startswith('class'):
        line += " pass"
        tree = ast.parse(line)

        if tree and isinstance(tree.body[0], ast.ClassDef):
            return not is_camel_case(tree.body[0].name)

    return False


def is_snake_case(s: str) -> bool:
    vocab = string.ascii_lowercase + string.digits + '_'
    return all(c in vocab for c in s)


# S009 : Function name function_name should be written in snake_case
def func_naming_incorrect(line: str) -> bool:
    if (line := line.strip()).startswith('def '):
        line += " pass"
        tree = ast.parse(line)

        if tree and isinstance(tree.body[0], ast.FunctionDef):
            return not is_snake_case(tree.body[0].name)

    return False


def extract_args(f: ast.FunctionDef) -> list:
    arguments = []
    arguments.extend(f.args.args)
    arguments.extend(f.args.posonlyargs)
    if f.args.kwarg is not None:
        arguments.append(f.args.kwarg)
    if f.args.vararg is not None:
        arguments.append(f.args.vararg)
    #
    # print(arguments)
    #
    # for a in arguments:
    #     print(ast.dump(ast.arg(a)))

    return list(map(lambda x: x.arg, arguments))


# S010 : Argument name arg_name should be written in snake_case
def arg_name_incorrect(line: str) -> bool:
    if (line := line.strip()).startswith('def '):
        line += " pass"
        tree = ast.parse(line)

        if tree and isinstance(tree.body[0], ast.FunctionDef):
            arguments = extract_args(tree.body[0])

            for argname in arguments:
                if not is_snake_case(argname):
                    return True

    return False


# S011 : Variable var_name should be written in snake_case
def var_name_incorrect(line: str) -> bool:
    logging.debug(line)
    try:
        tree = ast.parse(line.strip())
        if tree and isinstance(tree.body[0], ast.Assign):
            for target in tree.body[0].targets:
                logging.debug(target)
                name = target.id
                if not is_snake_case(name):
                    return True

    except Exception as e:
        pass

    return False


# S012 : The default argument value is mutable
def default_argument_mutable(line: str) -> bool:
    if (line := line.strip()).startswith('def '):
        line += " pass"
        tree = ast.parse(line)

        if tree and isinstance(tree.body[0], ast.FunctionDef):
            default_args = tree.body[0].args.defaults
            for arg in default_args:
                if any(isinstance(arg, ds) for ds in (ast.List, ast.Dict)):
                    return True

    return  False
