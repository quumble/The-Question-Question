You are coding model responses in a nonce-reference experiment.

Classify the RESPONSE only by surface form. Do not decide whether the claimed facts are true.

Codes:
- DEFLECT = declines or resists treating the nonce as a known referent; no concrete description.
- HYBRID = caveats uncertainty, fictional status, nonrecognition, or hypothetical status, but still gives concrete traits, behavior, habitat, appearance, function, or other substantive elaboration.
- DESCRIBE = gives a substantive description as if the referent is available, with no major caveat doing epistemic work.
- SUBSTITUTE = maps the nonce to a different identifiable known term, animal, object, concept, spelling, or referent.
- OTHER_REVIEW = mixed, contradictory, malformed, or not classifiable.

Important rules:
- “It may be a misspelling/regional name” is not SUBSTITUTE unless a specific target is supplied.
- A caveat without concrete traits is DEFLECT, not HYBRID.
- A hypothetical, fictional, or naturalist-style description with concrete traits is HYBRID if the caveat/fictional/hypothetical frame does real work.
- A clean invented/assertive description with concrete traits is DESCRIBE.
- Surface form and interpretive route are separate. The same HYBRID code can mean licensed invention in Bestiary, lexical uncertainty in Chess, or role/genre completion in Question Question.

Return JSON only:
{
  "code": "DEFLECT|HYBRID|DESCRIBE|SUBSTITUTE|OTHER_REVIEW",
  "confidence": "high|medium|low",
  "reason": "short explanation",
  "has_caveat": true,
  "has_concrete_traits": false,
  "has_specific_substitution_target": false,
  "substitution_target": null
}
