# Use urllib.request to send network request if needed.

import dataclasses
import fileinput
import logging
from typing import Callable, Iterable, Optional, List, Union

_logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class StatsResult:
    # Need some typing around the result of stats because it has two
    # specifica values and some typing would be lost with
    # something like a tuple

    count_of_fibonacci_calls: int
    count_of_overlap_calls: int


@dataclasses.dataclass(frozen=True)
class InputCommand:
    # Representation of parsed commands from the input.
    # This is the first level of parsing that makes sure the
    # commands are at least one of the right names.

    command_name: str
    maybe_correct_args: Iterable[str]


# Some declared types to help with readability.
InputFunction = Callable[[], Iterable[str]]
FibonacciResult = Union[Iterable[int], str]
OverlapResult = Union[bool, str]

# Some constants used multiple places in program.
FIBONACCI_NAME = 'fibonacci'
OVERLAP_NAME = 'overlap'
STATS_NAME = 'stats'
ERROR_INDICATION = 'error'


class FibOverlapStatsException(Exception):
    # Creating this exception to handle fatal cases.
    # Creating a custom exception so that users can catch
    # this exception instead of generic python ones.

    pass


def calculate_fibonacci(maybe_correct_args: Iterable[str]) -> FibonacciResult:
    # Runs the fibonacci expansion for the given args.
    # The args might not be correct.  The args could be strings,
    # less than one, or maybe too many args.
    # The function returns a union type of either the correct sequence
    # of fibonacci numbers or "error"

    _logger.info(f"Calculating fibonacci with {maybe_correct_args}")
    number_of_args = len(maybe_correct_args)

    if number_of_args != 1:
        error_message = (
            f"Found {number_of_args} args for fibonacci: {maybe_correct_args}."
            f"  Should be 1."
        )

        _logger.error(error_message)

        raise FibOverlapStatsException(error_message)

    sole_arg = maybe_correct_args[0]

    try:
        # The try block catches non-ints.
        target_number = int(sole_arg, base=10)

        if target_number < 1:
            _logger.info("Fibonacci arg less than 1.")
            result = ERROR_INDICATION

        # Doing the base case here.
        elif target_number == 1:
            result: List[int] = [0, 1, 1]

        # Handling non base case.
        else:
            result: List[int] = [0, 1, 1]

            while True:
                # Calculate new number using previous two.
                new_number = result[-2] + result[-1]

                # Check if new number should be added.
                if new_number <= target_number:
                    result.append(new_number)

                # Exit the while loop if the new number should
                # not be added.  This means we are done.
                else:
                    break

    except ValueError:
        _logger.info("Fibonacci found invalid int value.")
        result = ERROR_INDICATION

    _logger.info(f"Fibonacci found values: {result}")

    return result


def calculate_overlap(maybe_correct_args: Iterable[str]) -> OverlapResult:
    # Runs the overlap for the given args.
    # The args might not be correct.  The args could be strings,
    # or maybe too few args.
    # The function returns a union type of either the correct boolean
    # result or "error".

    _logger.info(f"Calculating overlap with: {maybe_correct_args}")
    number_of_args = len(maybe_correct_args)

    if number_of_args < 2:
        error_message = (
            f"Found {number_of_args} args for overlap: {maybe_correct_args}."
            f"  Should be at least 2."
        )

        _logger.error(error_message)

        raise FibOverlapStatsException(error_message)

    ranges: List[List[int]] = []

    # Running the parsing and calculations within the try block 
    # in order to catch any non-int values.
    try:

        for single_maybe_range in maybe_correct_args:
            # Parse out the ranges.  Checks if they are ints.
            split_range = single_maybe_range.split(',')
            first_typed_number = int(split_range[0], base=10)
            second_typed_number = int(split_range[1], base=10)
            new_range = (first_typed_number, second_typed_number)
            ranges.append(new_range)

        # Assume the result is false, break upon finding one overlap.
        result = False

        # Enumerate here so that we can compare the range against remaining
        # ranges.  We do not need to re-check against previous ranges because
        # we already determined that they are not overlapping.
        for range_index, single_range in enumerate(ranges):

            # Iterate throug the rest of the ranges as explained above.
            for single_other_range in ranges[range_index+1:]:

                # Putting friendlier names on the values
                # so that the logic is clearer.
                this_min = single_range[0]
                this_max = single_range[1]
                other_min = single_other_range[0]
                other_max = single_other_range[1]
                min_in_bounds = this_min <= other_max
                max_in_bounds = this_max >= other_min

                # Exit the loop if we found one overlap.
                # Only one needs to be correct.
                # No need to check the rest.
                if min_in_bounds and max_in_bounds:
                    result = True
                    break

    except ValueError:
        _logger.info("Overlap found a non-int.")
        result = ERROR_INDICATION

    _logger.info(f"Overlap found result: {result}")

    return result


