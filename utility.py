import sys
import operator
import random
import utility_ref
import time

def preprocess(wizards, num_constraints, constraints):
	mapped_constraint = wizardsmap(wizards,constraints)
	return remove_duplicate(num_constraints, mapped_constraint)

def wizardsmap(wizards, constraints):
    node_map = {k: v for v, k in enumerate(wizards)}
    mapped_constraint = []
    for constraint in constraints:
        wiz_a = constraint[0]
        wiz_b = constraint[1]
        wiz_c = constraint[2]

        mapped_constraint.append([node_map[wiz_a],node_map[wiz_b],node_map[wiz_c]])

    return mapped_constraint

def remove_duplicate(num_constraints, constraints):
    pairs = {}
    for constraint in constraints:
        wiz = [constraint[0],constraint[1]]
        s = frozenset(wiz)

        if len(s) == 1:
            continue
        
        if s in pairs:
            w = constraint[2]
            if w not in pairs[s]:
                pairs[s].append(w) 
                pairs[s] = sorted(pairs[s])
        else:
            pairs[s] = [constraint[2]]

    processed = []
    for p in pairs:
        for c in pairs[p]:
            l = list(p)
            processed.append([l[0],l[1],c])

    processed = sorted(processed,key=operator.itemgetter(0))
    print("We have removed " + str(num_constraints - len(processed)) + " duplicated constraints.")
    return processed

def valid(order, constraints):

    node_map = {k: v for v, k in enumerate(order)}
    for constraint in constraints:
        wiz_a = constraint[0]
        wiz_b = constraint[1]
        wiz_c = constraint[2]

        if (wiz_a in node_map) and (wiz_b in node_map) and (wiz_c in node_map):
             wiz_a = node_map[wiz_a]
             wiz_b = node_map[wiz_b]
             wiz_c = node_map[wiz_c]

             if (wiz_a < wiz_c < wiz_b) or (wiz_b < wiz_c < wiz_a):
                return False

    return True


def possible(order,constraint,condition):

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    if wiz_a in order and wiz_b in order and wiz_c in order:
        index1 = order.index(wiz_a)
        index2 = order.index(wiz_b)
        index3 = order.index(wiz_c)
        if(index1<index3<index2 and index2<index3<index1):
            return [-2]
        else:
            return [-1]
    elif wiz_a in order:
        if wiz_c in order:
            return validated_possible2(order,constraint,condition,wiz_a,wiz_c)
        elif wiz_b in order:
            return validated_possible2(order,constraint,condition,wiz_a,wiz_b)
        else:
            return possible1(order,constraint,wiz_a)
    elif wiz_b in order:
        if wiz_c in order:
            return validated_possible2(order,constraint,condition,wiz_b,wiz_c)
        else:
            return possible1(order,constraint,wiz_b)
    elif wiz_c in order:
        return possible1(order,constraint,wiz_c)
    else:
        print("NOT SUPPOSE TO BE NONRELATED")
        return [] 

# Given an order, there's one matching wizards in the constraint. 
def possible1(order,constraint,wiz):

    collect = []

    print("possible1")

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index = order.index(wiz)

    if wiz == wiz_a or wiz == wiz_b:

        otherwiz = wiz_b if (wiz == wiz_a) else wiz_a

        for i in range(index+1,len(order)+1):
            order1 = order[:]
            order1.insert(i,otherwiz)
            for j in range(0,index+1):
                order2 = order1[:]
                order2.insert(j,wiz_c)
                collect.append(order2)
            for j in range(i+1,len(order1)+1):
                order2 = order1[:]
                order2.insert(j,wiz_c)
                collect.append(order2)

        for i in range(0,index+1):
            order1 = order[:]
            order1.insert(i,otherwiz)
            for j in range(0,i+1):
                order2 = order1[:]
                order2.insert(j,wiz_c)
                collect.append(order2)

            new_index = order1.index(wiz)
            for j in range(new_index+1,len(order1)+1):
                order2 = order1[:]
                order2.insert(j,wiz_c)
                collect.append(order2)

    elif wiz == wiz_c:
        
        for i in range(0,index+1):
            order1 = order[:]
            order1.insert(i,wiz_a)
            for j in range(0,index+2):
                order2 = order1[:]
                order2.insert(j,wiz_b)
                collect.append(order2)

        for i in range(index+1,len(order)+1):
            order1 = order[:]
            order1.insert(i,wiz_a)
            for j in range(index+1,len(order1)+1):
                order2 = order1[:]
                order2.insert(j,wiz_b)
                collect.append(order2)
            
    else:
        print("SOMETHING WENT WRONG")


    return collect

