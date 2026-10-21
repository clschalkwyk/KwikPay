# KwikPay

KwikPay is a digital payment and settlement helper for South African spaza shops. It helps shop owners process sales, automatically split transaction value across business categories, and forward the payment record to an interoperable payment service.

## What this app does

KwikPay takes a sale amount and divides it according to configured percentages:

- Supplier
- Salaries
- Maintenance
- Profit

Example:

- Sale total: R20.00
- Supplier: 2% = R0.40
- Salaries: 3% = R0.60
- Maintenance: 5% = R1.00
- Profit: R18.00

This gives the business a clear view of where money is being allocated without doing manual calculations after each sale.

## Interledger integration

This repository is now connected to the external Interledger payment service at Holang-1/InterledgerPaymentService.

When a sale includes a shopId, KwikPay sends a payment creation request to the remote service at:

- POST /api/payments
- JSON payload:
  - shopId
  - amount
  - currency

The external service expects the currency to be ZAR and will return a payment object including the generated payment id and status.

## Project status

This project is in active development and is currently working through the following stage:

### Dev 2: payment service integration

Completed in this repo:

- Added Interledger payment submission from the sales API
- Added validation and guardrails around sale totals and percentages
- Hardened rules so invalid numbers and reserved rule names are rejected early
- Ensured allocations round cleanly to cents and preserve the total sale value
- Added regression tests covering the financial and Interledger behavior

## Environment variables

The app reads percentage values from environment variables when no explicit values are passed:

- KWIKPAY_SUPPLIER_PERCENT=2
- KWIKPAY_SALARIES_PERCENT=3
- KWIKPAY_MAINTENANCE_PERCENT=5
- INTERLEDGER_PAYMENT_SERVICE_URL=http://localhost:8080

## Example call

```python
from sales_api import create_sale_response

response = create_sale_response({
    "amount": 20,
    "shopId": "shop-42",
    "supplier": 2,
    "salaries": 3,
    "maintenance": 5,
})

print(response)
```

Example response shape:

```json
{
  "amount": 20.0,
  "split": {
    "supplier": 0.4,
    "salaries": 0.6,
    "maintenance": 1.0,
    "profit": 18.0
  },
  "payment": {
    "id": "uuid",
    "shopId": "shop-42",
    "amount": 20.0,
    "currency": "ZAR",
    "status": "PENDING"
  }
}
```

## Business value

KwikPay is designed to reduce friction for small businesses, improve financial visibility, and make digital payments easier for communities that still rely heavily on cash. It helps owners stay in control of their money while supporting more transparent, scalable operations.

## Run the tests

```bash
python -m unittest
```

## Development notes

The local codebase is intentionally lightweight and business-focused. It acts as a rules engine and sales API while the external Interledger Spring service handles payment persistence and settlement orchestration.
