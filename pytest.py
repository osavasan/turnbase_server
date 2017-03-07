
from pprint import pprint

def test(room_id, *args, **kwargs):
    order_id = kwargs.get("order_id")
    print("Order ID:"+ order_id)
    print(kwargs)

    return kwargs

result = test(0, [], order_id="1")

pprint(result)