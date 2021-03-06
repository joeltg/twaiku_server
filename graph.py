from completion import *

end_threshold = 0.5

def path_to_string(path):
    string = ''
    for word in path:
        string += word[0] + ' '
        # if word[1] == 5 or word[1] == 12:
        #     string += '\n'
    return string

def get_limit(distance):
    if distance < 5:
        return 5
    if distance < 12:
        return 12
    return 17

def get_children(path, limit):
    # path is a list of (node, distance, siblings)
    # child is a (node, distance, siblings)
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
            children.append([word, length, words])
    return children

def complete_haiku(path):
    distance = 0
    if len(path) > 0:
        distance = path[-1][1]
    if distance == 17:
        return path
    limit = get_limit(distance)

    children = get_children(path, limit)
    queue = [path + [child] for child in children]

    while len(queue) > 0:
        path = queue.pop()
        print(path_to_string(path))
        distance = path[-1][1]
        if distance == 17:
            context = [w[0] for w in path][-2:]
            end_prob = model.prob('.', context)
            print end_prob
            if end_prob > end_threshold:
                return path
        else:
            limit = get_limit(distance)
            children = get_children(path, limit)
            queue += [path + [child] for child in children]

    print('could not find path')
    if len(path) > 1:
        print('recursing')
        print(path_to_string(path[1:]))
        return complete_haiku(path[1:])
    return []

def complete_line(path, limit):
    if type(path) == str:
        path = path.lower()
        p = []
        total = 0
        for word in path.split(' '):
            total += count_syllables_word(word)
            p.append((word, total))
        path = p
    distance = 0
    if len(path) > 0:
        distance = path[-1][1]
    if distance == limit:
        return path

    queue = [path + [child] for child in get_children(path, limit)]

    while len(queue) > 0:
        path = queue.pop()
        # print(path_to_string(path))
        distance = path[-1][1]
        if distance == limit:
            context = [w[0] for w in path][-2:]
            end_prob = model.prob('.', context)
            if end_prob > end_threshold:
                return path
        else:
            children = get_children(path, limit)
            queue += [path + [child] for child in children]

    print('could not find path')
    if len(path) > 1:
        print('recursing')
        print(path_to_string(path[1:]))
        return complete_line(path[1:], limit)
    return []

def complete(string):
    path = []
    total = 0
    for word in string.split(' '):
        total += count_syllables_word(word)
        path.append((word, total))
    return path_to_string(complete_haiku(path))

# print complete_path([('Shy', 1)])
# print complete_path([('Where', 1)])
