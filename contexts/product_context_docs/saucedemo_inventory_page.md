# SauceDemo / Swag Labs — Inventory Page Documentation

## Overview

The **Inventory Page** (also known as the Products page) is the main shopping area of the SauceDemo application. It lists all available items for purchase and provides user actions such as sorting, viewing product details, and adding/removing items from the cart.

## URL & Navigation

| Environment       | URL / Path                                                                           | Notes                            |
| ----------------- | ------------------------------------------------------------------------------------ | -------------------------------- |
| Production / Demo | [https://www.saucedemo.com/inventory.html](https://www.saucedemo.com/inventory.html) | Accessed after successful login. |
| Redirect Behavior | Redirects to login if accessed unauthenticated.                                      |                                  |

Once logged in, the system always lands on this page by default.

## Layout & Design

* Page title "Products" at the top center.
* **Top navigation bar** includes:

  * The **hamburger menu** (top-left).
  * The **shopping cart icon** (top-right) with a badge showing the number of items in the cart.
  * The **product sort dropdown** (top-right of the item list).
* Products are displayed in a **grid layout**, each card containing:

  * Product image.
  * Product name (clickable → goes to product detail).
  * Product description.
  * Product price.
  * **Add to Cart / Remove** button.

## Behavioral Logic & UX Flow

### Normal Flow

1. User views available items.
2. User can sort the list by:

   * Name (A–Z / Z–A)
   * Price (low–high / high–low)
3. Clicking on a product name/image navigates to its detail page.
4. Clicking "Add to cart" toggles to "Remove" and increases the cart count badge.
5. Clicking "Remove" decreases the cart count badge.

### Sorting Behavior

* Sorting is instantaneous (client-side) and affects only visible list order.
* No backend refresh occurs; all data is preloaded.

### Edge / UX Notes

* When an item is added, the cart badge updates without a page reload.
* The product list and state persist unless "Reset App State" is used (via the menu).
* Product details maintain consistent item data across sessions.
