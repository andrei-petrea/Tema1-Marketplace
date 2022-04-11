"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        # maximum number of items per producer
        self.queue_size_per_producer = queue_size_per_producer
        self.cart = list()  # list of carts as dictionaries
        self.marketplace = list()  # list of products as dictionaries
        self.cart_no = 0  # variable used for the cart id
        self.producer_no = 0  # variable used for the producer id
        # variable that keeps track of how many products each producer has published
        self.producer_queue = [0] * 100

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = self.producer_no
        self.producer_no = self.producer_no + 1  # increment for the next producer

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # if the producers queue is full he needs to wait
        if self.producer_queue[producer_id] >= self.queue_size_per_producer:
            return False

        # create a dictionary to hold the info about the product
        product_aux = dict()
        product_aux["producer_id"] = producer_id
        product_aux["product"] = product
        product_aux["in_stock"] = True
        self.producer_queue[producer_id] += 1  # add the product to the queue
        self.marketplace.append(product_aux)  # add the product on the marketplace
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        cart_id = self.cart_no
        self.cart_no = self.cart_no + 1  # increment for the next cart

        return cart_id

    def get_index(self, product):
        """
        Get the index of a certain product in the marketplace

        :returns an int representing the product index or -1
         if the product is not on the marketplace
        """
        for i, dic in enumerate(self.marketplace):
            if dic["product"] == product and dic["in_stock"] is True:
                return i

        return -1

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # get the index of the element from the marketplace
        index = self.get_index(product)

        # if the element is not on the marketplace, wait
        if index == -1:
            return False

        # create a dictionary holding the product in the cart
        product_aux = dict()
        product_aux["cart_id"] = cart_id
        product_aux["product"] = product
        self.cart.append(product_aux)
        self.marketplace[index]["in_stock"] = False  # remove product from the marketplace
        # remove product from the queue
        self.producer_queue[self.marketplace[index]["producer_id"]] -= 1

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # find the product you want to delete from the cart
        for i, _ in enumerate(self.cart):
            if self.cart[i]["cart_id"] == cart_id and self.cart[i]["product"] == product:
                del self.cart[i]
                # stop after deleting one product, otherwise you might delete 2 of the same products
                break

        index = self.get_index(product)
        self.marketplace[index]["in_stock"] = True  # add product on the marketplace
        # add product back to queue
        self.producer_queue[self.marketplace[index]["producer_id"]] += 1

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # list with all the products
        order_list = list()

        # find all the products from a cart and add them to the list
        for _, dic in enumerate(self.cart):
            if dic["cart_id"] == cart_id:
                order_list.append(dic["product"])

        return order_list
