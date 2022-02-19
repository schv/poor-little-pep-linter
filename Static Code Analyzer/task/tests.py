from hstest.stage_test import *
from hstest.test_case import TestCase
import os, re

TOO_LONG_LINE = 'Too long line is not mentioned. '
error_code_long = "s001"

INDENTATION = "Invalid check of indentation. "
error_code_indention = "s002"

UNNECESSARY_SEMICOLON = "Your program passed the line with an unnecessary semicolon or has an incorrect format. "
error_code_semicolon = "s003"

TWO_SPACES_BEFORE_COMMENT = "The program should warn about the line with less than 2 spaces before a comment. "
error_code_comments = "s004"

TODO = "Your program passed the line with TODO comment or has an incorrect format. "
error_code_todo = "s005"

TOO_MANY_BLANK_LINES = "Your program didn't warn about more than two blank lines between lines. "
error_code_blank_lines = "s006"

error_code_class_def_spaces = "s007"
SPACES_AFTER_CLASS_FUNC = "Your program should warn about multiple spaces after keyword 'class' and 'def'. "

error_code_class_name = "s008"
CLASS_NAME = "The program should warn about incorrect class name. "

error_code_func_name = "s009"
FUNC_NAME = "The program passed the function with the name not in snake_case style. "

error_code_arg_name = "s010"
ARG_NAME = "Your program should warn about function argument written not in snake_case style. "

error_code_var_func_name = "s011"
VAR_FUNC_NAME = "The program omitted warning about incorrect variable name in the function's body. " \
                "It should be written in the snake_case style. "

error_code_default_argument_is_mutable = "s012"
MUTABLE_ARG = "The program didn't warn about mutable function argument. "

FALSE_ALARM = "False alarm. Your program warned about correct line. "

cur_dir = os.path.abspath(os.curdir)


class AnalyzerTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [TestCase(args=[f"test{os.sep}test_1.py"], check_function=self.test_1),
                TestCase(args=[f"test{os.sep}test_2.py"], check_function=self.test_2),
                TestCase(args=[f"test{os.sep}this_stage{os.sep}test_3.py"], check_function=self.test_3),
                TestCase(args=[f"test{os.sep}this_stage{os.sep}test_4.py"], check_function=self.test_4),
                TestCase(args=[f"test{os.sep}this_stage{os.sep}test_5.py"], check_function=self.test_5),
                TestCase(args=[cur_dir + f"{os.sep}test{os.sep}this_stage"], check_function=self.test_common)]

    # Stages 1-2 tests
    def test_1(self, output: str, attach):
        file_path = f"test{os.sep}test_1.py"
        output = output.strip().lower().splitlines()

        if len(output) != 9:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about nine mistakes in this test case")

        if not (output[0].startswith(f"{file_path}: line 1: s004") or
                output[7].startswith(f"{file_path}: line 13: s004")):
            return CheckResult.wrong(TWO_SPACES_BEFORE_COMMENT)

        if not (output[1].startswith(f"{file_path}: line 2: s003") or
                output[3].startswith(f"{file_path}: line 3: s003") or
                output[6].startswith(f"{file_path}: line 13: s003")):
            return CheckResult.wrong(UNNECESSARY_SEMICOLON)

        if not (output[2].startswith(f"{file_path}: line 3: s001") or
                output[4].startswith(f"{file_path}: line 6: s001")):
            return CheckResult.wrong(TOO_LONG_LINE)

        if not (output[5].startswith(f"{file_path}: line 11: s006")):
            return CheckResult.wrong(TOO_MANY_BLANK_LINES)

        if not output[8].startswith(f"{file_path}: line 13: s005"):
            return CheckResult.wrong(TODO)

        return CheckResult.correct()

    # Stage 4 tests
    def test_2(self, output: str, attach):
        file_path = f"test{os.sep}test_2.py"
        output = output.strip().lower().splitlines()
        if len(output) <= 1:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        for issue in output:
            if issue.startswith(f"{file_path}: line 6: ") or issue.startswith(f"{file_path}: line 10: "):
                return CheckResult.wrong(FALSE_ALARM)

        if not len(output) == 3:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about three mistakes in this test case")
        if not output[0].startswith(f"{file_path}: line 1: {error_code_class_def_spaces}"):
            return CheckResult.wrong(SPACES_AFTER_CLASS_FUNC)
        if not output[1].startswith(f"{file_path}: line 4: {error_code_class_name}"):
            return CheckResult.wrong(CLASS_NAME)
        if not output[2].startswith(f"{file_path}: line 14: {error_code_func_name}"):
            return CheckResult.wrong(FUNC_NAME)

        return CheckResult.correct()

    # Default variable is mutable test
    def test_3(self, output: str, attach):
        file_path = f"test{os.sep}this_stage{os.sep}test_3.py"
        output = output.strip().lower().splitlines()
        if len(output) < 1:
            return CheckResult.wrong("It looks like there is no messages from your program.")
        for issue in output:
            if issue.startswith(f"{file_path}: line 1: "):
                return CheckResult.wrong(FALSE_ALARM)
            if (issue.startswith(f"{file_path}: line 2: {error_code_default_argument_is_mutable}") or
                    issue.startswith(f"{file_path}: line 6: {error_code_default_argument_is_mutable}") or
                    issue.startswith(f"{file_path}: line 12: {error_code_default_argument_is_mutable}")):
                return CheckResult.wrong(FALSE_ALARM + "The program pointed correct function arguments as mutable.")

        if not len(output) == 1:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about one mistake in this test case")

        if not output[0].startswith(f"{file_path}: line 9: {error_code_default_argument_is_mutable}"):
            return CheckResult.wrong(MUTABLE_ARG)

        return CheckResult.correct()

    # Argument name test
    def test_4(self, output, attach):
        file_path = f"test{os.sep}this_stage{os.sep}test_4.py"
        output = output.strip().lower().splitlines()

        if len(output) < 1:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        for issue in output:
            if issue.startswith(f"{file_path}: line 1: "):
                return CheckResult.wrong(FALSE_ALARM)
            if issue.startswith(f"{file_path}: line 6: {error_code_arg_name}"):
                return CheckResult.wrong(FALSE_ALARM)
            if issue.startswith(f"{file_path}: line 9: {error_code_arg_name}"):
                return CheckResult.wrong(FALSE_ALARM + "Default value of argument was None.")

        if not len(output) == 1:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about one mistake in this test case")

        if not output[0].startswith(f"{file_path}: line 2: {error_code_arg_name}"):
            return CheckResult.wrong(ARG_NAME)

        return CheckResult.correct()

    # Variable name test
    def test_5(self, output, attach):
        file_path = f"test{os.sep}this_stage{os.sep}test_5.py"
        output = output.strip().lower().splitlines()
        if len(output) < 1:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        for issue in output:
            if issue.startswith(f"{file_path}: line 1: "):
                return CheckResult.wrong(FALSE_ALARM)
            if issue.startswith(f"{file_path}: line 6: {error_code_var_func_name}"):
                return CheckResult.wrong(FALSE_ALARM + "It was a part of the string - not a variable. ")
            if issue.startswith(f"{file_path}: line 8: {error_code_var_func_name}"):
                return CheckResult.wrong(FALSE_ALARM + "The None keyword starts with a capital letter. ")

        if not len(output) == 2:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about two mistakes in this test case")
        for i, j in enumerate([3, 9]):
            if not output[i].startswith(f"{file_path}: line {j}: {error_code_var_func_name}"):
                return CheckResult.wrong(VAR_FUNC_NAME)

        return CheckResult.correct()

    def test_common(self, output, attach):
        file_1 = cur_dir.lower() + f"{os.sep}test{os.sep}this_stage{os.sep}test_3.py"
        file_2 = cur_dir.lower() + f"{os.sep}test{os.sep}this_stage{os.sep}test_4.py"
        file_3 = cur_dir.lower() + f"{os.sep}test{os.sep}this_stage{os.sep}test_5.py"

        output = output.strip().lower().splitlines()

        if len(output) != 4:
            return CheckResult.wrong("It looks like there is an incorrect number of error messages. "
                                     f"Expected 4 lines, found {len(output)}")

        # negative tests
        for issue in output:
            if issue.startswith(f"{file_1}: line 1: "):
                return CheckResult.wrong(FALSE_ALARM)
            if (issue.startswith(f"{file_1}: line 2: {error_code_default_argument_is_mutable}") or
                    issue.startswith(f"{file_1}: line 6: {error_code_default_argument_is_mutable}") or
                    issue.startswith(f"{file_1}: line 12: {error_code_default_argument_is_mutable}")):
                return CheckResult.wrong(FALSE_ALARM + "The program pointed correct function arguments as mutable.")

            if issue.startswith(f"{file_2}: line 1: "):
                return CheckResult.wrong(FALSE_ALARM)
            if issue.startswith(f"{file_2}: line 6: {error_code_arg_name}"):
                return CheckResult.wrong(FALSE_ALARM)
            if issue.startswith(f"{file_2}: line 9: {error_code_arg_name}"):
                return CheckResult.wrong(FALSE_ALARM + "Default value of argument was None.")

            if issue.startswith(f"{file_3}: line 1: "):
                return CheckResult.wrong(FALSE_ALARM)
            if issue.startswith(f"{file_3}: line 6: {error_code_var_func_name}"):
                return CheckResult.wrong(FALSE_ALARM + "It was a part of the string - not a variable. ")
            if issue.startswith(f"{file_3}: line 8: {error_code_var_func_name}"):
                return CheckResult.wrong(FALSE_ALARM + "The None keyword starts with a capital letter. ")

        # test_3 file
        if not output[0].startswith(f"{file_1}: line 9: {error_code_default_argument_is_mutable}"):
            return CheckResult.wrong(MUTABLE_ARG)

        # test_4 file
        if not output[1].startswith(f"{file_2}: line 2: {error_code_arg_name}"):
            return CheckResult.wrong(ARG_NAME)

        # test_5 file
        for i, j in enumerate([3, 9]):
            if not output[i + 2].startswith(f"{file_3}: line {j}: {error_code_var_func_name}"):
                return CheckResult.wrong(VAR_FUNC_NAME)

        return CheckResult.correct()


if __name__ == '__main__':
    AnalyzerTest("analyzer.code_analyzer").run_tests()
