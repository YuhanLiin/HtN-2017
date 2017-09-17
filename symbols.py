from grammar import Rule, Many, Production, maybe
from helpers import pluralize_all, resolve_pronouns, replace_pronouns, replace_you, verbs_to_3rd, deleteIf, \
prevent_collection_repeat, format_quotes
from random import random

# Declarations
Verb, SpeakVerb, Adverb, Noun, Adjective, Name, NamePhrase, Subject3rd, Subject, IfPhrase, WhilePhrase, WhenPhrase, \
Conditional, Question, BasicStatement, Command, Sentence, Novel, Article, ArticlePlural, ObjectSingle, ObjectPlural, \
Statement, Object, Dialogue, Speech, SentenceOrSpeech, SubjectPlural, ObjectMulti, NounPhrase, NounPhraseSingle, \
NounPhrasePlural, PrepPhrase, Preposition = Rule.declare_all(34)

#import pdb; pdb.set_trace()
# Definitions
Verb.define('move', 'kick', 'hit', 'caress', 'shoot', 'programs', 'punch', 'take', 'touch', 'have', 'stroke', 'nibble')
SpeakVerb.define('say', 'cry', 'shout', 'scream', 'laugh', 'whisper', 'mention', 'think', 'scribble')
Adverb.define('quickly', 'slowly', 'furiously', 'lovingly', 'unknowingly', 'happily', 'angrily')
Noun.define('bird', 'dog', 'dinosaur', 'force', 'Masterball', 'alien', 'dude', 'arrow', 'experience', 'demon', 'candy')
Adjective.define('large', 'tiny', 'crazy', 'psychopathic', 'blue', 'ancient', 'sad', 'angry', 'cheerful', 'lit', 'gold')
Name.define('Dio', 'Mr. Goose', 'Hackerman', 'Jojo', 'Luke')
Article.define('the', 'this', 'that', 'this one', 'that one', 'a', 'some')
ArticlePlural.define('the', 'these', 'those', 'many', 'some')
Preposition.define('of', 'from', 'in', 'by', 'with', 'without', 'within', 'inside', 'outside')

NamePhrase.define(Production(',', Name))
NounPhraseSingle.define(Production(Article, Many(Adjective, 0, 1), Noun))
NounPhrasePlural.define(Production(ArticlePlural, Many(Adjective, 0, 1), Noun.clone().transform(pluralize_all)))
NounPhrase.define(NounPhrasePlural, NounPhraseSingle)
PrepPhrase.define(Production(Preposition, NounPhrase))

Subject3rd.define(
    Production(NounPhraseSingle, maybe(PrepPhrase)),
    'he', 'she', 'it', Name
).set_distr(0.3, 0.1, 0.1, 0.2, 0.31)
SubjectPlural.define(
    'you', 'they', 'we', 'y\'all',
    Production(NounPhrasePlural, maybe(PrepPhrase))
).set_distr(0.15, 0.15, 0.15, 0.15, 0.41)
Subject.define(Production(
    SubjectPlural, Many(Production('and', Rule().define(SubjectPlural, Subject3rd)), 0, 2).set_distr(0.7, 0.2, 0.1)
)).add_post(prevent_collection_repeat)

ObjectSingle.define(
    Production(NounPhraseSingle, maybe(PrepPhrase)),
    'you', 'her', 'it', 'me', 'him', Name, 
).set_distr(0.3, 0.1, 0.1, 0.1, 0.1, 0.31)
ObjectPlural.define(
    'you', 'them', 'y\'all', 'us', 
    Production(NounPhrasePlural, maybe(PrepPhrase)),
).set_distr(0.15, 0.15, 0.15, 0.15, 0.41)
ObjectMulti.define(Production(
    ObjectPlural, Many(Production('and', Rule().define(ObjectPlural, ObjectSingle)), 0, 2).set_distr(0.7, 0.2, 0.1)
)).add_post(prevent_collection_repeat)
Object.define(ObjectMulti, ObjectSingle)

IfPhrase.define(
    Production('if', BasicStatement), 
    Production('unless', BasicStatement), 
)
WhenPhrase.define(Production('when', BasicStatement), Production('until', BasicStatement))
WhilePhrase.define(Production('while', BasicStatement), Production('as', BasicStatement))
Conditional.define(
    Production(IfPhrase, maybe(WhilePhrase, 0.7, 0.3), maybe(WhenPhrase, 0.7, 0.3)),
    Production(IfPhrase, maybe(WhenPhrase, 0.7, 0.3), maybe(WhilePhrase, 0.7, 0.3)),
    Production(WhenPhrase, maybe(WhilePhrase, 0.7, 0.3), maybe(IfPhrase, 0.7, 0.3)),
    Production(WhenPhrase, maybe(IfPhrase, 0.7, 0.3), maybe(WhilePhrase, 0.7, 0.3)),
    Production(WhilePhrase, maybe(WhenPhrase, 0.7, 0.3), maybe(IfPhrase, 0.7, 0.3)),
    Production(WhilePhrase, maybe(IfPhrase, 0.7, 0.3), maybe(WhenPhrase, 0.7, 0.3)),
)

