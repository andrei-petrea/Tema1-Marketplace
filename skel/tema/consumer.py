"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()  # generating a new id for each cart
            for ops in cart:  # for each operation in a cart do something
                i = 0
                while i < ops["quantity"]:  # adding or removing products based on quantity
                    if ops["type"] == "add":
                        if self.marketplace.add_to_cart(cart_id, ops["product"]):
                            i = i + 1  # if element was added, go to next one
                        else:
                            time.sleep(self.retry_wait_time)  # if element was not added wait
                    else:
                        # remove and element from the cart, the element exists in the cart
                        self.marketplace.remove_from_cart(cart_id, ops["product"])
                        i = i + 1

            # print the list of products at the end
            products = self.marketplace.place_order(cart_id)
            for product in products:
                print(f'{self.name} bought {product}')
