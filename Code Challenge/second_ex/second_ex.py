import asyncio
import random
import datetime

tree = list(range(1, 51))
dirty_basket = []
clean_basket = []

farmers = {"fst_farmer": [], "snd_farmer": [], "trd_farmer": []}
cleaners = {"fst_cleaner": [], "snd_cleaner": [], "trd_cleaner": []}

# Semaphore to control farmer access to the tree
farmer_semaphore = asyncio.Semaphore(1)

# Flag to control execution
stop_execution = False


async def print_lengths():
    while not stop_execution:
        print(
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Tree: {len(tree)}, Dirty Basket: {len(dirty_basket)}, Clean Basket: {len(clean_basket)}, Farmers: {len(farmers['fst_farmer'])}, {len(farmers['snd_farmer'])}, {len(farmers['trd_farmer'])} - Cleaners: {len(cleaners['fst_cleaner'])}, {len(cleaners['snd_cleaner'])}, {len(cleaners['trd_cleaner'])}"
        )
        await asyncio.sleep(1)


async def farmer_behavior():
    while tree:
        async with farmer_semaphore:
            if len(tree) > 0:
                fruit = random.choice(tree)
                tree.remove(fruit)
                farmer = farmers[random.choice(list(farmers.keys()))]
                farmer.append(fruit)
                await asyncio.sleep(random.uniform(3, 6))
                farmer.remove(fruit)
                dirty_basket.append(fruit)


async def cleaner_behavior(cleaner_name):
    while True:
        if len(dirty_basket) > 0:
            fruit = dirty_basket.pop()
            cleaner = cleaners[cleaner_name]
            cleaner.append(fruit)
            await asyncio.sleep(random.uniform(2, 4))
            cleaner.remove(fruit)
            clean_basket.append(fruit)
        else:
            await asyncio.sleep(1)


async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(print_lengths())

    # Create tasks for farmer behavior
    farmer_tasks = [loop.create_task(farmer_behavior()) for _ in range(3)]

    # Create tasks for cleaner behavior
    cleaner_tasks = [loop.create_task(cleaner_behavior(name)) for name in cleaners.keys()]

    global stop_execution
    while True:
        if len(tree) == 0 and len(dirty_basket) == 0 and len(clean_basket) == 50:
            stop_execution = True
            break
        await asyncio.sleep(1)

    for task in asyncio.all_tasks():
        if task != asyncio.current_task():
            task.cancel()

    await asyncio.gather(*asyncio.all_tasks())


if __name__ == "__main__":
    asyncio.run(main())
