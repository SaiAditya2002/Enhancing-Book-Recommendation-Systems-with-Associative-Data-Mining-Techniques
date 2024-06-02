enerate_candidates(frequent_itemsets, k):
    candidates = []
    for i in range(len(frequent_itemsets)):
        for j in range(i+1, len(frequent_itemsets)):
            itemset1, tids1 = frequent_itemsets[i]
            itemset2, tids2 = frequent_itemsets[j]
            if itemset1[:k-2] == itemset2[:k-2]:
                candidate = itemset1 + [itemset2[-1]]
                candidate_tids = intersect(tids1, tids2)
                if len(candidate_tids) >= min_support:
                    candidates.append((candidate, candidate_tids))
    return candidates