from collections import defaultdict
from itertools import combinations

def eclat(transactions, min_support):
    # Step 1: Convert transactions to vertical data format
    vertical_data = defaultdict(list)
    for tid, transaction in enumerate(transactions):
        for item in transaction:
            vertical_data[item].append(tid)

    # Step 2: Get frequent single-item itemsets
    frequent_itemsets = []
    for item, tids in vertical_data.items():
        support = len(tids)
        if support >= min_support:
            frequent_itemsets.append(([item], tids))
    print(frequent_itemsets)
    answer=[]
    answer.extend(frequent_itemsets)
    # Step 3: Generate frequent itemsets
    k = 2
    while True:
        candidates = generate_candidates(frequent_itemsets, k)
        answer.extend(candidates)
        if not candidates:
            break
        frequent_itemsets = candidates
        print(frequent_itemsets)
        k += 1

    return answer, vertical_data


def generate_candidates(frequent_itemsets, k):
    candidates = []
    itemsets = [itemset for itemset, _ in frequent_itemsets]
    for itemset_pair in combinations(itemsets, 2):
        itemset1, itemset2 = itemset_pair
        union_itemset = set(itemset1) | set(itemset2)
        if len(union_itemset) == k:
            candidate = list(set(sorted(union_itemset)))
            if candidate not in [itemset for itemset, _ in candidates]:
                tids1 = [tids for itemset, tids in frequent_itemsets if itemset == itemset1][0]
                tids2 = [tids for itemset, tids in frequent_itemsets if itemset == itemset2][0]
                candidate_tids = intersect(tids1, tids2)
                if len(candidate_tids) >= min_support:
                    candidates.append((candidate, candidate_tids))
    return candidates

# def generate_candidates(frequent_itemsets, k):
#     candidates = []
#     for i in range(len(frequent_itemsets)):
#         for j in range(i+1, len(frequent_itemsets)):
#             itemset1, tids1 = frequent_itemsets[i]
#             itemset2, tids2 = frequent_itemsets[j]
#             if set(itemset1[:k-2]) == set(itemset2[:k-2]):
#                 candidate = sorted(list(set(itemset1) | set(itemset2)))
#                 candidate_tids = intersect(tids1, tids2)
#                 if len(candidate_tids) >= min_support:
#                     candidates.append((candidate, candidate_tids))
#     return candidates

# def generate_candidates(frequent_itemsets, k):
#     candidates = []
#     for i in range(len(frequent_itemsets)):
#         for j in range(i+1, len(frequent_itemsets)):
#             itemset1, tids1 = frequent_itemsets[i]
#             itemset2, tids2 = frequent_itemsets[j]
#             if itemset1[:k-2] == itemset2[:k-2]:
#                 candidate = itemset1 + [itemset2[-1]]
#                 candidate_tids = intersect(tids1, tids2)
#                 if len(candidate_tids) >= min_support:
#                     candidates.append((candidate, candidate_tids))
#     return candidates

def intersect(tids1, tids2):
    return [tid for tid in tids1 if tid in tids2]

def generate_association_rules(frequent_itemsets, vertical_data, min_confidence):
    association_rules = []
    for itemset, tids in frequent_itemsets:
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = list(antecedent)
                    consequent = [item for item in itemset if item not in antecedent]
                    antecedent_tids = set([tid for item in antecedent for tid in vertical_data[item]])
                    itemset_tids = set(tids)
                    confidence = len(itemset_tids) / len(antecedent_tids)
                    if confidence >= min_confidence:
                        association_rules.append((antecedent, consequent, confidence))
    return association_rules

# Example usage
transactions = [
    ['A', 'B', 'C'],
    ['A','B', 'C', 'D'],
    ['A', 'C', 'D'],
    ['A', 'D', 'E'],
    ['A', 'B', 'C', 'D']
]
min_support = 3
min_confidence = 0.6

frequent_itemsets, vertical_data = eclat(transactions, min_support)
association_rules = generate_association_rules(frequent_itemsets, vertical_data, min_confidence)

# Print the frequent itemsets
print("Frequent Itemsets:")
for itemset, tids in frequent_itemsets:
    print(f"Itemset: {itemset}, Support: {len(tids)}")

# Print the association rules
print("\nAssociation Rules:")
cnt=0
for antecedent, consequent, confidence in association_rules:
    print(f"{cnt}::{antecedent} => {consequent}, Confidence: {confidence:.2f}")
    cnt+=1

# Print the vertical data
print("\nVertical Data:")
for item, tids in vertical_data.items():
    print(f"Item: {item}, Transaction IDs: {tids}")