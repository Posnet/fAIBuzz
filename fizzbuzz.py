#!/usr/bin/env python3

from typing import Generator
import argparse
import openai


def validate_fizz_buzz(counter: int, to_validate: str) -> None:
    if counter % 15 == 0:
        test_str = "FizzBuzz"
    elif counter % 3 == 0:
        test_str = "Fizz"
    elif counter % 5 == 0:
        test_str = "Buzz"
    else:
        test_str = str(counter)

    assert (
        to_validate == test_str
    ), f"Invalid AI result, {to_validate} should have been {test_str}."


def fizz_buzz(limit: int) -> Generator[str, None, None]:
    messages = [
        {
            "role": "system",
            "content": """
    You are a FizzBuzz robot.
    Your role is to take in a number and then count from 1 up to an including that number.
    The results should be 1 number on each line.
    If the resulting number is divisible by 3, substitute it with "Fizz".
    If the resulting number is divisible by 5, substitute it with "Buzz".
    If the resulting number is diviisble by 3 AND 5, substitute it with "FizzBuzz".

    For example here is a python program that replicates your behavior.
    ```python
    def fizz_buzz(limit):
      for i in range(1, limit+1):
        if i % 3 == 0 and i % 5 == 0:
          print("FizzBuzz")
        elif i % 3 == 0:
          print("Fizz")
        elif i % 5 == 0:
          print("Buzz")
        else:
          print(i)
    ```
    """,
        },
        {
            "role": "user",
            "content": "20",
        },
        {
            "role": "assistant",
            "content": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n16\n17\nFizz\n19\nBuzz",
        },
        {"role": "user", "content": f"{limit}"},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", temperature=0, stream=True, messages=messages
    )

    buffer = ""
    ctr = 1
    for chunk in response:
        buffer += chunk.choices[0].delta.get("content", "")
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            yield line.strip()
    if buffer:
        yield buffer


def main():
    parser = argparse.ArgumentParser(
        description="A high performance FizzBuzz for the AI world."
    )
    parser.add_argument(
        "--validate", action="store_true", help="enable validation of FizzBuzz output"
    )
    parser.add_argument("limit", help="limit for which to fizz buzz to", type=int)
    args = parser.parse_args()
    for index, value in enumerate(fizz_buzz(args.limit)):
        print(value, end="")
        if args.validate:
            try:
                validate_fizz_buzz(index + 1, value)
            except AssertionError as e:
                print(f", {e}")
        print()


if __name__ == "__main__":
    main()
