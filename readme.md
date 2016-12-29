**Running the application**
============================

1. To run tests, use the following command:

    ```python manage.py test```

2. To run application, use the following command:

    ```python manage.py production```

*To end the session in production, just press 'Enter' without entering any text*


**Flow**
========

**Steps:**
1. String Input (Format: <order-id> <time> <stock> <buy/sell> <quantity> <price>)
2. Input Length Validation
3. Conversion to native input
4. Parameters Type/Value Validation
5. Exchange Processing
6. Native Output (After the session is completed)
7. Print the output in desired format (<sell-order-id> <quantity> <sell-price> <buy-order-id>)

Here native input/output is in reference to the given framework input/output.

Please note that a session can also end prematurely with a wrong input given. This failure will be accompanied by an intermediate output of completed and pending transactions.