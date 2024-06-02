from itertools import combinations

def apriori(transactions, min_support, min_confidence):
    # Step 1: Generate all frequent 1-itemsets
    item_count = {}
    for transaction in transactions:
        for item in transaction:
            if item in item_count:
                item_count[item] += 1
            else:
                item_count[item] = 1

    # Filter based on min_support
    frequent_itemsets = [{item} for item, count in item_count.items() if count >= min_support]
    support_data = {frozenset({item}): count for item, count in item_count.items() if count >= min_support}

    # Step 2: Generate higher order itemsets
    k = 2
    while True:
        new_candidates = []
        for i in range(len(frequent_itemsets)):
            for j in range(i + 1, len(frequent_itemsets)):
                # Join step
                union_set = frequent_itemsets[i].union(frequent_itemsets[j])
                if len(union_set) == k and union_set not in new_candidates:
                   new_candidates.append(union_set)

        
        # Calculate support for new candidates
        candidate_count = {frozenset(candidate): 0 for candidate in new_candidates}
        for transaction in transactions:
            for candidate in new_candidates:
                if candidate.issubset(transaction):
                    candidate_count[frozenset(candidate)] += 1

        
        # Prune step
        new_frequent_itemsets = [candidate for candidate, count in candidate_count.items() if count >= min_support]
        for itemset in new_frequent_itemsets:
            support_data[frozenset(itemset)] = candidate_count[itemset]
        
        if not new_frequent_itemsets:
            break

        frequent_itemsets.extend(new_frequent_itemsets)
        k += 1

    # Generate association rules
    association_rules = []
    for itemset in support_data:
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = set(antecedent)
                    consequent = itemset - antecedent
                    antecedent_support = support_data[frozenset(antecedent)]
                    rule_support = support_data[itemset]
                    confidence = rule_support / antecedent_support
                    if confidence >= min_confidence:
                        association_rules.append((antecedent, consequent, confidence))

    return list(support_data.items()), association_rules

# Example usage
test_cases = {
    "basic": [
        ['A', 'B', 'C'],
        ['A', 'B', 'D'],
        ['A', 'C', 'D'],
        ['B', 'C', 'E'],
    ],
    "no_frequent_itemsets": [
        ['A', 'B'],
        ['C', 'D'],
        ['E', 'F'],
        # With min_support set to the number of transactions, none should be frequent.
    ],
    "all_single_frequent": [
        ['A'],
        ['A'],
        ['A'],
        # With min_support set to 1, 'A' is always frequent.
    ],
    "large_transactions": [
        ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        ['A', 'C', 'G'],
        ['B', 'F', 'E', 'G'],
        # This should test the scalability with respect to itemset length.
    ],
    "large_num_transactions": [
        *([['A', 'B', 'C', 'D']] * 100),  # 100 identical transactions
        *([['X', 'Y', 'Z']] * 100),  # 100 identical transactions
        # This should test the scalability with respect to the number of transactions.
    ],
    "confidence_testing": [
        ['A', 'B', 'C'],
        ['A', 'B'],
        ['A', 'C'],
        ['A'],
        # With min_confidence set to 0.5, there should be rules like A => B, B => A, etc.
    ],
    "all_combinations_frequent": [
        ['A', 'B'],
        ['B', 'C'],
        ['A', 'C'],
        ['A', 'B', 'C'],
        # With min_support set to 1, all subsets should be frequent.
    ],
    "varying_length": [
        ['A', 'B', 'C', 'D', 'E', 'F'],
        ['A', 'B', 'C'],
        ['A', 'B'],
        ['A'],
        # This will test how well the algorithm handles transactions of different lengths.
    ],
    "duplicate_transactions": [
        ['A', 'B', 'C'],
        ['A', 'B', 'C'],
        ['A', 'B', 'C'],
        # The duplicates should not affect the final counts.
    ],
    "no_association_rules": [
        ['A', 'B', 'C'],
        ['B', 'C', 'D'],
        ['C', 'D', 'E'],
        # With a high min_confidence, there may be no rules that satisfy the threshold.
    ],
}

test_case_parameters = {
    "basic": {"min_support": 2, "min_confidence": 0.6},
    "no_frequent_itemsets": {"min_support": 4, "min_confidence": 0.6},
    "all_single_frequent": {"min_support": 1, "min_confidence": 0.6},
    "large_transactions": {"min_support": 2, "min_confidence": 0.6},
    "large_num_transactions": {"min_support": 50, "min_confidence": 0.6},
    "confidence_testing": {"min_support": 2, "min_confidence": 0.5},
    "all_combinations_frequent": {"min_support": 1, "min_confidence": 0.6},
    "varying_length": {"min_support": 1, "min_confidence": 0.6},
    "duplicate_transactions": {"min_support": 2, "min_confidence": 0.6},
    "no_association_rules": {"min_support": 2, "min_confidence": 1.0},  # set high for no rules
}

for name, transactions in test_cases.items():
    # Fetch the parameters for the current test case
    parameters = test_case_parameters[name]
    min_support = parameters['min_support']
    min_confidence = parameters['min_confidence']

    print(f"Running test case: {name} (Min Support: {min_support}, Min Confidence: {min_confidence})")
    frequent_itemsets, association_rules = apriori(transactions, min_support, min_confidence)

    # Print the frequent itemsets
    print("Frequent Itemsets:")
    for itemset, support in frequent_itemsets:
        print(f"Itemset: {itemset}, Support: {support}")

    # Print the association rules
    print("\nAssociation Rules:")
    for antecedent, consequent, confidence in association_rules:
        print(f"{antecedent} => {consequent}, Confidence: {confidence:.2f}")

    print("\n" + "-" * 50 + "\n")  # Separator for readability between test cases


