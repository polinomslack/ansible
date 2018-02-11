#!/usr/bin/env python

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

list_of_inventories = ['/home/cmgmtuser/git/infrastructure/ansible/inventories/live/live','/home/cmgmtuser/git/infrastructure/ansible/inventories/stage/stage','/home/cmgmtuser/git/infrastructure/ansible/inventories/qa/qa',]

def uniql(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

loader = DataLoader()

inventory = InventoryManager(
    loader = loader,
    sources = list_of_inventories
)

a=uniql(inventory.hosts.values())
for i in a: print i