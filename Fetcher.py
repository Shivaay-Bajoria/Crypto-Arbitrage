import ccxt.async_support as ccxt
import asyncio

async def fetch(exchange_names, symbol):

    exchanges = []
    for name in exchange_names:
        try:
            exchange = getattr(ccxt, name)
            exchanges.append(exchange())
        except AttributeError:
            print(f"Error-Exchange {name} not found in ccxt library")

    #Creating the tasks but not sending them
    tasks = []
    for exchange in exchanges:
        tasks.append(exchange.fetch_ticker(symbol))

    results = []
    try:
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for exchange, response in zip(exchanges, responses):
            if isinstance(response, Exception):
                print(f"Error-Error Fetching {exchange.id}: {response}")
            else:
                results.append({
                    'Exchange': exchange.id,
                    'Symbol': symbol,
                    'Bid': response['bid'],
                    'Ask': response['ask'],
                })
    finally:
        for exchange in exchanges:
            await exchange.close()

    return results


