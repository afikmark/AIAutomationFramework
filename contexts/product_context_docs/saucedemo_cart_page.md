# SauceDemo / Swag Labs — Cart Page Documentation

## Overview

The **Cart Page** lists all items the user added from the inventory. It allows users to review, remove, and proceed to checkout.

## URL & Navigation

| Environment       | URL / Path                                                                 | Notes                               |
| ----------------- | -------------------------------------------------------------------------- | ----------------------------------- |
| Production / Demo | [https://www.saucedemo.com/cart.html](https://www.saucedemo.com/cart.html) | Accessed by clicking the cart icon. |

## Layout & Design

* Title: **"Your Cart"**
* Each listed product includes:

  * Item name (linked to detail page)
  * Description
  * Quantity (always "1" per item in demo)
  * Price
  * "Remove" button
* **Buttons**:

  * "Continue Shopping" → back to `/inventory.html`
  * "Checkout" → proceeds to step one of checkout.

## Behavioral Logic

1. User adds items in the inventory page.
2. Cart reflects selected items with total quantity badge.
3. User can remove items — item disappears instantly.
4. Clicking "Checkout" redirects to `/checkout-step-one.html`.