def calculate_stats(
    maybe_correct_args: Iterable[str],
    count_of_fibonacci_calls: int,
    count_of_overlap_calls: int
) -> StatsResult:

    # This function is mostly a pass-through to catch any fatal errors.
    # It is fatal if there are any args at all.

    number_of_args = len(maybe_correct_args)

    if number_of_args != 0:
        error_message = (
            f"Found more than 0 args for stats: {maybe_correct_args}"
        )

        _logger.error(error_message)

        raise FibOverlapStatsException(error_message)

    else:
        results = StatsResult(
            count_of_fibonacci_calls=count_of_fibonacci_calls,
            count_of_overlap_calls=count_of_overlap_calls
        )

    return results


def resolve_input(
    unparsed_input: Optional[Iterable[str]],
    input_function: InputFunction = fileinput.input
) -> Iterable[str]:

    # Check if input is provided to test function.
    # Not totally needed, but it allows for dep injection.

    if unparsed_input:
        resolved_unparsed_input = unparsed_input

    else:
        resolved_unparsed_input = input_function()

    return resolved_unparsed_input


def parse_input_into_commands(
    unparsed_input: Iterable[InputCommand]
) -> Iterable[InputCommand]:

    # High level function that checks to make sure
    # that each line has a valid command.
    # Does not check if all of the arguments are correct.

    _logger.info("Parsing input into commands")
    all_command_names = set([FIBONACCI_NAME, OVERLAP_NAME, STATS_NAME])
    parsed_commands: List[str] = []

    for single_line in unparsed_input:
        split_line = single_line.split(' ')

        try:
            command_name = split_line[0]
        except IndexError:
            error_message = "Line is blank."
            _logger.error(error_message)

            raise FibOverlapStatsException(error_message)

        if command_name in all_command_names:
            _logger.info(f"Found command: {command_name}")
            new_command = InputCommand(
                command_name=command_name,
                maybe_correct_args=split_line[1:]
            )

            parsed_commands.append(new_command)

        else:
            error_message = f"Command name not recognized: {command_name}"
            _logger.error(error_message)

            raise FibOverlapStatsException(error_message)

    _logger.info("Done parsing input into commands.")

    return parsed_commands


def serialize_fibonacci_result(fibonacci_result: FibonacciResult) -> str:

    if isinstance(fibonacci_result, str):
        serialized_result = fibonacci_result

    else:
        as_strings = [str(number) for number in fibonacci_result]
        serialized_result = ' '.join(as_strings)

    return serialized_result


def handle_commands(parsed_commands: Iterable[InputCommand]) -> str:
    # Run through each command and calculate it.
    # Serializes each command result into a string
    # and joins them together.
    # Tracks calls made to fib and overlap.

    _logger.info("Handling parsed commands.")

    # Used variables and kept increments inline
    # instead of passing around the counts.
    count_of_fibonacci_calls = 0
    count_of_overlap_calls = 0
    output_lines: List[str] = []

    for single_parsed_command in parsed_commands:

        if single_parsed_command.command_name == FIBONACCI_NAME:
            count_of_fibonacci_calls += 1
            fibonacci_result = calculate_fibonacci(
                maybe_correct_args=single_parsed_command.maybe_correct_args
            )

            serialized_fibonacci_result = serialize_fibonacci_result(
                fibonacci_result=fibonacci_result
            )

            output_lines.append(serialized_fibonacci_result)

        elif single_parsed_command.command_name == OVERLAP_NAME:
            count_of_overlap_calls += 1
            overlap_result = calculate_overlap(
                maybe_correct_args=single_parsed_command.maybe_correct_args
            )

            serialized_overlap_result = str(overlap_result)
            lower_overlap_result = serialized_overlap_result.lower()
            output_lines.append(lower_overlap_result)

        elif single_parsed_command.command_name == STATS_NAME:
            stats_result = calculate_stats(
                maybe_correct_args=single_parsed_command.maybe_correct_args,
                count_of_fibonacci_calls=count_of_fibonacci_calls,
                count_of_overlap_calls=count_of_overlap_calls
            )

            serialized_stats_result = (
                f"{stats_result.count_of_fibonacci_calls} "
                f"{stats_result.count_of_overlap_calls}"
            )

            output_lines.append(serialized_stats_result)

        else:
            error_message = (
                f"Parsed input command not recognized: {single_parsed_command}"
            )

            raise FibOverlapStatsException(error_message)

    joined_lines = '\n'.join(output_lines)
    _logger.info("Done handling parsed commands.")

    return joined_lines


def codeHere(
    unparsed_input: Optional[Iterable[str]] = None,
    input_function: InputFunction = fileinput.input
) -> str:

    _logger.info("Starting main process.")
    resolved_unparsed_input = resolve_input(
        unparsed_input=unparsed_input,
        input_function=input_function
    )

    parsed_commands = parse_input_into_commands(
        unparsed_input=resolved_unparsed_input
    )

    result = handle_commands(parsed_commands=parsed_commands)
    _logger.info("Finished main process.")

    # Use the function to return the solution.
    return result


print(codeHere())
