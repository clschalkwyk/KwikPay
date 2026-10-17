# KwikPay

KwikPay is a payment and settlement platform designed for South African spaza shops. It helps owners accept digital payments more easily, split funds automatically, and manage the business with less manual cash handling.

## Project Idea

Spaza shops are a vital part of South African communities. They provide everyday essentials to local communities and support millions of livelihoods, but many still depend on cash because digital payment systems are often too expensive, too complex, or not interoperable enough.

KwikPay addresses that gap by making transactions simple, affordable, and flexible. When a customer buys bread for R20, the system can automatically split the payment according to the business rules configured for that shop.

Example:

- Supplier: 2% = R0.40
- Salaries: 3% = R0.60
- Maintenance: 5% = R1.00
- Profit: R18.00

This helps the owner understand where money is going without manually calculating each sale.

## Why KwikPay?

Spaza shops play an important role in South African communities, but they are still heavily cash-driven. Many payment options involve high transaction costs, expensive hardware, difficult onboarding, delayed settlements, or systems that do not work well across different providers.

This makes it hard for small businesses to adopt digital payments while maintaining control over cost, cash flow, and operational simplicity.

KwikPay aims to make digital payments more accessible, practical, and affordable for township businesses by using open and interoperable payment principles. The goal is to reduce friction and make it easier for shop owners to accept digital payments without being locked into one provider or paying excessive fees.

## Environment-based Configuration

The app is designed to be flexible. Instead of hardcoding split values into the code, it reads business rules from environment variables.

Example configuration:

- KWIKPAY_SUPPLIER_PERCENT=2
- KWIKPAY_SALARIES_PERCENT=3
- KWIKPAY_MAINTENANCE_PERCENT=5

If no value is passed directly into the function, the app uses those environment variables. This makes it easy to change the business model without rewriting the application.

## Main Features

- Automatic transaction splitting
- Simple payment flow for spaza shops
- Open and configurable payment rules
- Percentage-based allocation
- Automatic profit calculation
- Business-friendly reporting and transparency

## Example Workflow

1. A customer buys a product for R20
2. The app reads the configured payment percentages from environment variables
3. The sale is split automatically across supplier, salaries, maintenance, and profit
4. The owner sees the breakdown immediately
5. The shop gets a cleaner digital payment experience with less manual admin

## Business Value

KwikPay is designed to reduce friction for small businesses, improve financial visibility, and make digital payments easier for communities that still rely heavily on cash. It helps owners stay in control of their money while supporting more transparent and scalable operations.

## Current Status

This project is in early development, with a focus on automatic revenue splitting, digital payment accessibility, and flexible configuration for spaza shop operations.
