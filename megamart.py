from datetime import datetime
from typing import Dict, Tuple, Optional
from DiscountType import DiscountType
from PaymentMethod import PaymentMethod
from FulfilmentType import FulfilmentType
from TransactionLine import TransactionLine
from Transaction import Transaction
from Item import Item
from Customer import Customer
from Discount import Discount

from RestrictedItemException import RestrictedItemException
from PurchaseLimitExceededException import PurchaseLimitExceededException
from InsufficientStockException import InsufficientStockException
from FulfilmentException import FulfilmentException
from InsufficientFundsException import InsufficientFundsException

# You are to complete the implementation for the eight methods below:
#### START


def is_not_allowed_to_purchase_item(item: Item, customer: Customer, purchase_date_string: str) -> bool:
    """
    Returns True if the customer is not allowed to purchase the specified item, False otherwise.
    In all cases, if an item object was not actually provided, an Exception should be raised.

    Items that are under the alcohol, tobacco or knives category may only be sold to customers who are aged 18+ and have their ID verified.
    An item potentially belongs to many categories - as long as it belongs to at least one of the three categories above, restrictions apply to that item.
    The checking of an item's categories against restricted categories should be done in a case-insensitive manner.
    For example, if an item A is in the category ['Alcohol'] and item B is in the category ['ALCOHOL'], both items A and B should be identified as restricted items.
    
    The customer object represents a customer's account (personal profile), and contains some of their personal details.
    It is optional for customers to provide their date of birth in their profile. In this case, the customer will not be able to purchase restricted items as their actual age cannot be determined.

    The age of the customer is calculated as the number of full years since their specified date of birth and the purchase date. Both purchase and birth dates are of the format dd/mm/yyyy.
    Hence, a customer whose date of birth is 01/08/2005 is only considered to be age 18+ on or after 01/08/2023.
    For example, if purchasing restricted items on 31/07/2023, the customer is considered underage and may not purchase these restricted items.

    Even if the customer is actually aged 18+ and is verified (in the real world), they must provide/link their customer account to the transaction when purchasing restricted items (i.e. customer argument value is not None).
    Otherwise, if a customer account is not provided/linked to the transaction (i.e. the customer argument value is None), they will not be allowed to purchase the restricted item even if they would have been eligible.

    If an item is a restricted item but the provided purchase date or provided birth date is in the incorrect format, an Exception should be raised.
    If an item is a restricted item but the purchase date is not provided, True should be returned.
    If an item is a restricted item but the customer's birth date is not provided, True should be returned.
    If an item is a restricted item but the customer's ID is not verified, True should be returned.
    
    If an item is not a restricted item and the provided purchase date is not formatted correctly or not provided, an Exception does not need to be raised.
    If an item is not a restricted item, the customer's birth date and ID verification status does not need to be checked.
    """
    # Check if item object is provided
    if item is None:
        raise Exception("Item object not provided.")

    # Check if item is in the restricted category
    restricted_cat = ["alcohol", "tobacco", "knives"]
    is_item_restricted = any(category.lower() in restricted_cat for category in item.categories)

    if is_item_restricted:
        # If purchase date is not provided
        if not purchase_date_string:
            return True

        # Check if purchase date is in correct format
        try:
            purchasedate = datetime.strptime(purchase_date_string, "%d/%m/%Y")
        except ValueError:
            raise Exception("Purchase date is in incorrect format.")

        # If customer is not provided or birth date is not provided or ID not verified
        if not customer or not customer.date_of_birth or not customer.id_verified:
            return True

        # Check if birth date is in correct format and calculate age
        try:
            birthdate = datetime.strptime(customer.date_of_birth, "%d/%m/%Y")
            age = purchasedate.year - birthdate.year - ((purchasedate.month, purchasedate.day) < (birthdate.month, birthdate.day))
        except ValueError:
            raise Exception("Birth date is in incorrect format.")

        # Check if customer is underage
        if age < 18:
            return True

        return False
    return False


