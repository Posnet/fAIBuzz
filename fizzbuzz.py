#!/usr/bin/env python3

from typing import Generator
import argparse
import openai


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
    for chunk in response:
        buffer += chunk.choices[0].delta.get("content", "")
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            yield line
    if buffer:
        yield buffer


def main():
    parser = argparse.ArgumentParser(description="A high performance FizzBuzz for the AI world")
    parser.add_argument("limit", help="Limit for which to fizz buzz to.", type=int)
    args = parser.parse_args()
    for value in fizz_buzz(args.limit):
        print(value)


if __name__ == "__main__":
    main()