# Given an order, there are two matchings in the constraint
def validated_possible2(order,constraint,condition,wiz1,wiz2):

    collect = []

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    index1 = order.index(wiz1)
    index2 = order.index(wiz2)

    possible_index = []
    otherwiz = None

    if (wiz2 != wiz_c):
        #assert(wiz2 == wiz_b)
        lower = min(index1,index2)
        upper = max(index1,index2)
        possible_index = list(range(0,lower+1)) + list(range(upper+1,len(order)+1))
        otherwiz = wiz_c

    else:
        otherwiz = wiz_b if wiz1 == wiz_a else wiz_a
        if index2 > index1:
            possible_index = list(range(0,index2+1))
        else:
            possible_index = list(range(index2+1,len(order)+1))

    copy_possible_index = possible_index[:]


    for c in condition:

        if possible_index == []:
            return []
        l = len(possible_index)-1
        toadd = c.index(otherwiz)

        for p in possible_index:
            wiz1 = p if toadd == 0 else order.index(c[0])
            wiz2 = p if toadd == 1 else order.index(c[1])
            wiz3 = p if toadd == 2 else order.index(c[2])

            lower = min(wiz1,wiz2)
            upper = max(wiz1,wiz2)

            if lower == wiz3 and c[2] != otherwiz:  
                copy_possible_index.remove(p)
            elif upper == wiz3 and c[2] == otherwiz:
                copy_possible_index.remove(p)
            elif lower < wiz3 < upper:
                copy_possible_index.remove(p)

        possible_index = copy_possible_index[:]
        
    for p in possible_index:
        order1 = order[:]
        order1.insert(p,otherwiz)
        collect.append(order1)

    return collect


def strategy1(num_wizards,wizards,constraints):

    possible_order = []
    remain_constraints = constraints[:]

    counter = 10000

    while(len(remain_constraints) > 0 and counter > 0):

        if num_wizards <= 0:
            break

        collect = variation(remain_constraints[0])
        remain_constraints = remain_constraints[1:]

        while(len(collect[0]) < num_wizards and len(remain_constraints) > 0 and counter > 0):

            new_collect = []
            candidate = find_related(collect[0],remain_constraints)
            # No more related constraints
            if (candidate == []):
                print("No more related constraints! Disjoint Set.")
                print("Number of remain:",len(remain_constraints))
                print(collect[0])
                break

            condition = []
            if len(candidate) == 3:
                wizs = collect[0]+candidate[2]
                condition = find_3_related(wizs,remain_constraints)

            pos = []
            for order in collect:
                pos = possible(order,candidate[0],condition)
                #Invalid order, do not build on 
                if (pos == [-2]):
                    continue
                elif (pos == [-1]):
                    new_collect.append(order)
                elif (pos != []):
                    new_collect.extend(pos)

            del remain_constraints[candidate[1]]

            if (new_collect == []):
                print("Wrong direction")
                return collect[0]
            elif (len(new_collect) > 10000):
                new_collect = new_collect[::2]

            random.shuffle(new_collect)
            collect = new_collect
            counter -= 1
            # s = "\r" + str(len(remain_constraints)) + " " + str(len(collect)) + " " + str(counter)
            # sys.stdout.write(s)
            # sys.stdout.flush()

        counter -= 1
        possible_order.append(collect[0])
        num_wizards -= len(collect[0])

    return sum(possible_order,[])

def find_related(order,constraints):

    candidate2 = []
    candidate1 = []

    for i in range(len(constraints)):
        notmatch = []
        for c in constraints[i]:
            if c not in order:
                notmatch.append(c)
        num = len(notmatch)

        if num == 0:
                return [constraints[i],i]
        elif num == 3:
            continue
        elif num == 1:
            candidate2.append([constraints[i],i,notmatch])
        else:
            candidate1.append([constraints[i],i,notmatch])
        
    if candidate2 == []:
        if candidate1 == []:
            return []
        else:
            return candidate1[0]
    else:
        return candidate2[0]

def find_3_related(wizs,constraints):

    related = []

    for constraint in constraints:
        matches = 0
        for c in constraint:
            if c in wizs:
                matches += 1

        if matches == 3:
            related.append(constraint)

    return related


def variation(constraint):

    wiz_a = constraint[0]
    wiz_b = constraint[1]
    wiz_c = constraint[2]

    return [constraint,[wiz_b,wiz_a,wiz_c],[wiz_c,wiz_a,wiz_b],[wiz_c,wiz_b,wiz_a]]


