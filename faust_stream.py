import faust

app = faust.App('naver.finance.board', broker='http://49.50.174.75:9092')

class Order(faust.Record):
    account_id: str
    amount: int

@app.agent(value_type=Order)
async def order(orders):
    async for order in orders:
        # process infinite stream of orders.
        print(f'Order for {order.account_id}: {order.amount}')

# data sent to 'clicks' topic sharded by URL key.
# e.g. key="http://example.com" value="1"
click_topic = app.topic('clicks', key_type=str, value_type=int)

# default value for missing URL will be 0 with `default=int`
counts = app.Table('click_counts', default=int)

@app.agent(click_topic)
async def count_click(clicks):
    async for url, count in clicks.items():
        counts[url] += count

# Order is a json serialized dictionary,
# having these fields:

class Order(faust.Record):
    account_id: str
    product_id: str
    price: float
    quantity: float = 1.0

orders_topic = app.topic('orders', key_type=str, value_type=Order)

@app.agent(orders_topic)
async def process_order(orders):
    async for order in orders:
        # process each order using regular Python
        total_price = order.price * order.quantity
        await send_order_received_email(order.account_id, order)