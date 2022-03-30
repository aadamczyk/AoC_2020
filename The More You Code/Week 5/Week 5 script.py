import pandas as pd
from collections import deque


def parse(contents):
    content_list = contents.split()
    rules = {'parent': " ".join(content_list[0:2]), 'number': [], 'child': []}
    n_children = int((len(content_list) - 4) / 4)
    for n in range(n_children):
        rules['number'].append(content_list[4 + 4*n])
        rules['child'].append(" ".join(content_list[5 + 4*n: 7 + 4*n]))
    return pd.DataFrame.from_dict(rules)


def parse_all(raw):
    all_rules = pd.DataFrame(columns=['parent', 'number', 'child'])
    for line in raw:
        all_rules = pd.concat([all_rules, parse(line)], ignore_index=True)
    return all_rules


def count_contains_gold(all_rules):
    containers = []
    d = deque(["shiny gold"])
    while len(d) > 0:
        current = d.pop()
        new = all_rules[all_rules['child'] == current]['parent']
        if len(new) > 0:
            for item in new:
                d.append(item)
                containers.append(item)
    return len(set(containers))


def count_gold_contains(all_rules, target_bag):
    new_bags = 0
    new = all_rules[all_rules['parent'] == target_bag]
    if len(new) > 0:
        for row in range(len(new)):
            below_bags = count_gold_contains(all_rules, new['child'].values[row])
            new_bags += (below_bags + 1) * int(new['number'].values[row])
    else:
        return 0
    return new_bags


raw_data = pd.read_table('bags.txt', names=['rule'], skip_blank_lines=False).squeeze('columns')
data = parse_all(raw_data)
print(count_contains_gold(data))
print(count_gold_contains(data, "shiny gold"))