def get_item_purchase_quantity_limit(item: Item, items_dict: Dict[str, Tuple[Item, int, Optional[int]]]) -> Optional[int]:
    '''
    For a given item, returns the integer purchase quantity limit.
    If an item object or items dictionary was not actually provided, an Exception should be raised.
    If the item was not found in the items dictionary or if the item does not have a purchase quantity limit, None should be returned.
    The items dictionary (which is a mapping from keys to values) contains string item IDs as its keys,
    and tuples containing an item object, integer stock level and an optional integer purchase quantity limit (which may be None) that correspond to their respective item ID as values.
    '''
    # Check that an item object and items dictionary are actually provided.
    if item is None or items_dict is None:
        raise Exception("Item object or items dictionary not provided.")

    # Check if item is in items dictionary.
    if item.id in items_dict:
        # Check if item has purchase quantity limit.
        if items_dict[item.id][2] is not None:
            return items_dict[item.id][2]
        else:
            return None
    else:
        return None

##### HERE IS THE FIRST PART#####


def is_item_sufficiently_stocked(item: Item, purchase_quantity: int, items_dict: Dict[str, Tuple[Item, int, Optional[int]]]) -> bool:
    """
    For a given item, returns True if the purchase quantity does not exceed the currently available stock, or False if it exceeds, or the item was not found in the items dictionary.
    If an item object, purchase quantity or items dictionary was not actually provided, an Exception should be raised.
    Purchase quantity should be a minimum of 1, and stock level is always a minimum of 0. Otherwise, an Exception should be raised for each of these situations.
    The items dictionary (which is a mapping from keys to values) contains string item IDs as its keys,
    and tuples containing an item object, integer stock level and an optional integer purchase quantity limit (which may be None) that correspond to their respective item ID as values.
    """
    # Check that an item object, purchase quantity, and items dictionary are actually provided.
    if item is None or purchase_quantity is None or items_dict is None:
        raise Exception("Item object, purchase quantity or items dictionary not provided.")
    # Check if item is in items dictionary.
    if item.id in items_dict:
        # Check if item has stock level.
        if items_dict[item.id][1] is not None:
            if items_dict[item.id][1] >= 0:
                # Check if purchase quantity is valid.
                if purchase_quantity >= 1:
                    # Check if purchase quantity is less than or equal to stock level.
                    if purchase_quantity <= items_dict[item.id][1]:
                        return True
                    else:
                        return False
                else:
                    raise Exception("Purchase quantity is not a positive integer more than zero.")
            else:
                raise Exception("Item stock level is not zero or a positive integer.")
        else:
            raise Exception("Item stock level not provided.")
    else:
        return False
    

def calculate_final_item_price(item: Item, discounts_dict: Dict[str, Discount]) -> float:
    """
    An item's final price may change if there is currently a discount available for it.
    If an item object or discounts dictionary was not actually provided, an Exception should be raised.
    There are two types of discounts - it may be a percentage off the original price, or a flat amount off the original price.
    Percentage-based discounts have a value defined between 1 and 100 inclusive. Otherwise, an Exception should be thrown.
    For example, a percentage-type discount of value 25 means a 25% discount should be applied to that item.
    Flat-based discounts should not cause the item's final price to be more than its original price or be negative. Otherwise, an Exception should be thrown.
    For example, a flat-type discount of value 1.25 means a discount of $1.25 should be applied to that item.
    The discounts dictionary (which is a mapping from keys to values) contains string item IDs as its keys, and discount objects that correspond to their respective item ID as values.
    If an item has an associated discount, the discounts dictionary (which is a mapping from keys to values) will contain a key corresponding to the ID of that item.
    Otherwise, if the item does not have an associated discount, its final price would be the same as its original price.
    """
 # Check if item object and discounts dictionary are provided
    if item is None or discounts_dict is None:
        raise Exception("Item object or discounts dictionary not provided.")
        
    # Initialize the final price with the original price
    final_price = item.original_price

    # Check if there is a discount for the item
    if item.id in discounts_dict:

        # Get the discount object
        discount = discounts_dict[item.id]

        # Apply the discount
        if discount.type == DiscountType.PERCENTAGE:
            # Check if discount value is within the valid range
            if 1 <= discount.value <= 100:
                final_price -= final_price * (discount.value / 100)
            else:
                raise Exception("Invalid percentage value for discount.")
        elif discount.type == DiscountType.FLAT:
            # Check if the discount makes the price negative or greater than original
            if discount.value < 0 or discount.value > final_price:
                raise Exception("Invalid flat discount value. Final price would be negative or greater than original price.")
            final_price -= discount.value
        else:
            raise Exception("Unknown discount type.")
    
    return round(final_price, 2)  # Rounding to 2 decimal places

