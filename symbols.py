from grammar import Rule, Many, Production
from helpers import pluralize, resolve_pronouns, replace_pronouns, replace_you

Verb = Rule('move', 'kick', 'hit', 'caress', 'use', 'super punch', 'punch')
Verb3rd = Verb.clone().transform(pluralize)
Adverb = Rule('quickly', 'slowly', 'furiously', 'lovingly')
Noun = Rule('bird', 'dog', 'dinosaur', 'force', 'Masterball')
Adjective = Rule('large', 'tiny', 'crazy', 'psychopathic')
Name = Rule('Dio', 'Lem', 'Hackerman', 'Benny', 'Luke')

NamePhrase = Rule(Production(',', Name))
Subject3rd = Rule(
    Production('the', Many(Adjective, 0, 1), Noun),
    'he', 'she', 'it', Name
)
Subject = Rule(
    'you', 'they', 'we', 'y\'all',
    Production('the', Many(Adjective, 0, 1), Noun.clone().transform(pluralize))
)
Object = Rule(
    'you', 'them', 'us', 'him', 'her', 'y\'all', 'me', Name, 
    Production('the', Many(Adjective, 0, 1), Noun.clone().transform(pluralize)), 
    Production('the', Many(Adjective, 0, 1), Noun)
)

Question = Rule(
    Production('does', Subject3rd, Verb, Object, Many(Adverb, 0, 1), '?').set_pre(replace_pronouns(1, 3)), 
    Production('do', Subject, Verb, Object, Many(Adverb, 0, 1), '?').set_pre(replace_pronouns(1, 3)),
)
Statement = Rule(
    Production(Subject, Many(Adverb, 0, 1), Verb, Object, '.').set_pre(replace_pronouns(0, 3)), 
    Production(Subject3rd, Many(Adverb, 0, 1), Verb3rd, Object, '.').set_pre(replace_pronouns(0, 3)),
)
Command = Rule(
    Production(Verb, Object, Many(Adverb, 0, 1), Many(NamePhrase, 0, 1), '!').set_pre(replace_you(1))
)
Sentence = Rule(
    Statement, Question, Command
).set_post(lambda s: s[0].upper() + s[1:]).set_distr([0.33, 0.33, 0.34])

Novel = Rule(Many(Sentence, 1, 10))


print(Novel.generate())