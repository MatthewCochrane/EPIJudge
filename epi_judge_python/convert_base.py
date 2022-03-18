from test_framework import generic_test


def convert_base(num_as_string: str, b1: int, b2: int) -> str:
    """
    Start: 11:49

    Assuming we don't have a base higher than 36 so we can get by with just capital letters...

    How do we convert a number from one base to another?

    Example:
        123 base 10, convert to base 3
        process digit by digit
        add 3 to result
        add 20 to result
        add 100 to result

        how do we add 20 in base 3 to base 3 result?
        Could we 'go through binary'?

        convert num_as_str to an integer
        convert that integer to a string

        We could get huge numbers that don't fit into an integer.  They didn't say anything about that though...
        That's a question I'd ask the interviewer...

        convert to int:
            for each char:
                if not (is_alpha(char) or is_numeric(char)):
                    continue
                result *= base
                digit = digit_to_int(char)
                result += digit
            return result * (-1 if first char is '-' else 1)

        convert to base:
            check for zero
            was_neg = x < 0
            x = abs(0)
            res = []
            while x:
                digit = x % base
                x //= base
                res.append(digit_to_str(digit))
            if was_neg:
                res.append('-')
            res.reverse()
            return ''.join(res)

        return convert_to_base(convert_to_int(num_as_str, b1), b2)

    O(log n) time where n is the number as an integer
    O(log n) space too

    All passing
    Time: 12:17
    Fairly large problem.
    I think the idea of 'going through' binary was a good choice.
    """

    def char_to_int(c: str) -> int:
        if str.isnumeric(c):
            return ord(c) - ord("0")
        return 10 + ord(c.upper()) - ord("A")

    def digit_to_char(x: int) -> str:
        if x < 10:
            return chr(ord("0") + x)
        return chr(ord("A") + (x - 10))

    def convert_to_int(num: str, base: int) -> int:
        result = 0
        for c in num:
            if not str.isalnum(c):
                continue
            result *= base
            digit = char_to_int(c)
            result += digit
        return result * (-1 if num[0] == "-" else 1)

    def convert_to_base(x: int, base: int) -> str:
        if x == 0:
            return "0"
        negative = x < 0
        x = abs(x)
        res = []
        while x:
            digit = x % base
            x //= base
            res.append(digit_to_char(digit))
        if negative:
            res.append("-")
        res.reverse()
        return "".join(res)

    return convert_to_base(convert_to_int(num_as_string, b1), b2)


if __name__ == "__main__":
    exit(
        generic_test.generic_test_main(
            "convert_base.py", "convert_base.tsv", convert_base
        )
    )
