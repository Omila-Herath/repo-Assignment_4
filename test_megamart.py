import unittest
import megamart

class TestMegaMart(unittest.TestCase):

  def test_checkout_public_sample(self):
    item1 = (megamart.Item('1', 'Tim Tam - Chocolate', 4.50, ['Confectionery', 'Biscuits']), 20, None)

    items_dict = {
      '1': item1,
    }

    discounts_dict = {}

    transaction = megamart.Transaction('02/08/2023', '12:00:00')

    transaction.transaction_lines = [
      megamart.TransactionLine(item1[0], 2),
    ]

    transaction.payment_method = megamart.PaymentMethod.CASH
    transaction.fulfilment_type = megamart.FulfilmentType.PICKUP

    checkedout_transaction = megamart.checkout(transaction, items_dict, discounts_dict)
    self.assertEqual(checkedout_transaction.total_items_purchased, 2)
    self.assertEqual(checkedout_transaction.fulfilment_surcharge_amount, 0.00)
    self.assertEqual(checkedout_transaction.all_items_subtotal, 9.00)
    self.assertEqual(checkedout_transaction.rounding_amount_applied, 0.00)
    self.assertEqual(checkedout_transaction.final_total, 9.00)
    self.assertEqual(checkedout_transaction.amount_saved, 0.00)

  def test_checkout_private(self):
    item1 = (megamart.Item('1', 'Tim Tam - Chocolate', 4.50, ['Confectionery', 'Biscuits']), 20, None)
    item2 = (megamart.Item('2', 'Beer', 16.00, ['Alcohol']), 12, 2)
    item3 = (megamart.Item('3', 'Laundry Detergent', 9.98, ['Household', 'Cleaning']), 5, None)

    items_dict = {
      '1': item1,
      '2': item2,
      '3': item3,
    }
    item_dict_none = {'1': (None, None, None)}
    discounts_dict = {}

    transaction = megamart.Transaction('02/08/2023', '12:00:00')
    transaction2 = megamart.Transaction('02/08/2023', '12:00:00')
    transaction2.customer = megamart.Customer('789', 'Carol', None, False, 15)
    transaction3 = megamart.Transaction('02/08/2023', '12:00:00')
    transaction3.customer = megamart.Customer('123', 'Alice', '01/08/2003', True, None)
    transaction4 = megamart.Transaction('02/08/2023', '12:00:00')
    transaction4.customer = transaction3.customer
    transaction.transaction_lines = [megamart.TransactionLine(item1[0], 2)]
    transaction2.transaction_lines = [megamart.TransactionLine(item2[0], 13)]
    transaction3.transaction_lines = [megamart.TransactionLine(item2[0], 15)]
    transaction4.transaction_lines = [megamart.TransactionLine(item3[0], 15)]
    transaction.payment_method = megamart.PaymentMethod.CASH
    transaction.fulfilment_type = megamart.FulfilmentType.PICKUP

    checkedout_transaction = megamart.checkout(transaction, items_dict, discounts_dict)
    self.assertEqual(checkedout_transaction.total_items_purchased, 2)
    self.assertEqual(checkedout_transaction.fulfilment_surcharge_amount, 0.00)
    self.assertEqual(checkedout_transaction.all_items_subtotal, 9.00)
    self.assertEqual(checkedout_transaction.rounding_amount_applied, 0.00)
    self.assertEqual(checkedout_transaction.final_total, 9.00)
    self.assertEqual(checkedout_transaction.amount_saved, 0.00)

    with self.assertRaises(Exception):
      megamart.checkout(None, items_dict, discounts_dict)
    with self.assertRaises(Exception):
      megamart.checkout(transaction2, items_dict, discounts_dict)
    with self.assertRaises(Exception):
      megamart.checkout(transaction2, item_dict_none, discounts_dict)
    with self.assertRaises(Exception):
      megamart.checkout(transaction3, items_dict, discounts_dict)
    with self.assertRaises(Exception):
      megamart.checkout(transaction4, items_dict, discounts_dict)

    
  def test_is_not_allowed_to_purchase_item(self):

    # Data block for is_not_allowed_to_purchase_item testing
    itemAllowed = (megamart.Item('1', 'Tim Tam - Chocolate', 4.50, ['Confectionery', 'Biscuits']))
    itemRestricted = (megamart.Item('2', 'Beer', 4.50, ['Alcohol']))
    customerOldVerified = megamart.Customer('456', 'Bob', '01/08/2001', True, 21)
    customerYoungVerified = megamart.Customer('123', 'Alice', '01/08/2008', True, None)
    customerOldUnverified = megamart.Customer('789', 'Carol', '01/08/2001', False, 15)
    customerYoungUnverified = megamart.Customer('789', 'Carol', '01/08/2008', False, 15)
    purchaseDateValid = '01/08/2023'
    purchaseDateInvalid = '2019-08-01'
    customerDobInvalid = megamart.Customer('456', 'Bob', '01-08-2001', True, 21)

    #Check all permutations of customer age, verification status, and item restrictions
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemRestricted,customerOldVerified,purchaseDateValid), False)
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemRestricted,customerYoungVerified,purchaseDateValid), True)
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemRestricted,customerOldUnverified,purchaseDateValid), True)
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemRestricted,customerYoungUnverified,purchaseDateValid), True)
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemAllowed,customerOldVerified,purchaseDateValid), False)
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemAllowed,customerYoungVerified,purchaseDateValid), False)
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemAllowed,customerOldUnverified,purchaseDateValid), False)
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemAllowed,customerYoungUnverified,purchaseDateValid), False)
    self.assertEqual(megamart.is_not_allowed_to_purchase_item(itemRestricted,customerYoungVerified,None), True)
    #Check for all possible exceptions
    with self.assertRaises(Exception):
      megamart.is_not_allowed_to_purchase_item(None,customerOldVerified,purchaseDateValid)
    with self.assertRaises(Exception):
      megamart.is_not_allowed_to_purchase_item(None,None,None)
    with self.assertRaises(Exception):
      megamart.is_not_allowed_to_purchase_item(itemRestricted,customerDobInvalid,purchaseDateValid)
    with self.assertRaises(Exception):
      megamart.is_not_allowed_to_purchase_item(itemRestricted,customerOldVerified,purchaseDateInvalid)
    with self.assertRaises(Exception):
      megamart.is_not_allowed_to_purchase_item(itemRestricted,customerDobInvalid,purchaseDateInvalid)

  def test_get_item_purchase_quantity_limit(self):
    # Data block for test_get_item_purchase_quantity_limit testing
    itemNoLimit = (megamart.Item('1', 'Tim Tam - Chocolate', 4.50, ['Confectionery', 'Biscuits']))
    itemLimit = (megamart.Item('2', 'Coffee Powder', 16.00, ['Coffee', 'Drinks']))
    itemRandom = (megamart.Item('99', 'Something', 16.00, ['Coffee', 'Drinks']))
    itemDict = {
      '1': (itemNoLimit, 20, None),
      '2': (itemLimit, 12, 2),
    }

    #Check all permutations of item purchase quantity limits and itemDict
    self.assertEqual(megamart.get_item_purchase_quantity_limit(itemNoLimit, itemDict), None)
    self.assertEqual(megamart.get_item_purchase_quantity_limit(itemLimit, itemDict), 2)
    self.assertEqual(megamart.get_item_purchase_quantity_limit(itemRandom, itemDict), None)
    
    #Check for all possible exceptions
    with self.assertRaises(Exception):
      megamart.get_item_purchase_quantity_limit(None, itemDict)
    with self.assertRaises(Exception):
      megamart.get_item_purchase_quantity_limit(itemRandom, None)
    with self.assertRaises(Exception):
      megamart.get_item_purchase_quantity_limit(None, None)

  def test_is_item_sufficiently_stocked(self):
    #Data block for test_is_item_sufficiently_stocked testing
    itemSufficient = (megamart.Item('1', 'Tim Tam - Chocolate', 4.50, ['Confectionery', 'Biscuits']), 20, None)
    itemInsufficient = (megamart.Item('2', 'Coffee Powder', 16.00, ['Coffee', 'Drinks']), 12, 2)
    itemNone = (megamart.Item('3', 'Something', 16.00, ['Coffee', 'Drinks']), None, None)
    ItemNegativeStock = (megamart.Item('4', 'Something', 16.00, ['Coffee', 'Drinks']), -1, None)
    itemRandom = (megamart.Item('99', 'Random', 16.00, ['Coffee', 'Drinks']), 0, None)
    itemDict = {
      '1': itemSufficient,
      '2': itemInsufficient,
      '3': itemNone,
      '4': ItemNegativeStock,
    }

    #Check all permutations of item purchase quantity and itemDict
    self.assertEqual(megamart.is_item_sufficiently_stocked(itemSufficient[0], 1, itemDict), True)
    self.assertEqual(megamart.is_item_sufficiently_stocked(itemInsufficient[0], 20, itemDict), False)
    self.assertEqual(megamart.is_item_sufficiently_stocked(itemRandom[0], 20, itemDict), False)

    #Check for all possible exceptions
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(None, 1, itemDict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(itemRandom[0], 1, None)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(itemRandom[0], None, itemDict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(None, 1, None)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(itemRandom[0], None, None)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(None, None, itemDict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(None, None, None)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(itemNone[0], 1, itemDict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(itemNone[0], 1, itemDict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(ItemNegativeStock[0], 1, itemDict)
    with self.assertRaises(Exception):
      megamart.is_item_sufficiently_stocked(itemSufficient[0], -1, itemDict)
    

  def test_calculate_final_item_price(self):
    #Data block for test_calculate_final_item_price testing
    itemNoDiscount = (megamart.Item('1', 'Tim Tam - Chocolate', 4.50, ['Confectionery', 'Biscuits']), 20, None)
    itemDiscountPercValid = (megamart.Item('2', 'Coffee Powder', 4.00, ['Coffee', 'Drinks']), 12, 2)
    itemDiscountFlatValid = (megamart.Item('3', 'Something', 16.00, ['Coffee', 'Drinks']), None, None)
    itemDiscountFlatInvalid = (megamart.Item('4', 'Something', 16.00, ['Coffee', 'Drinks']), None, None)
    itemDiscountPercInvalid = (megamart.Item('5', 'Something', 16.00, ['Coffee', 'Drinks']), None, None)
    itemDiscountUnknown = (megamart.Item('6', 'Something', 16.00, ['Coffee', 'Drinks']), None, None)
    disc_dict = {
      '2': megamart.Discount(megamart.DiscountType.PERCENTAGE, 25, '2'),
      '3': megamart.Discount(megamart.DiscountType.FLAT, 1.50, '3'),
      '4': megamart.Discount(megamart.DiscountType.FLAT, -1.5, '4'),
      '5': megamart.Discount(megamart.DiscountType.PERCENTAGE, 0, '5'),
      '6': megamart.Discount(None, 1.50, '6'),
    }

    #Check all permutations of item and discounts_dict
    self.assertEqual(megamart.calculate_final_item_price(itemNoDiscount[0], disc_dict), 4.50)
    self.assertEqual(megamart.calculate_final_item_price(itemDiscountPercValid[0], disc_dict), 3.00)
    self.assertEqual(megamart.calculate_final_item_price(itemDiscountFlatValid[0], disc_dict), 14.50)

    #Check for all possible exceptions
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(None, disc_dict)
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(itemNoDiscount[0], None)
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(None, None)
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(itemDiscountFlatInvalid[0], disc_dict)
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(itemDiscountPercInvalid[0], disc_dict)
    with self.assertRaises(Exception):
      megamart.calculate_final_item_price(itemDiscountUnknown[0], disc_dict)

  def test_calculate_item_savings(self):
    #Data block for test_calculate_item_savings testing
    itemOrignalLarge = 32.00
    itemOrignalSmall = 4.50
    itemFinalLarge = 16.00
    itemFinalSmall = 3.00

    #Check all permutations of original and final item prices
    self.assertEqual(megamart.calculate_item_savings(itemOrignalLarge, itemFinalLarge), 16.00)
    self.assertEqual(megamart.calculate_item_savings(itemOrignalSmall, itemFinalSmall), 1.50)

    #Check for all possible exceptions
    with self.assertRaises(Exception):
      megamart.calculate_item_savings(None, itemFinalLarge)
    with self.assertRaises(Exception):
      megamart.calculate_item_savings(itemOrignalLarge, None)
    with self.assertRaises(Exception):
      megamart.calculate_item_savings(None, None)
    with self.assertRaises(Exception):
      megamart.calculate_item_savings(itemOrignalSmall, itemFinalLarge)

  def test_calculate_fulfilment_surcharge(self):
    #Data block for test_calculate_fulfilment_surcharge testing
    customerNoDist = megamart.Customer('123', 'Alice', '01/08/2008', True, None)
    customerNormal = megamart.Customer('456', 'Bob', '20/04/2010', True, 2)
    customerZeroDist = megamart.Customer('123', 'Alice', '01/08/2008', True, 0)

    #Check all permutations of customer and fulfilment type
    self.assertEqual(megamart.calculate_fulfilment_surcharge(megamart.FulfilmentType.PICKUP, customerNormal), 0.00)
    self.assertEqual(megamart.calculate_fulfilment_surcharge(megamart.FulfilmentType.DELIVERY, customerNormal), 5.00)
    
    #Check for all possible exceptions
    with self.assertRaises(Exception):
      megamart.calculate_fulfilment_surcharge(None, customerNormal)
    with self.assertRaises(Exception):
      megamart.calculate_fulfilment_surcharge(megamart.FulfilmentType.DELIVERY, None)
    with self.assertRaises(Exception):
      megamart.calculate_fulfilment_surcharge(None, None)
    with self.assertRaises(Exception):
      megamart.calculate_fulfilment_surcharge(megamart.FulfilmentType.DELIVERY, customerNoDist)
    with self.assertRaises(Exception):
      megamart.calculate_fulfilment_surcharge(megamart.FulfilmentType.DELIVERY, customerZeroDist)

  def test_round_off_subtotal(self):
    #Data block for test_round_off_subtotal testing
    subtotalNoRounding = 4.50
    subtotalRoundingDown = 4.51
    subtotalRoundingUp = 4.58

    #Check all permutations of subtotal
    self.assertEqual(megamart.round_off_subtotal(subtotalNoRounding, megamart.PaymentMethod.CASH), 4.50)
    self.assertEqual(megamart.round_off_subtotal(subtotalRoundingDown, megamart.PaymentMethod.CASH), 4.50)
    self.assertEqual(megamart.round_off_subtotal(subtotalRoundingDown, megamart.PaymentMethod.CREDIT), 4.51)
    self.assertEqual(megamart.round_off_subtotal(subtotalRoundingUp, megamart.PaymentMethod.CASH), 4.60)

    #Check for all possible exceptions
    with self.assertRaises(Exception):
      megamart.round_off_subtotal(None, megamart.PaymentMethod.CASH)
    with self.assertRaises(Exception):
      megamart.round_off_subtotal(subtotalNoRounding, None)
    with self.assertRaises(Exception):
      megamart.round_off_subtotal(None, None)

unittest.main()