def strategy2(num_wizards,wizards,constraints):

    possible_order = []

    remain_constraints = {3:constraints[:]}
    factor = 0.5

    while(len(remain_constraints) > 0):

        if num_wizards <= 0:
            break

        currentlayer = 3
        previouslayers = [3]

        collect = {3:variation(remain_constraints[3][0])}
        remain_constraints[3] = remain_constraints[3][1:]
        possible_to_build = []
        current_cons = []

        while(currentlayer < num_wizards and len(remain_constraints) > 0):

            # Remove any empty that's not needed
            curr = time.process_time()
            remove = [layer for layer in collect if collect[layer] == []]
            #print(process_time() - curr)
            for r in remove:
                collect.pop(r)
                remain_constraints.pop(r)
                previouslayers.remove(r)

            current_pos = collect[currentlayer]
            current_cons = remain_constraints[currentlayer]

            #Check relevance 
            notchecking = True
            candidate = find_related(current_pos[0],current_cons)

            condition = []
            if len(candidate) == 2:
                notchecking = False
            elif len(candidate) == 3:
                wizs = current_pos[0]+candidate[2]
                condition = find_3_related(wizs,current_cons)

            # Amount check
            amount = len(current_pos)
            if amount > 1 and notchecking:
                random.shuffle(current_pos)
                while len(possible_to_build) < factor * len(current_pos):
                    possible_to_build.append(current_pos.pop())
                msg = str(previouslayers[0]) + " " + str(currentlayer)
                sys.stdout.write("\r"+msg)
                sys.stdout.flush()
                if factor > 0.0625:
                    factor /= 2
            else:
                possible_to_build = current_pos

                if factor < 0.5:
                    factor *= 2

            # No more related constraints
            if (candidate == []):
                print("No more related constraints! Disjoint Set.")
                print("Number of remain:",len(current_cons))
                print(possible_to_build[0])
                break

            new_collect,pos = [],[]
            while (possible_to_build != []):
                order = possible_to_build.pop()
                pos = possible(order,candidate[0],condition)
                #Invalid order, do not build on 
                if (pos == [-2]):
                    continue
                elif (pos == [-1]):
                    new_collect.append(order)
                elif (pos != []):
                    new_collect.extend(pos)

            if (new_collect == []):
                msg = "Wrong direction " + str(currentlayer) 
                sys.stdout.write("\r" + msg)
                sys.stdout.flush()
                if collect[currentlayer] == []:
                    collect.pop(currentlayer)
                    remain_constraints.pop(currentlayer)
                    previouslayers.pop()
                    currentlayer = previouslayers[-1]
                continue
            
            currentlayer = len(new_collect[0])

            if currentlayer not in previouslayers:
                previouslayers.append(currentlayer)

            collect[currentlayer] = new_collect[:]
            remain = current_cons[:]
            remain_constraints[currentlayer] = remain

            del remain[candidate[1]]
            for c in condition:
                if c in remain:
                    remain.remove(c)

    
            # s = "\r" + str(len(remain_constraints)) + " " + str(len(collect)) + " " + str(counter)
            #sys.stdout.write(s)
            #sys.stdout.flush()

        possible_order.append(collect[currentlayer][0])
        num_wizards -= len(collect[currentlayer][0])
        remain_constraints = {3:current_cons}

    return sum(possible_order,[])

def find_optimizable(constraints):

    remain_constraints = constraints[:]

    pairs = {}
    order = []
    name = []

    for constraint in constraints:
        s = frozenset(constraint)

        if s in pairs:
            c = pairs[s]
            wiz_a = c[2]
            wiz_c = constraint[2]
            wiz_b = c[0] if c[0] != wiz_c else c[1]

            if wiz_a not in name:
                name.append(wiz_a)
            if wiz_b not in name:
                name.append(wiz_b)
            if wiz_c not in name:
                name.append(wiz_c)

            order.append([wiz_a,wiz_b,wiz_c])
            order.append([wiz_c,wiz_b,wiz_a])
        else:
            pairs[s] = constraint

    for constraint in constraints:
        wiz_a = constraint[0]
        wiz_b = constraint[1]
        wiz_c = constraint[2]

        if wiz_a in name and wiz_b in name and wiz_c in name:
            remain_constraints.remove(constraint)

    return order, name, remain_constraints

def optimization1(constraints,full_constraints,wizards):

    remain_constraints = constraints[:]
    collect = [remain_constraints[0],remain_constraints[1]]
    print(collect)
    remain_constraints = remain_constraints[2:]


    while len(remain_constraints) > 0 :

        constraint1 = remain_constraints.pop()
        constraint2 = remain_constraints.pop()

        new_collect = []
        for order in collect:
            pos1 = utility_ref.possible(order,constraint1)
            pos2 = utility_ref.possible(order,constraint2)

            if (pos1 == [-1] or pos2 == [-1]):
                new_collect.append(order)
            else:
                for p in pos1:
                    if valid(p,full_constraints):
                        new_collect.append(p)
                for p in pos2:
                    if valid(p,full_constraints):
                        new_collect.append(p)

        if collect != []:
            print(collect[0],collect[1])
        collect = new_collect

    return collect[0]


















