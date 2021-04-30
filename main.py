def is_sentence_in_KB(sentence, KB):
    return sentence in KB.keys()

def get_token(sentence):
    if (sentence[0] == '(') or (sentence[0] == ')') or (sentence[0] == '&') or (sentence[0] == '|') :
        return sentence[0]
    i=0;
    private_sentence = sentence
    while len(private_sentence)!=0 and not((private_sentence[0] == '(') or (private_sentence[0] == ')') or (private_sentence[0] == '&') or (private_sentence[0] == '|')):
        i+=1
        private_sentence = private_sentence[1:]
    return sentence[0:i]

def is_true(sentence, KB):
    token = get_token(sentence)
    if token == '(':
        remaining_sentence = sentence[1:]
        left_value, left_character_used = is_true(remaining_sentence, KB)
        remaining_sentence = remaining_sentence[left_character_used:]
        token = get_token(remaining_sentence)
        if not(token == '&' or token == '|'):
            print("ERROR: illegal operator = {}".format(token))
            exit(1)
        operator = token
        remaining_sentence = remaining_sentence[1:]
        right_value, right_character_used = is_true(remaining_sentence, KB)
        remaining_sentence = remaining_sentence[right_character_used:]
        token = get_token(remaining_sentence)
        if token != ")":
            print("ERROR: found {} instead of ')'".format(remaining_sentence[0]))
            exit(1)
        if len(remaining_sentence)!=1:
            print("ERROR: illegal sentence size")
            exit(1)
        if operator == '&':
            return left_value and right_value, 1+left_character_used+1+right_character_used+1
        elif operator == '|':
            return left_value or right_value, 1+left_character_used+1+right_character_used+1
    if token=='~':
        remaining_sentence = sentence[1:]
        value, character_used = is_true(remaining_sentence, KB)
        return not value, character_used
    elif is_sentence_in_KB(token, KB):
        return True, len(token)
    return False, 0

RC_FAIL = -1
RC_ATOM = 0
RC_TRIPLET = 1

def get_non_operator(sentence):
    i=0;
    private_sentence = sentence
    while len(private_sentence)!=0 and not((private_sentence[0] == '(') or (private_sentence[0] == ')') or (private_sentence[0] == '&')
                                           or (private_sentence[0] == '|') or (private_sentence[0] == '>')):
        i+=1
        private_sentence = private_sentence[1:]
    return sentence[0:i]

def decompose_3(sentence):
    token = get_token(sentence)
    if token == '(':
        remaining_sentence = sentence[1:]
        rc, left, operator, right = decompose_3(remaining_sentence)
        if rc == RC_FAIL:
            return RC_FAIL, None, None, None
        if rc == RC_ATOM:
            left_sentence = left
            remaining_sentence = remaining_sentence[len(left):]
        else: # rc == RC_TRIPLET
            left_sentence='('+left+operator+right+')'
            remaining_sentence = remaining_sentence[len(left)+len(operator)+len(right):]
        token = get_token(remaining_sentence)
        triplet_operator = token
        if not(triplet_operator == '&' or triplet_operator == '|' or triplet_operator == '>'):
            print("ERROR: illegal operator = {}".format(triplet_operator))
            exit(1)
        remaining_sentence = remaining_sentence[1:]
        rc, left, operator, right = decompose_3(remaining_sentence)
        if rc == RC_FAIL:
            return RC_FAIL, None, None, None
        if rc == RC_ATOM:
            right_sentence = left
        else: # rc == RC_TRIPLET
            right_sentence='('+left+operator+right+')'
        return RC_TRIPLET, left_sentence, triplet_operator, right_sentence
    return RC_ATOM, get_non_operator(sentence), None, None

    print("Can't recognize: {}".format(sentence[0]))
    exit(1)

def implication(sentence):
    rc, left, operator, right = decompose_3(sentence)
    if rc == RC_TRIPLET and operator == '>':
        return True, left, right
    return False, left, right


def modus_ponens(sentence, KB):
    is_implication, alpha, beta = implication(sentence)
    if is_implication:
        value, character_used = is_true(alpha,KB)
        if value:
            KB[beta]=1



def and_elimination(sentence,KB):
    rc, alpha_1, operator, alpha_2 = decompose_3(sentence)
    if rc == RC_TRIPLET and operator == '&':
        KB[alpha_1]=1
        KB[alpha_2]=1

def unit_resolution(sentence,KB):
    rc, alpha, operator, beta = decompose_3(sentence)
    if rc == RC_TRIPLET and operator == '|':
        value, character_used = is_true('~'+alpha, KB)
        if value:
            KB[beta]=1


def extend_KB(KB):
    kb_grew=True
    while kb_grew:
        next_KB = KB.copy()
        kb_len=len(KB)
        for sentence in KB.keys():
            modus_ponens(sentence, next_KB)
            and_elimination(sentence, next_KB)
            unit_resolution(sentence, next_KB)
        kb_grew = len(next_KB)>kb_len
        KB=next_KB.copy()
    return KB


KB={}
KB["~S1,1"]=1
KB["~S2,1"]=1
KB["S1,2"]=2
#KB.append("~B1,1")
#KB.append("B2,1")
#KB.append("~B1,2")
KB["(~S1,1>(~W1,1&(~W1,2&~W2,1)))"]=1
KB["(~S2,1>(~W1,1&(~W2,1&(~W2,2&~W3,1))))"]=1
KB["(S1,2>(W1,1|(W2,2|(W1,2|W1,3)))"]=1
KB=extend_KB(KB)
print(KB)


#print(is_true("(a&b)", KB))