Question.define(
    Production(
        maybe(Production(Conditional, ','), 0.7, 0.3), 
        'does', Subject3rd, Verb, Object, Many(Adverb, 0, 1),
        maybe(Conditional, 0.7, 0.3),
    ).add_pre(replace_pronouns(2, 4)).add_pre(deleteIf(3, {'has', 'have'}, 5)), 
    Production(
        maybe(Production(Conditional, ','), 0.7, 0.3), 
        'do', Subject, Verb, Object, Many(Adverb, 0, 1),
        maybe(Conditional, 0.7, 0.3),
    ).add_pre(replace_pronouns(2, 4)).add_pre(deleteIf(3, {'has', 'have'}, 5)),
    Production(
        maybe(Production(Conditional, ','), 0.7, 0.3), 'am', 'I', ObjectSingle, maybe(Conditional, 0.7, 0.3),
    ).add_pre(replace_pronouns(2, 3)),
    Production(
        maybe(Production(Conditional, ','), 0.7, 0.3), 'is', Subject3rd, ObjectSingle, maybe(Conditional, 0.7, 0.3),
    ).add_pre(replace_pronouns(2, 3)),
    Production(
        maybe(Production(Conditional, ','), 0.7, 0.3), 'are', Subject, ObjectMulti, maybe(Conditional, 0.7, 0.3),
    ).add_pre(replace_pronouns(2, 3)),
    "Why", "What is this", 'How the hell'
).set_distr(0.2, 0.2, 0.1001, 0.1, 0.1, 0.1, 0.1)

BasicStatement.define(
    Production(
        Subject, Many(Adverb, 0, 1), Verb, Object,
    ).add_pre(replace_pronouns(0, 3)).add_pre(deleteIf(2, {'has', 'have'}, 1)), 
    Production(
        Subject3rd, Many(Adverb, 0, 1), Verb.clone().transform(verbs_to_3rd), Object,
    ).add_pre(replace_pronouns(0, 3)).add_pre(deleteIf(2, {'has', 'have'}, 1)),
    Production('I', 'am', ObjectSingle),
    Production(Subject, 'are', ObjectMulti).add_pre(replace_pronouns(0, 2)),
    Production(Subject3rd, 'is', ObjectSingle).add_pre(replace_pronouns(0, 2)),
).set_distr(0.38, 0.38, 0.05, 0.1, 0.1
).add_post(
    lambda s: s.replace('it is', 'it\'s').replace('they are', 'they\'re').replace('we are', 'we\'re')
        if random() > 0.5 else s
)
Statement.define(Production(maybe(Production(Conditional, ','), 0.7, 0.3), BasicStatement, maybe(Conditional, 0.7, 0.3)))

Command.define(
    Production(
        maybe(Production(Conditional, ','), 0.7, 0.3), 
        Verb, Object, Many(Adverb, 0, 1), 
        maybe(Conditional, 0.7, 0.3), Many(NamePhrase, 0, 1),
    ).add_pre(replace_you(2)).add_pre(deleteIf(1, {'has', 'have'}, 3))
)

Dialogue.define(
    Production(Sentence),
    Production(Many("muda", 3, 10), 'MUDA!'),
    Production(Many("ora", 3, 10), 'ORA!'),
    Production(Many("ha", 5, 12), '!'),
).add_post(lambda s: s[0].upper() + s[1:]).set_distr(0.4, 0.2, 0.2, 0.2)
DialogueBefore = Dialogue.clone().add_post(lambda s: s.replace('.', ','))
Speech.define(
    Production(Subject, maybe(Adverb), SpeakVerb, '"', Dialogue, '"',),
    Production(Subject3rd, maybe(Adverb), SpeakVerb.clone().transform(verbs_to_3rd), '"', Dialogue, '"',),
    Production('"', DialogueBefore, '"', Subject, SpeakVerb, '.'),
    Production('"', DialogueBefore, '"', Subject3rd, SpeakVerb.clone().transform(verbs_to_3rd), '.'),
).add_post(lambda s: s[0].upper() + s[1:]).add_post(format_quotes)

Sentence.define(
    Production(Statement, Rule().define('.', '!').set_distr(0.71, 0.3)),
    Production(Question, '?'),
    Production(Command, Rule().define('!', '.').set_distr(0.71, 0.3)),
).set_distr(0.5, 0.25, 0.25)

SentenceOrSpeech.define(Sentence, Speech).set_distr(0.61, 0.4).add_post(lambda s: s[0].upper() + s[1:])

Novel.define(Many(SentenceOrSpeech, 1, 10)).add_post(
    lambda s: s.replace(' ,', ',').replace(' .', '.').replace(' !', '!').replace(' ?', '?')
)
