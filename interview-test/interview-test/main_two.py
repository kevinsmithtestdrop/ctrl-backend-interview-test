from two_async.async_functions import method_one, method_two, method_three, method_four
import asyncio


async def main():
    """
    Question

    call async functions together and return in the order function_one, function_two, function_three, function_four.

    Many ways to call these async functions, extra points for good use of asyncio. Try and fire all at the same time
    and get the results together

    :return: None
    """
    tasks = [method_one(), method_two(), method_three(), method_four()]
    result_list = await asyncio.gather(*tasks, return_exceptions=True)

    print(result_list)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Note: Python 3.7 has some nicer options than the current setup. Will be sticking to 3.5 to 3.6 here though.
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

    """
    Question:
    Run main() method
    """
