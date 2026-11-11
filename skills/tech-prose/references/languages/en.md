# English technical prose: what reads as machine-written

Companion to SKILL.md. The cross-language patterns live there; this file covers phrasing.

**A single tell proves nothing.** Careful writers make these choices on purpose. Act only when several appear in the same passage, or when one clearly damages accuracy or clarity. Never rewrite a quotation, a title, a proper name, or a passage that discusses the phrase rather than uses it.

## Staging instead of stating

- **Not X, but Y.** `This isn't just a cache — it's a contract.` State the thing once.
- **Arguing with no one.** `While some might argue, the reality is...` Nobody argued. Drop the foil.

## Rhythm by rule

- **Dashes as default connector.** A dash standing in for a period or comma, or letting one sentence run long without a break. Use the period.
- **Repeated sentence openings.** Every item starting with `You can` or `This allows you to`. Vary by rewriting the verb, not by swapping synonyms.

## Inflation

- **Stock words.** `delve`, `seamless`, `robust`, `leverage`, `comprehensive`, `powerful`, `effortless`, `cutting-edge`. Replace with the fact the word was standing in for, or delete.
- **Sales language.** `blazingly fast`, `battle-tested`, `enterprise-grade`. Give the number or drop the adjective.
- **Borrowed authority.** `It's widely recognized that`, `experts agree`. Either cite it or say it directly.
- **Shallow -ing rider.** `..., thereby ensuring reliability.` The clause claims a guarantee the sentence did not establish.
- **Copula avoidance.** `serves as`, `acts as`, `functions as` where `is` would do.
- **Stacked qualifiers.** `a highly scalable, low-latency, fault-tolerant system`. Say which one matters and how you know.
- **Hyphenated pairs everywhere.** `end-to-end, best-in-class, real-time`. Keep only the ones with a fixed technical meaning.

## Formatting by rule

- **Decorative headings.** Headings that announce a topic instead of telling the reader what the section does or concludes. `Overview` is weaker than `How retries behave under load`.
- **Chatbot residue.** `Great question!`, `Let me know if you'd like me to expand this`, `In this article, we will explore`. Delete.

## Writing for the wrong reader

- **Re-explaining what the reader knows.** A paragraph of HTTP background before the one fact the reader came for. Lead with the fact.
- **Writing about the document instead of its subject.** `This section aims to clarify...` Say the clarification.
- **Hedging where a judgment was expected.** `It might possibly be better to consider...` Either recommend it or say why you can't.

## English forms of the SKILL.md patterns

Explanations live in SKILL.md; these are the English shapes.

- Staged run-up: `Before we get to the schema, it helps to understand...` — start with the schema.
- One-line closer: a short paragraph after each section restating it — delete it.
- Forced triads: drop the two that only mirror the first; keep all three when each carries different information.
- Decorative bold: whole sentences, or bold standing in for a heading or for emphasis. Bold labels in definition lists, parameter lists and term-first lists are structure, because each one is a lookup key rather than an emphasis substitute.
- Inflated significance: `plays a crucial role in`, `is a testament to`, `marks a significant shift` — usually one ordinary thing.

## Spoken register

Written docs borrow from speech in ways that survive a casual read. The test is whether the phrase means anything outside a conversation.

- **Casual verbs.** `grab` the value, `snag`, `whip up`, `fiddle with`. The test is whether the verb says what happens; idiomatic dev verbs (`bump the version` in a changelog) are fine — don't substitute mechanically.
- **Vague quantity.** `a bunch of`, `a ton of`, `a couple of`. Give the number or the bound; if neither is known, keep the hedge or report the gap — don't invent a figure.
- **Intensifiers.** `super`, `really`, `pretty`, `totally`, `insanely`, `crazy fast`. Give the measurement.
- **Filler.** `basically`, `actually`, `just`, `simply`, `of course`, `obviously`. Delete it; if the sentence survives, the word carried nothing.
- **Slang and idiom.** `ballpark figure`, `back burner`, `hang in there`, `in the weeds`, `brick` a device. Meaning does not survive translation.
- **Internet shorthand.** `tl;dr`, `ymmv`, `fwiw`. Write it out.
- **Cutesy register.** `oops`, `uh-oh`, `whoops`, `ta-da`, `magic`, `secret sauce`. Say what happened.
- **Exclamation marks and emoji.** Not in technical prose.

**Contractions and second person are not this.** `don't`, `you're`, `you can` are prescribed by Microsoft, Google, and GNOME for tutorials and procedures. Keep them. The target is conversational, not colloquial.

## Punctuation

- Serial comma in lists of three or more: `logs, metrics, and traces`.
- Em dash takes no surrounding spaces; en dash for ranges (`1–9`); hyphen only inside compound words.
- No space before punctuation, one space after. Chinese sentences follow `zh.md` for their own punctuation.
- Number plus unit: `10 MB`, `5 s`, but `80%` and `30°` attach directly.

## Where to stop

The goal is a text a person would write, not a text with the personality removed. Keep:

- A specific, unusual detail that carries information (a real limit, an odd workaround, a measured number).
- A stated opinion where the document type allows one.
- Uncertainty that reflects real uncertainty (`usually succeeds`, `may be up to 30 seconds old`).
- Mixed assessment: `this is fine for reads and risky for writes` is more useful than a balanced-sounding non-statement.

Do not add sentence variety for its own sake. If every sentence is short and clear, that is the correct result, not a defect.
