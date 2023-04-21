from django.test import TestCase

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from nltk.tree import Tree
from itertools import permutations
import json

@require_GET
def paraphrase(request):
    tree_str = request.GET.get('tree')
    limit = int(request.GET.get('limit', 20))

    # Parse the tree string into an NLTK Tree object
    tree = Tree.fromstring(tree_str)

    # Find all NP subtrees and collect their daughter NPs
    np_daughters = []
    for np in tree.subtrees(lambda t: t.label() == 'NP'):
        np_daughters.extend([d for d in np if d.label() == 'NP'])

    # Generate permutations of the NP daughter nodes
    permutations_list = list(permutations(np_daughters))

    # Generate paraphrased trees for each permutation
    paraphrased_trees = []
    for permutation in permutations_list[:limit]:
        # Replace the daughter nodes in the original tree with the current permutation
        new_tree = tree.copy(deep=True)
        np_index = 0
        for np in new_tree.subtrees(lambda t: t.label() == 'NP'):
            for i in range(len(np)):
                if np[i].label() == 'NP':
                    np[i] = permutation[np_index]
                    np_index += 1

        # Convert the tree back to a string and add it to the list of paraphrased trees
        paraphrased_trees.append(str(new_tree))
        

    # Return the list of paraphrased trees as a JSON response
    return JsonResponse(paraphrased_trees, safe=False)

    
