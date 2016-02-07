from syllables import count_syllables_word
from oxford import get_candidates
from completion import *

def path_to_string(path):
    return ' '.join([word[0] for word in path])

def get_limit(distance):
    if distance < 5:
        return 5
    if distance < 12:
        return 12
    return 17

'''
def get_children(path, limit):
    # path is a list of (node, distance)
    # child is a (node, distance)
    # all distances are cumulative
    distance = 0
    if len(path) > 0:
        distance = path[-1][1]
    candidates = get_candidates(path_to_string(path))
    children = []
    for candidate in candidates:
        word = candidate['word']
        syllables = count_syllables_word(word)
        length = distance + syllables
        if length <= limit:
            children.append((word, length))
    return children
'''

def get_children(path, limit):
    # path is a list of (node, distance)
    # child is a (node, distance)
    # all distances are cumulative
    distance = 0
    if len(path) > 0:
        distance = path[-1][1]
    words = get_next_words(path)
    children = []
    for word in words:
        syllables = count_syllables_word(word)
        length = distance + syllables
        if length <= limit:
            children.append((word, length))
    return children

def complete_path(path):
    distance = 0
    if len(path) > 0:
        disance = path[-1][1]
    if distance == 17:
        return path
    limit = get_limit(distance)

    queue = [path + [child] for child in get_children(path, limit)]

    while len(queue) > 0:
        path = queue.pop()
        print(path_to_string(path))
        distance = path[-1][1]
        if distance == 17:
            context = [w[0] for w in path][-2:]
            end_prob = model.prob('.', context)
            if end_prob > 0.1:
                return path
        else:
            limit = get_limit(distance)
            children = get_children(path, limit)
            queue += [path + [child] for child in children]

    print('could not find path')
    if len(path) > 1:
        print('recursing')
        print(path_to_string(path[1:]))
        return complete_path(path[1:])
    return []

# print complete_path([('Shy', 1)])
# print complete_path([('Where', 1)])