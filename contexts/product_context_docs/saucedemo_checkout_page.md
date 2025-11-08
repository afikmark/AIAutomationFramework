# SauceDemo / Swag Labs — Checkout Page Documentation

The checkout flow is divided into **three sequential steps**.

---

## Step One — Your Information

### URL & Navigation

| Path                      | Notes                                   |
| ------------------------- | --------------------------------------- |
| `/checkout-step-one.html` | Requires at least one item in the cart. |

### Layout & Inputs

* Title: **"Checkout: Your Information"**
* Fields:

  * First Name (required)
  * Last Name (required)
  * Postal Code (required)
* Buttons:

  * "Cancel" → returns to cart.
  * "Continue" → proceeds to step two if all fields are valid.

### Behavior & Validation

* All fields required; missing fields show an inline red error message.
* On success → `/checkout-step-two.html`.

---

## Step Two — Overview

### URL & Navigation

| Path                      | Notes                                |
| ------------------------- | ------------------------------------ |
| `/checkout-step-two.html` | Displays cart summary + total price. |

### Layout & Design

* Title: **"Checkout: Overview"**
* Displays list of all products to be purchased:

  * Name, description, and price.
* Shows:

  * **Item total**
  * **Tax**
  * **Total (sum)**

### Buttons:

* "Cancel" → back to inventory page.
* "Finish" → completes purchase → `/checkout-complete.html`.

---

## Step Three — Complete

### URL & Navigation

| Path                      | Notes                    |
| ------------------------- | ------------------------ |
| `/checkout-complete.html` | Final confirmation page. |

### Layout & Design

* Title: **"Checkout: Complete!"**
* Main message: "Thank you for your order!"
* Sub-message: "Your order has been dispatched..."
* "Back Home" button returns to `/inventory.html`.
