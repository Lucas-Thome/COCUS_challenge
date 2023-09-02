import asyncio
import random
import datetime

tree = list(range(1, 51))
dirty_basket = []
clean_basket = []

farmers = {"fst_farmer": [], "snd_farmer": [], "trd_farmer": []}
cleaners = {"fst_cleaner": [], "snd_cleaner": [], "trd_cleaner": []}


async def print_lengths():
    while True:
        await asyncio.sleep(1)
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Tree: {len(tree)}, Dirty Basket: {len(dirty_basket)}, Clean Basket: {len(clean_basket)}, Farmers: {len(farmers['fst_farmer'])}, {len(farmers['snd_farmer'])}, {len(farmers['trd_farmer'])}")


async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(print_lengths())

    while tree:
        fruit = random.choice(tree)
        tree.remove(fruit)
        farmer = farmers[random.choice(list(farmers.keys()))]
        farmer.append(fruit)
        await asyncio.sleep(random.uniform(3, 6))
        farmer.remove(fruit)
        dirty_basket.append(fruit)


if __name__ == "__main__":
    asyncio.run(main())
