from enum import StrEnum
from typing import Literal, Union

from pydantic import BaseModel, Field, HttpUrl, field_validator


class RecipeStatus(StrEnum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    STALE = "stale"
    DEPRECATED = "deprecated"


class ReviewDecision(StrEnum):
    ACCEPT = "accept"
    REJECT = "reject"
    NARROW_SCOPE = "narrow_scope"
    MERGE_EXISTING = "merge_existing"
    NEEDS_MORE_EVIDENCE = "needs_more_evidence"
    MARK_STALE = "mark_stale"
    DEPRECATE = "deprecate"
    KEEP_SEPARATE = "keep_separate"
    REJECT_DUPLICATE = "reject_duplicate"


class EvidenceRef(BaseModel):
    source_id: str
    url: HttpUrl
    final_url: HttpUrl
    source_type: str
    captured_at: str
    section_anchor: str
    span_id: str
    short_excerpt: str = Field(min_length=1, max_length=600)
    quote_hash: str


class ExtractionProfile(BaseModel):
    content_selectors: list[str] = Field(default_factory=list)
    structured_text_paths: list[str] = Field(default_factory=list)
    min_sections: int = 1
    max_sections: int = 500
    require_expected_hints: bool = True
    agentic_fallback: bool = True


class Source(BaseModel):
    source_id: str
    url: HttpUrl
    source_type: str
    stacks: list[str]
    expected_failure_hints: list[str] = Field(default_factory=list)
    refresh_policy: str = "manual"
    extraction_profile: ExtractionProfile = Field(default_factory=ExtractionProfile)

    @field_validator("source_id")
    @classmethod
    def source_id_must_be_slug(cls, value: str) -> str:
        if not value or any(ch.isspace() for ch in value):
            raise ValueError("source_id must be a non-empty slug")
        return value


class SourceList(BaseModel):
    sources: list[Source]


class EvidenceCandidate(BaseModel):
    failure_label: str
    symptom_quotes: list[str] = Field(default_factory=list)
    cause_quotes: list[str] = Field(default_factory=list)
    avoidance_quotes: list[str] = Field(default_factory=list)
    validation_quotes: list[str] = Field(default_factory=list)
    section_refs: list[str] = Field(default_factory=list)
    confidence: Literal["low", "medium", "high"] = "low"


class EvidenceCandidates(BaseModel):
    candidates: list[EvidenceCandidate]


class ReviewRecord(BaseModel):
    candidate_id: str
    decision: ReviewDecision
    reviewed_at: str
    reviewer: str = "human"
    notes: str = ""


class Maintenance(BaseModel):
    state: RecipeStatus = RecipeStatus.PROPOSED
    stale_reason: list[str] = Field(default_factory=list)
    stale_detected_at: str | None = None


class Recipe(BaseModel):
    id: str
    kind: Literal["debug-recipe"] = "debug-recipe"
    status: RecipeStatus
    stack: list[str]
    failure_class: str
    symptoms: list[str]
    fingerprints: list[str]
    first_checks: list[str]
    do_not: list[str]
    evidence_needed: list[str]
    minimal_fix_scope: list[str]
    validation_ladder: list[str]
    regression_guard: list[str]
    evidence_refs: list[EvidenceRef]
    review: list[ReviewRecord] = Field(default_factory=list)
    maintenance: Maintenance = Field(default_factory=Maintenance)

    @field_validator("evidence_refs")
    @classmethod
    def must_have_evidence_refs(cls, value: list[EvidenceRef]) -> list[EvidenceRef]:
        if not value:
            raise ValueError("recipe core fields require at least one evidence_ref")
        return value


class DecisionOption(BaseModel):
    condition: str
    recommendation: str


class TriggerSpec(BaseModel):
    file_pattern: str = ""
    code_signals: list[str] = Field(default_factory=list)
    description: str = ""


class BuildRecipe(BaseModel):
    id: str
    kind: Literal["build-recipe"] = "build-recipe"
    status: RecipeStatus
    stack: list[str]
    trigger: TriggerSpec = Field(default_factory=TriggerSpec)
    correct_pattern: list[str]
    decision_context: list[DecisionOption] = Field(default_factory=list)
    constraints: list[str]
    do_not: list[str]
    defaults: list[str] = Field(default_factory=list)
    validation: list[str]
    related_debug_recipes: list[str] = Field(default_factory=list)
    evidence_refs: list[EvidenceRef]
    review: list[ReviewRecord] = Field(default_factory=list)
    maintenance: Maintenance = Field(default_factory=Maintenance)

    @field_validator("evidence_refs")
    @classmethod
    def build_must_have_evidence_refs(cls, value: list[EvidenceRef]) -> list[EvidenceRef]:
        if not value:
            raise ValueError("build recipe requires at least one evidence_ref")
        return value


AnyRecipe = Union[Recipe, BuildRecipe]
