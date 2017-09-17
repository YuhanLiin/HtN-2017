from grammar import Rule, Many, Production, maybe
from helpers import pluralize_all, resolve_pronouns, replace_pronouns, replace_you, verbs_to_3rd, deleteIf
from random import random

# Declarations
Verb, Verb3rd, Adverb, Noun, Adjective, Name, NamePhrase, Subject3rd, Subject, Object, IfPhrase, WhilePhrase, WhenPhrase, \
Conditional, Question, BasicStatement, Command, Sentence, Novel, Article, ArticlePlural, ObjectSingle, ObjectPlural, \
Statement = Rule.declare_all(24)

#import pdb; pdb.set_trace()
# Definitions
Verb.define('move', 'kick', 'hit', 'caress', 'use', 'super-punch', 'punch', 'take', 'make', 'have')
Verb3rd = Verb.clone().transform(verbs_to_3rd)
Adverb.define('quickly', 'slowly', 'furiously', 'lovingly')
Noun.define('bird', 'dog', 'dinosaur', 'force', 'Masterball', 'alien')
Adjective.define('large', 'tiny', 'crazy', 'psychopathic')
Name.define('Dio', 'Lem', 'Hackerman', 'Benny', 'Luke')
Article.define('the', 'this', 'that', 'this one', 'that one', 'a', 'some')
ArticlePlural.define('the', 'these', 'those', 'all these', 'all those', 'many', 'some')

NamePhrase.define(Production(',', Name))
Subject3rd.define(
    Production(Article, Many(Adjective, 0, 1), Noun),
    'he', 'she', 'it', Name
)
Subject.define(
    'you', 'they', 'we', 'y\'all',
    Production(ArticlePlural, Many(Adjective, 0, 1), 
        Noun.clone().transform(pluralize_all)
    )
)
ObjectSingle.define('you', 'her', 'it', 'me', 'him', Name, Production(Article, Many(Adjective, 0, 1), Noun))
ObjectPlural.define(
    'you', 'them', 'y\'all', 'us', 
    Production(ArticlePlural, Many(Adjective, 0, 1), Noun.clone().transform(pluralize_all))
)
Object.define(ObjectPlural, ObjectSingle)

IfPhrase.define(Production('if', BasicStatement), Production('only if', BasicStatement), Production('if and only if', BasicStatement))
WhenPhrase.define(Production('when', BasicStatement),)
WhilePhrase.define(Production('while', BasicStatement), Production('as', BasicStatement))
Conditional.define(
    Production(IfPhrase, maybe(WhilePhrase), maybe(WhenPhrase)),
    Production(IfPhrase, maybe(WhenPhrase), maybe(WhilePhrase)),
    Production(WhenPhrase, maybe(WhilePhrase), maybe(IfPhrase)),
    Production(WhenPhrase, maybe(IfPhrase), maybe(WhilePhrase)),
    Production(WhilePhrase, maybe(WhenPhrase), maybe(IfPhrase)),
    Production(WhilePhrase, maybe(IfPhrase), maybe(WhenPhrase)),
)

Question.define(
    Production(
        maybe(Production(Conditional, ',')), 
        'does', Subject3rd, Verb, Object, Many(Adverb, 0, 1),
        maybe(Conditional),
    ).add_pre(replace_pronouns(2, 4)).add_pre(deleteIf(3, {'has', 'have'}, 5)), 
    Production(
        maybe(Production(Conditional, ',')), 
        'do', Subject, Verb, Object, Many(Adverb, 0, 1),
        maybe(Conditional),
    ).add_pre(replace_pronouns(2, 4)).add_pre(deleteIf(3, {'has', 'have'}, 5)),
    Production(
        maybe(Production(Conditional, ',')), 'am', 'I', ObjectSingle, maybe(Conditional),
    ).add_pre(replace_pronouns(2, 3)),
    Production(
        maybe(Production(Conditional, ',')), 'is', Subject3rd, ObjectSingle, maybe(Conditional),
    ).add_pre(replace_pronouns(2, 3)),
    Production(
        maybe(Production(Conditional, ',')), 'are', Subject, ObjectPlural, maybe(Conditional),
    ).add_pre(replace_pronouns(2, 3)),
).set_distr(0.3, 0.3, 0.1001, 0.15, 0.15)

BasicStatement.define(
    Production(
        Subject, Many(Adverb, 0, 1), Verb, Object,
    ).add_pre(replace_pronouns(0, 3)).add_pre(deleteIf(2, {'has', 'have'}, 1)), 
    Production(
        Subject3rd, Many(Adverb, 0, 1), Verb3rd, Object,
    ).add_pre(replace_pronouns(0, 3)).add_pre(deleteIf(2, {'has', 'have'}, 1)),
    Production('I', 'am', ObjectSingle),
    Production(Subject, 'are', ObjectPlural).add_pre(replace_pronouns(0, 2)),
    Production(Subject3rd, 'is', ObjectSingle).add_pre(replace_pronouns(0, 2)),
).set_distr(0.3, 0.3, 0.1001, 0.15, 0.15
).add_post(
    lambda s: s.replace('it is', 'it\'s').replace(' is', '\'s').replace('they are', 'they\'re').replace('we are', 'we\'re')
        if random() > 0.5 else s
)
Statement.define(Production(maybe(Production(Conditional, ',')), BasicStatement, maybe(Conditional)))

Command.define(
    Production(
        maybe(Production(Conditional, ',')), 
        Verb, Object, Many(Adverb, 0, 1), 
        maybe(Conditional), Many(NamePhrase, 0, 1),
    ).add_pre(replace_you(2)).add_pre(deleteIf(1, {'has', 'have'}, 3))
)
Sentence.define(
    Production(Statement, Rule().define('.', '!').set_distr(0.71, 0.3)),
    Production(Question, '?'),
    Production(Command, '!'),
).add_post(lambda s: s[0].upper() + s[1:]).set_distr(1, 0, 0)

Novel.define(Many(Sentence, 1, 10)).add_post(
    lambda s: s.replace(' ,', ',').replace(' .', '.').replace(' !', '!').replace(' ?', '?')
)


print(Novel.generate())