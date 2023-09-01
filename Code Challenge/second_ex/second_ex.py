import random
import threading
import time

# Create the mutex
mutex = threading.Lock()

# Define the functions
def _collect_fruits(tree, dirty_basket, mutex):
  """Collects fruits from the tree and puts them in the dirty basket."""
  while len(tree) > 0:
    # Acquire the mutex
    mutex.acquire()

    # Remove a fruit from the tree
    fruit = tree.pop()

    # Add the fruit to the dirty basket
    dirty_basket.append(fruit)

    # Release the mutex
    mutex.release()

def _clean_fruits(dirty_basket, clean_basket, mutex):
  """Cleans fruits from the dirty basket and puts them in the clean basket."""
  while len(dirty_basket) > 0:
    # Acquire the mutex
    mutex.acquire()

    # Remove a fruit from the dirty basket
    fruit = dirty_basket.pop()

    # Add the fruit to the clean basket
    clean_basket.append(fruit)

    # Release the mutex
    mutex.release()

# Create the tree, dirty basket, and clean basket
tree = []
dirty_basket = []
clean_basket = []

# Create the farmers and cleaners
farmers = [threading.Thread(target=_collect_fruits, args=(tree, dirty_basket, mutex)) for _ in range(3)]
cleaners = [threading.Thread(target=_clean_fruits, args=(dirty_basket, clean_basket, mutex)) for _ in range(3)]

# Start the farmers and cleaners
for farmer in farmers:
  farmer.start()
for cleaner in cleaners:
  cleaner.start()

# Wait for the farmers and cleaners to finish
for farmer in farmers:
  farmer.join()
for cleaner in cleaners:
  cleaner.join()

# Print the final state of the tree, dirty basket, and clean basket
print("Tree:", tree)
print("Dirty basket:", dirty_basket)
print("Clean basket:", clean_basket)