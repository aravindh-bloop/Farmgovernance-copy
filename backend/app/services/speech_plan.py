"""
Decides what the assistant actually *reads out*, and what it asks next.

A kiosk answer is written to be read on screen: it carries the detail, the
citations and the caveats. Reading all of that aloud produces a lecture that
runs on long after the citizen has stopped listening, and the important first
sentence - the direct answer - is buried under it.

So the voice reads the lead of the answer, and the detail stays on screen to be
read by eye. When the whole answer is short enough, it is simply read in full
and no follow-up is offered, because there is nothing left to ask about.

The follow-up kind is chosen from what the answer already talks about, so the
question is always about something the citizen can actually get: the steps, the
eligibility, the documents, the amount, or the officer. The wording is
localised on the frontend, which already carries all twelve languages.
"""
import re
from typing import Any, Dict, List, Optional

# Everything the voice says when the answer is short enough to just read.
READ_EVERYTHING_UNDER = 420
# Where to stop reading a longer answer. Long enough to carry the direct answer
# and its first supporting point, short enough to finish while attention lasts.
READ_ALOUD_TARGET = 340
# Never read a wall of text, however long the answer.
READ_ALOUD_CEILING = 460

_SENTENCE_END = re.compile(r'(?<=[.!?।॥])\s+')
_WHITESPACE = re.compile(r'[ \t]+')
_BULLET = re.compile(r'^\s*(?:[-*•‣▪]|\d+[.)])\s+', re.MULTILINE)
_EMOJI = re.compile(
    '[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF←-⇿⌀-➿]'
)
_MD = re.compile(r'(\*\*|__|`{1,3}|~~|^\s{0,3}#{1,6}\s+|^\s{0,3}>\s?)', re.MULTILINE)

# A short, multilingual keyword map. Anything not recognised falls through to
# the structural rule below, so an unknown language still gets a sensible offer.
_KIND_KEYWORDS: Dict[str, List[str]] = {
    "steps": [
        "step", "steps", "procedure", "process", "how to apply", "apply by",
        "चरण", "प्रक्रिया", "आवेदन", "कसे", "पायऱ्या",
        "படி", "விள்வை", "எப்படி", "క్రమం", "ప్రక్రియ", "ఎలా",
    ],
    "eligibility": [
        "eligible", "eligibility", "who can", "who is eligible", "criteria",
        "योग्यता", "पात्र", "अर्हता", "అర్హత", "தகுத்துக்கொள்ள",
    ],
    "documents": [
        "document", "documents", "paper", "papers", "proof", "attach",
        "दस्तावेज़", "कागज़", "कागद", "పత్రాలు", "आवण्य",
    ],
    "amount": [
        "amount", "rupee", "rupees", "₹", "deadline", "last date", "due by",
        "राशि", "अंतिम तिथि", "रुपये", "తొలుగ", "பணம்",
    ],
    "contact": [
        "contact", "helpline", "toll free", "office", "officer",
        "अधिकारी", "कार्यालय", "हेल्पलाइन", "कार्यालय",
    ],
}

# Phrases that mean the answer has genuinely run out of things to say, in which
# case a follow-up would be noise.
_NOTHING_MORE = (
    "let me know if", "feel free to ask", "anything else",
    "if you have any other", "would you like me to clarify",
)


def _strip_markdown(text: str) -> str:
    """Flatten the answer into something a voice can pronounce."""
    if not text:
        return ""
    out = _MD.sub(" ", text)
    out = _BULLET.sub("", out)
    out = _EMOJI.sub(" ", out)
    out = out.replace("|", " ")
    out = _WHITESPACE.sub(" ", out)
    return re.sub(r"\s*\n\s*", " ", out).strip()


def split_sentences(text: str) -> List[str]:
    """Split on sentence-ending punctuation, including the Indic danda."""
    parts = [p.strip() for p in _SENTENCE_END.split(text or "") if p and p.strip()]
    return parts or ([text.strip()] if text and text.strip() else [])


def _read_aloud_for(clean: str, sentences: List[str]) -> str:
    """Take the lead of the answer, always ending on a sentence boundary."""
    if len(clean) <= READ_EVERYTHING_UNDER:
        return clean

    picked: List[str] = []
    length = 0
    for sentence in sentences:
        picked.append(sentence)
        length += len(sentence) + 1
        if length >= READ_ALOUD_TARGET:
            break

    spoken = " ".join(picked).strip()

    # A single runaway sentence can overshoot the ceiling on its own. Trim it on
    # a word boundary and close it off, so the voice never trails into nothing.
    if len(spoken) > READ_ALOUD_CEILING:
        spoken = spoken[:READ_ALOUD_CEILING].rsplit(" ", 1)[0].rstrip(",;:")
        spoken += "."

    return spoken


def _choose_follow_up(clean: str, procedure: Optional[Any], domains: Optional[List[str]]) -> Optional[str]:
    """Pick the question the citizen is most likely to want next."""
    lowered = clean.lower()

    # An explicit invitation in the answer is the best possible follow-up, but
    # it is already spoken, so it is only used to suppress our own.
    for phrase in _NOTHING_MORE:
        if phrase in lowered:
            return None

    # A generated resolution procedure is the most concrete next step we have.
    if procedure:
        return "steps"

    scored: List[tuple] = []
    for kind, keywords in _KIND_KEYWORDS.items():
        hits = sum(1 for word in keywords if word in lowered)
        if hits:
            scored.append((hits, kind))
    if scored:
        scored.sort(reverse=True)
        return scored[0][1]

    # Nothing recognisable: offer the procedure, which is always answerable.
    if any(d and "grievance" in str(d).lower() for d in (domains or [])):
        return "steps"
    return "steps"


def build_speech_plan(
    answer: str,
    language: str = "en",
    procedure: Optional[Any] = None,
    active_domains: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Work out the spoken part of a reply and the question to ask next.

    Returns the text the voice should read, whether that was the whole answer,
    and a follow-up kind for the frontend to phrase in the citizen's language.
    """
    clean = _strip_markdown(answer)
    if not clean:
        return {
            "read_aloud": "",
            "read_aloud_is_full": True,
            "follow_up_kind": None,
            "detail_withheld": False,
        }

    sentences = split_sentences(clean)
    read_aloud = _read_aloud_for(clean, sentences)
    is_full = len(read_aloud) >= len(clean) - 2

    follow_up_kind = None if is_full else _choose_follow_up(clean, procedure, active_domains)

    return {
        "read_aloud": read_aloud,
        "read_aloud_is_full": is_full,
        "follow_up_kind": follow_up_kind,
        "detail_withheld": not is_full,
    }