def calculate_item_savings(item_original_price: float, item_final_price: float) -> float:
    """
    Savings on an item is defined as how much money you would not need to spend on an item compared to if you bought it at its original price.
    If an item's original price or final price was not actually provided, an Exception should be raised.
    If the final price of the item is greater than its original price, an Exception should be raised.
    """
 # Check if item's original price or final price was not actually provided
    if item_original_price is None or item_final_price is None:
        raise Exception("Item's original price or final price was not provided.")
    
    # Round the input prices
    item_original_price = round(item_original_price, 2)
    item_final_price = round(item_final_price, 2)
    
    # Check if the final price of the item is greater than its original price
    if item_final_price > item_original_price:
        raise Exception("The final price of the item is greater than its original price.")
    
    # Calculate and return the savings
    return round(item_original_price - item_final_price, 2)

def calculate_fulfilment_surcharge(fulfilment_type: FulfilmentType, customer: Customer) -> float:
    """
    Currently, a fulfilment surcharge is only applicable for deliveries. There is no surcharge applied in any other case.
    The fulfilment surcharge is calculated as $5 or $0.50 for every kilometre, whichever is greater.
    Surcharge value returned should have at most two decimal places.
    If a fulfilment type was not actually provided, an Exception should be raised.
    Delivery fulfilment type can only be used if the customer has linked their member account to the transaction, and if delivery distance is specified in their member profile.
    Otherwise, a FulfilmentException should be raised.
    """
   # Check if fulfilment type is provided
    if fulfilment_type is None:
        raise Exception("Fulfilment type not provided.")
    
    # If the fulfilment type is PICKUP
    if fulfilment_type == FulfilmentType.PICKUP:
        return 0.0
    
    # If the fulfilment type is DELIVERY
    if fulfilment_type == FulfilmentType.DELIVERY:
        
        # Check if customer object and delivery distance are provided
        if customer is None or customer.delivery_distance_km is None or customer.delivery_distance_km == 0:
            raise FulfilmentException("Delivery not possible. Customer or delivery distance information is missing.")
        
        # Calculate surcharge
        distance_based_surcharge = customer.delivery_distance_km * 0.50
        surcharge = max(5.0, distance_based_surcharge)
        
        return round(surcharge, 2)  # Rounding to 2 decimal places

######## Second

def round_off_subtotal(subtotal: float, payment_method: PaymentMethod) -> float:
    """
    Currently, subtotal rounding is only applicable when paying by cash.
    There is no rounding performed in any other case.
    If the subtotal value or payment method was not actually provided, an Exception should be raised.
    The subtotal is rounded off to the nearest multiple of 5 cents. Surcharge value returned should have at most two decimal places.
    Cent amounts which have their ones-place digit as 1 - 2 or 6 - 7 will be rounded down. If it is 3 - 4 or 8 - 9, it will be rounded up instead.
    As the (monetary) subtotal value is provided as a float, ensure that it is first rounded off to two decimal places before doing the rounding.
    """
    # Check if both subtotal and payment_method are provided
    if subtotal is None or payment_method is None:
        raise Exception("Both subtotal and payment method must be provided.")
    
    # Round off the subtotal to two decimal places initially
    subtotal = round(subtotal, 2)
    
    if payment_method != PaymentMethod.CASH:
        return subtotal
    
    # Convert the subtotal to cents to make it easier to work with
    cents = int(subtotal * 100)
    
    # Find the remainder when dividing by 5
    rem = cents % 5
    
    # Apply the rounding rules
    if rem in [1, 2, 6, 7]:
        cents -= rem
    elif rem in [3, 4, 8, 9]:
        cents += (5 - rem)
    
    # Convert the subtotal back to dollars and cents
    new_subtotal = cents / 100.0
    return round(new_subtotal, 2)

