# AI Usage Disclosure

<!--
Fill in this file before you submit. Submissions without it are not graded.
If you used no AI tools, delete everything below and write only:
No AI tools were used.
-->

## Tools used

- - ChatGPT (OpenAI)

## Conversation links

- Link 1:- Implementation review and explanations:https://chatgpt.com/share/6b0650d6-034c-83ed-b4e2-ed1ff0714490


## What I used them for

- I used ChatGPT to help with the implementation, understand the assignment requirements, review different coding approaches and identify possible edge cases. It also helped me understand validation, duplicate detection, query filtering and error handling.

## Which parts of the code were AI-generated or substantially AI-assisted

| File | Function or part | How (generated / modified / explained) |
| --- | --- | --- |
| validator.py | Airport loading, datetime validation, validate_row() and to_record() | Generated and explained |
| csv_loader.py | CSV processing, duplicate detection and error collection | Generated and explained |
| query.py | Query validation, filtering, sorting and limiting results | Generated and explained |
| flight_parser.py | Argument handling, file processing, logging and exception handling | Generated and explained |


## Key prompts

1. How can early returns preserve the required validation order, and how should unusual prices and datetime values be handled?
2. Is using a set of tuples a reliable approach for detecting duplicate flights across multiple CSV files?
3. How can filtering, stable sorting and limiting be implemented without changing the original database?
4. How should CSV and JSON processing be separated, and how can logging handlers be properly closed?
5. What additional edge cases should be considered before submitting the project?

## What I changed or verified myself
I set up the GitHub repository and Codespaces environment, added my student information and checked the project structure. I applied and reviewed the AI-assisted code in each Python file. I ran the official public tests using Python 3.13.5 in GitHub Codespaces and passed all 29 tests. I also ran 13 additional checks covering invalid dates, unusual price values and invalid query parameters. All of these checks passed. I reviewed alternative implementations and kept the existing working code where no changes were necessary.
