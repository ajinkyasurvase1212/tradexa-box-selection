# AI-Assisted Box Selection System

A Django-based shipping box recommendation system for an ecommerce platform.

The system evaluates an order's products based on their dimensions and weight, checks available shipping boxes, and recommends the most suitable box based on physical fit, weight capacity, and cost.

## Features

- Product management
- Shipping box management
- Order and order-item management
- Product quantity support
- Dimension validation
- Product rotation/orientation support
- Maximum weight validation
- Multiple products in an order
- Cheapest suitable box selection
- REST API for creating orders
- Input validation
- Automated test cases
- Django Admin interface

## Technology Stack

- Python
- Django
- Django REST Framework
- SQLite
- HTML
- JavaScript
- Git
- GitHub

## Project Structure

```text
tradexa-box-selection/
│
├── box_selection/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── shipping/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   └── shipping/
│       └── index.html
│
├── manage.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
├── TEST_OUTPUT.md
└── .gitignore


Database Models

Product

Stores product information:
- Name
- Length
- Width
- Height
- Weight

Box

Stores shipping box information:
- Name
- Internal length
- Internal width
- Internal height
- Maximum weight
- Cost

Order

Stores customer orders.
OrderItem
Connects products to orders and stores the quantity of each product.

Setup Instructions
1. Clone the Repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd tradexa-box-selection
2. Create a Virtual Environment
For Windows:
python -m venv venv

Activate the virtual environment:
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Apply Database Migrations
python manage.py migrate

5. Create a Superuser
python manage.py createsuperuser

6. Start the Development Server
python manage.py runserver

The application will be available at:
http://127.0.0.1:8000/

Django Admin:
http://127.0.0.1:8000/admin/

API
Create Order
Endpoint:
POST /api/orders/

Local URL:
http://127.0.0.1:8000/api/orders/

Request
{
    "items": [
        {
            "product_id": 1,
            "quantity": 1
        },
        {
            "product_id": 2,
            "quantity": 2
        }
    ]
}

Successful Response
{
    "order_id": 1,
    "recommended_box": {
        "id": 1,
        "name": "Small Box",
        "cost": 50.0
    },
    "message": "Suitable box found."
}

No Suitable Box
{
    "order_id": 2,
    "recommended_box": null,
    "message": "No suitable box found."
}

Box Selection Logic
The system follows these steps:
1. Calculate the total weight of all products in the order.
2. Check whether the total weight is within the box's maximum weight capacity.
3. Check whether each product can fit inside the box.
4. Consider different orientations of product dimensions.
5. Attempt to pack the products using the implemented 3D shelf-style packing heuristic.
6. Reject the box if the complete order cannot be packed.
7. Compare all suitable boxes.
8. Select the suitable box with the lowest cost.
Packing Approach
The implementation uses a deterministic shelf-style 3D packing heuristic.
Products are considered in descending order of volume. Different orientations are attempted when placing each product.
The implementation is intended as a practical solution for this assignment and does not claim to provide an optimal mathematical solution to the general 3D bin-packing problem.
API Validation
The API validates:
- Product existence
- Quantity greater than zero
- At least one order item
Invalid requests return an HTTP 400 Bad Request response.
Testing
The project contains automated Django test cases covering:
- Product fitting inside a box
- Product not fitting inside a box
- Product rotation
- Cheapest suitable box selection
- Weight capacity
- No suitable box
- Multiple products
- Multiple quantities
- Successful API request
- Invalid quantity
- Invalid product
- Empty order
Run the complete test suite with:

python manage.py test
Expected result:
Found 12 test(s).
............
----------------------------------------------------------------------
Ran 12 tests in ...s

OK

API Testing
The API was tested using Thunder Client.
Example request:
{
    "items": [
        {
            "product_id": 1,
            "quantity": 1
        }
    ]
}

The API returns the recommended box and its cost when a suitable box is available.
AI Usage
AI tools were used during development for assistance with understanding the requirements, discussing implementation approaches, debugging, testing, and documentation.
Detailed information about AI usage, prompts, accepted/rejected suggestions, identified mistakes, and verification steps is provided separately in:
AI_USAGE.md

Test Output
The final test execution output is documented in:
TEST_OUTPUT.md

Assumptions
- Product dimensions and box dimensions use the same unit.
- Product weight and box maximum weight use the same weight unit.
- A box must satisfy both dimensional and weight constraints.
- When multiple boxes are suitable, the lowest-cost suitable box is selected.
- The packing implementation uses a heuristic and does not guarantee mathematically optimal 3D packing.

## What I Learned

Through this assignment, I learned how to design and build a Django application for a real-world ecommerce problem. I learned how to create Django models and relationships between products, orders, and order items. I also learned how to separate the business logic into a service layer instead of putting all the logic inside the views. One of the challenging parts was handling product dimensions and different orientations while checking whether products could fit inside a box. I also learned how to create REST APIs using Django REST Framework and validate different types of invalid input. Writing automated test cases helped me understand how to verify different scenarios such as weight limits, product rotation, multiple products, and cases where no suitable box is available. Overall, this assignment improved my understanding of Django, API development, testing, and implementing business logic for a practical problem.