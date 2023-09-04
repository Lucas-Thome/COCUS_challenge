import asyncio
import random
import datetime
import sys

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
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Tree: {len(tree)} - Dirty Basket: {len(dirty_basket)} - Clean Basket: {len(clean_basket)} - Farmers: {len(farmers['fst_farmer'])}, {len(farmers['snd_farmer'])}, {len(farmers['trd_farmer'])} - Cleaners: {len(cleaners['fst_cleaner'])}, {len(cleaners['snd_cleaner'])}, {len(cleaners['trd_cleaner'])}"
        )
        await asyncio.sleep(1)


async def farmers_task():
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


async def cleaners_task():
    while True:
        if len(dirty_basket) > 0:
            fruit = dirty_basket.pop()
            #cleaner = cleaners[cleaner_name]
            cleaner = cleaners[random.choice(list(cleaners.keys()))]
            cleaner.append(fruit)
            await asyncio.sleep(random.uniform(2,4))
            cleaner.remove(fruit)
            clean_basket.append(fruit)
        else:
            await asyncio.sleep(1)


async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(print_lengths())

    # Create tasks for farmers
    farmer_tasks = [loop.create_task(farmers_task()) for _ in range(len(farmers.keys()))]

    # Create tasks for cleaners
    cleaner_tasks = [loop.create_task(cleaners_task()) for _ in range(len(cleaners.keys()))]

    global stop_execution
    while True:
        if len(tree) == 0 and len(dirty_basket) == 0 and len(clean_basket) == 50:
            stop_execution = True
            break
        await asyncio.sleep(1)

    for task in asyncio.all_tasks():
        if task != asyncio.current_task():
            print('All the fruits were collected and cleaned.')
            sys.exit(1)

    await asyncio.gather(*asyncio.all_tasks())


if __name__ == "__main__":
    asyncio.run(main())
