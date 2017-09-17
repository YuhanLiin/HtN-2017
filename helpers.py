def pluralize(word):
    return word + 'es' if word.endswith('s') or word.endswith('ch') else word + 's'

def pluralize_all(words):
    return [pluralize(word) for word in words]

def verbs_to_3rd(words):
    out = []
    for word in words:
        if word == 'have':
            word = 'has'
        else:
            word = pluralize(word)
        out.append(word)
    return out

pronoun_subj_to_obj = {
    'I': ['me', 'us'], 
    'you': ['you', 'y\'all'],
    'we': ['me', 'us'],
    'y\'all': ['you', 'y\'all'],
    'he': ['him'],
    'she': ['her'],
    'they': ['them'],
    'it': ['it']
}
pronoun_to_self = {
    'I': 'myself', 
    'you': 'yourself',
    'he': 'himself',
    'she': 'herself',
    'they': 'themselves',
    'it': 'itself',
    'we': 'ourselves',
    'y\'all': 'yourselves'
}

# Return self version of pronoun object if there is a subj/obj conflict (he-him, I-me)
def resolve_pronouns(subj, obj):
    if obj in pronoun_subj_to_obj.get(subj, []):
        return pronoun_to_self[subj]
    return obj

# Prevents phrases like "I hit me" and "He hit him" by returning function that replace object with the "self" version
# s and o are indices of subject and verb in word list
def replace_pronouns(s, o):
    def replacer (words): 
        words[o] = resolve_pronouns(words[s], words[o])
    return replacer

def replace_you(o):
    def replacer(words):
        words[o] = resolve_pronouns('you', words[o])
        words[o] = resolve_pronouns('y\'all', words[o])
    return replacer

def deleteIf(a, match, b):
    def deleter(words):
        if (words[a] in match): words[b] = ''
    return deleter