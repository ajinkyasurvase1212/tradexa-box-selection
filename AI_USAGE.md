\# AI Usage Documentation



\## AI Tool Used



ChatGPT was used as an AI assistance tool during the development of this assignment.



\## Purpose of AI Usage



AI assistance was used for:



\- Understanding the assignment requirements

\- Discussing the Django project structure

\- Discussing database model design

\- Understanding the box-selection approach

\- Debugging and resolving development issues

\- Designing automated test cases

\- Reviewing API validation

\- Preparing project documentation



\## Prompts Used



The prompts used during development included requests related to:



\- Setting up a Django project for the assignment

\- Designing Product, Box, Order, and OrderItem models

\- Implementing the box-selection logic

\- Handling product dimension rotations

\- Implementing the Django REST API

\- Creating automated Django tests

\- Handling API validation

\- Preparing README documentation



The actual conversation transcript containing the prompts and responses is included separately in the repository as required by the assignment.



\## Accepted AI Suggestions



AI suggestions were used as a starting point for:



\- Django project structure

\- Model relationships

\- Service-layer organization

\- Box-selection implementation

\- REST API implementation

\- Automated test structure

\- API validation

\- Documentation structure



The generated suggestions were reviewed and tested before being retained in the project.



\## Rejected or Modified Suggestions



Some suggestions were modified during implementation rather than being used without verification.



Examples include:



\- Adjusting the box-selection logic to handle multiple products and quantities.

\- Adding validation for non-existent products.

\- Adding validation for empty orders.

\- Adding additional automated tests.

\- Adjusting the project documentation to match the actual implementation.



\## Mistakes or Issues Identified



During development, some implementation details required correction or improvement.



The main issues identified were:



\- The initial box-selection implementation needed to consider multiple products rather than only checking a single product.

\- Additional API validation was required for invalid product IDs and empty order items.

\- Additional tests were added to verify multiple products and quantities.

\- The implementation uses a practical packing heuristic rather than claiming to solve optimal 3D bin packing.



These issues were identified through testing and review.



\## Verification Process



The final implementation was verified using:



1\. Django system checks:



```bash

python manage.py check
2. Automated Django tests:
python manage.py test

3. API testing using Thunder Client.
4. Manual verification of successful box recommendations.
5. Manual verification of cases where no suitable box is available.
The automated test suite contains 12 tests and all tests passed successfully.
Final Verification Result
Found 12 test(s).
............
----------------------------------------------------------------------
Ran 12 tests in ...s

OK
