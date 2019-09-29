Steps and thoughts while solving the various test questions.
[Kevin Smith <kevinsmith.kis@gmail.com>]

# Solution Process
1. Setup environment. (Venv ->source ./bin/activate, deactivate)
2. navigate to /ctrl-backend-interview-test/interview-test/interview-test
3. pip install -r requirements.txt
4. Investigate.
5. Solve Q1: (and test with asserts)
    a. combine_two_lists_parallel [DONE]
    b. return_matches_in_list_parallel [DONE]
    c. count_shakespeare (added my own asserts to test my solution) (note that my gut feeling here was to use sets, 
    for the punctuation removal, but translate is around 6x faster. - I also know regex is faster but not everyone 
    likes those...) [DONE]
    d. infinite_loop (made assumptions and completed function.)[DONE]
6. Solve Q2: (added a try, finally and a args task list on an asyncio gather function) [DONE]
7. Solve Q3 (the api)
    a. authentication endpoint  [DONE] (The auth system used is based on jwt. which makes storing the token 
    irrelevant or superfluous)
    b. get user endpoint (auth required) [DONE]
    c. user endpoint to create a new user [DONE]
    d. get with auth to get the user's balance  [DONE]
    e. one POST request for both credit and debit. Hint query/params  [DONE]
8. made a commit to the git
9. place in git account. send the link.

# Notes
1. Use 1 additional library. It was added to the requirements.txt (pyjwt) for the auth process.
2. Used a decorator as well in the auth process.
3. Used params for the credit/debit setup.
4. Completed Q2 in main_two.
5. Completed Q3 in main_three. It was just simpler.
6. Added the postman testing setup for the API.