def checkout(transaction: Transaction, items_dict: Dict[str, Tuple[Item, int, Optional[int]]], discounts_dict: Dict[str, Discount]) -> Transaction:
    """
    This method will need to utilise all of the seven methods above.
    As part of the checkout process, each of the transaction lines in the transaction should be processed.
    If a transaction object, items dictionary or discounts dictionary was not actually provided, an Exception should be raised.
    All items in the transaction should be checked against any restrictions, available stock levels and purchase quantity limits.
    If a restricted item in the transaction may not be purchased by the customer initiating the transaction, a RestrictedItemException should be raised.
    If an item in the transaction exceeds purchase quantity limits, a PurchaseLimitExceededException should be raised.
    If an item in the transaction is of insufficient stock, an InsufficientStockException should be raised.
    All of the transaction lines will need to be processed in order to calculate its respective final price after applicable discounts have been applied.
    The subtotal, surcharge and rounding amounts, as well as final total, total savings from discounts and total number of items purchased also need to be calculated for the transaction.
    Once the calculations are completed, the updated transaction object should be returned.
    """
    # Validate inputs
    if transaction is None or items_dict is None or discounts_dict is None:
        raise Exception("Transaction object, items dictionary, or discounts dictionary not provided")
        
    # Initialize variables for the transaction
    subtotal = 0
    total_savings = 0
    total_items = 0
    purchased_quantities = {}

    # Go through every transaction line in the transaction object
    for tline in transaction.transaction_lines:
      # Get item details using the item id in the transaction line
      item, _, _ = items_dict.get((tline.item.id), (None, None, None))
          
      # Check if the item exists
      if item is None:
        raise Exception(f"Item with code {item[0]} not found")
          
      # Use existing functions to check restrictions, stock levels, and purchase quantity limits
      if is_not_allowed_to_purchase_item(item, transaction.customer, transaction.date):
        raise RestrictedItemException(f"Restricted item {item.name} cannot be purchased by the customer")
      
      # Get or set the purchased quantity for the item
      purchased_so_far = purchased_quantities.get(item.id, 0)
      new_purchase_amount = purchased_so_far + tline.quantity
      
      purchase_limit = get_item_purchase_quantity_limit(item, items_dict)
      if purchase_limit is not None and new_purchase_amount > purchase_limit:
        raise PurchaseLimitExceededException(f"Purchase limit exceeded for item {item.name}")
      
      # Update purchased quantity for the item
      purchased_quantities[item.id] = new_purchase_amount
      
      if not is_item_sufficiently_stocked(item, new_purchase_amount, items_dict):
        raise InsufficientStockException(f"Insufficient stock for item {item.name}")
          
      # Calculate final item price and savings using existing functions
      final_price = calculate_final_item_price(item, discounts_dict)
      savings = calculate_item_savings(item.original_price, final_price)
          
      # Update transaction line with the final price
      tline.final_cost = final_price* tline.quantity
          
      # Update transaction details
      subtotal += final_price * tline.quantity
      total_savings += savings * tline.quantity
      total_items += tline.quantity
      
    # Calculate the rounded-off subtotal and surcharge using existing functions
    rounded_subtotal = round_off_subtotal(subtotal, transaction.payment_method)
    surcharge = calculate_fulfilment_surcharge(transaction.fulfilment_type, transaction.customer)
      
    # Calculate final total and rounding
    final_total = rounded_subtotal + surcharge
    rounding = rounded_subtotal- subtotal
      
    # Update the transaction object with all the calculated details
    transaction.all_items_subtotal = subtotal
    transaction.fulfilment_surcharge_amount = surcharge
    transaction.rounding_amount_applied = rounding
    transaction.final_total = final_total
    transaction.amount_saved= total_savings
    transaction.total_items_purchased = total_items
      
    return transaction


#### END
