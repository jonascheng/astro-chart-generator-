# Specification Refinement Summary

**Date**: 2025-12-01
**Focus Areas**: FR-005, SC-003, Constraints (Font)
**Status**: ✅ COMPLETE

## Overview

This document records the refinements made to the feature specification, implementation plan, and data model following the `/speckit.analyze` review. Three high-priority ambiguities were resolved.

---

## Refinements Applied

### 1. FR-005: Aspect Definition Gap → RESOLVED ✅

**Original Ambiguity**:
> "The system MUST draw aspect lines for major aspects (e.g., 90°, 120°, 180°)."

**Issue**: No explicit list of which aspects qualify as "major" or orb tolerance ranges.

**Resolution**: Updated `spec.md` FR-005 to define exact aspect types and orb tolerances:

```
- **Conjunction** (0°): ±8°
- **Sextile** (60°): ±6°
- **Square** (90°): ±8°
- **Trine** (120°): ±8°
- **Opposition** (180°): ±8°
```

**Impact on Tasks**:
- T013: D3.js rendering logic now has explicit criteria for drawing aspect lines
- Test acceptance criteria now have measurable thresholds

**Reference**: Standard astrological orb tolerances; Sextile uses ±6° (tighter) due to weaker aspect strength.

---

### 2. SC-003: Accuracy Baseline → RESOLVED ✅

**Original Ambiguity**:
> "The system correctly calculates and displays planet and house positions with 100% accuracy against a trusted third-party astrology calculation library."

**Issues**:
- No baseline library specified
- "100% accuracy" is unmeasurable and not achievable in practice
- No tolerance defined

**Resolution**: Updated `spec.md` SC-003 to specify baseline and tolerance:

```
The system correctly calculates and displays planet and house positions
with a maximum tolerance of ±0.01° longitude difference when compared
against the Swiss Ephemeris (reference baseline).
```

**Impact on Tasks**:
- T007: Calculation implementation now has explicit accuracy target
- T020 (validation phase): Can verify accuracy against Swiss Ephemeris reference
- Integration tests can validate against known reference ephemeris data

**Rationale**: ±0.01° is the practical limit of visual precision in a 2D chart visualization and aligns with Swiss Ephemeris accuracy.

---

### 3. Constraints: Font Clarification → RESOLVED ✅

**Original Constraint**:
> "[NEEDS CLARIFICATION: The exact font used in the reference image is unknown and needs to be identified or a visually similar open-source alternative must be selected.]"

**Resolution**: Referenced `research.md` Section 1 and updated `plan.md` Constraints:

```
Font Selection: Traditional Chinese text uses Source Han Serif (思源宋體)
for a traditional serif feel; Latin characters and numerals use Source Han Sans
for readability and modern aesthetics. Both are open-source and provide full
Traditional Chinese coverage.
```

**Impact on Tasks**:
- T019: Stylistic adjustments can now reference specific font families
- T004 (i18n setup): Font stack can be configured in CSS before implementation
- Frontend CSS dependencies now specified (no external CDN required)

**Rationale**: Decision sourced from `research.md` (Section 1) where fonts were already chosen to match the reference image aesthetic.

---

### 4. FR-007: Error Handling Clarification → ENHANCED ✅

**Original Text**:
> "The system MUST provide feedback if the user inputs invalid birth data."

**Enhancement**: Updated `spec.md` FR-007 with specificity:

```
When invalid birth data is provided (invalid date, missing location,
invalid timezone), the system MUST display a clear, actionable error
message in Traditional Chinese at the point of error. Error messages
shall provide specific guidance (e.g., "請選擇有效的出生地點" for invalid location).
```

**Impact on Tasks**:
- T020: Error handling now has explicit scope and language requirements
- Can be promoted from Phase 4 to Phase 2 if needed (no longer deferred)
- Translation file (T005) now has specific error message keys to include

---

### 5. Data Model Consistency → RESOLVED ✅

**Original Issue**: `Point` object in `data-model.md` lacked `degree` and `minute` fields, but spec required these for the positions table.

**Resolution**: Updated `data-model.md`:
- Added `degree` (Number) field to `Point` object
- Added `minute` (Number) field to `Point` object
- Updated example JSON payload to include these fields for all four points (Ascendant, Descendant, MC, IC)

**Before**:
```json
"points": [
  {
    "name": "Ascendant",
    "longitude": 153.25,
    "sign": "Virgo"
  }
]
```

**After**:
```json
"points": [
  {
    "name": "Ascendant",
    "longitude": 153.25,
    "sign": "Virgo",
    "degree": 3,
    "minute": 15
  }
]
```

**Impact on Tasks**:
- T006: Pydantic models now have consistent field structure for planets and points
- T014 (PositionsTable component): Can uniformly render degree/minute for all bodies

---

## Updated Artifact States

| Artifact | Changes | Status |
|----------|---------|--------|
| `spec.md` | FR-005 (aspects), SC-003 (accuracy), FR-007 (error handling), Key Entities/Data Model clarification | ✅ Updated |
| `plan.md` | Constraints section: font selection resolved | ✅ Updated |
| `data-model.md` | Point object: added degree, minute fields; updated example JSON | ✅ Updated |
| `tasks.md` | No changes (all tasks remain valid) | ✅ Unchanged |

---

## Coverage Impact

| Requirement | Before | After | Tasks Affected |
|-------------|--------|-------|-----------------|
| FR-005 | Ambiguous | Precise (5 aspects, 5 orb ranges) | T013 |
| SC-003 | Unmeasurable | Measurable (±0.01° vs Swiss Ephemeris) | T007, T020 |
| FR-007 | Vague | Specific (languages, error types) | T020 |
| Data Model | Inconsistent | Consistent (all bodies have degree/minute) | T006, T014 |
| Constraints | Unresolved | Resolved (font families specified) | T019 |

---

## Outstanding Items

### Resolved (Previously HIGH-Severity)

- ✅ FR-005 aspect specification
- ✅ SC-003 accuracy baseline
- ✅ Font constraint clarification
- ✅ Data model inconsistency

### Remaining (MEDIUM-Severity, can proceed)

| ID | Item | Recommendation |
|----|------|-----------------|
| U4 | Timezone handling for ambiguous locations | Add geocoding service task (Phase 1) or document as future enhancement |
| C2 | Performance benchmarking (2-second goal) | Add to T020 or create T021 |
| C3 | Unit/integration test coverage for new code | Add test tasks after T007, T013 |
| C4 | Swiss Ephemeris data file validation | Add verification step to T003 |

---

## Validation Checklist

- [x] FR-005: Aspects are now explicitly defined with orb tolerances
- [x] SC-003: Accuracy requirement is measurable and baselined
- [x] Constraints: Font selection is resolved and documented
- [x] Data Model: Points now include degree/minute fields
- [x] FR-007: Error handling requirements are specific
- [x] All changes align with Constitutional Principles I–V
- [x] All changes maintain backward compatibility with existing tasks

---

## Next Steps

### Before `/speckit.implement`:

1. ✅ Specification refinements complete
2. ⏳ **OPTIONAL**: Run `/speckit.plan --force-refresh` to regenerate plan with refined spec
3. ⏳ **OPTIONAL**: Run `/speckit.tasks --force-refresh` to regenerate tasks with refined requirements

### For Implementation Phase:

1. Reference `data-model.md` when creating Pydantic models in T006
2. Use FR-005 aspect list when implementing T013 (aspect line drawing)
3. Use SC-003 tolerance when validating T007 (calculation accuracy)
4. Use FR-007 specific error messages when implementing T020 (error handling)
5. Ensure fonts from constraints are loaded in T004 (i18n/CSS setup)

---

## Sign-Off

**Refinement Status**: ✅ COMPLETE AND VALIDATED

All three focus areas (FR-005, SC-003, Constraints) have been clarified and integrated into the specification, plan, and data model. The feature is now ready for implementation phase without remaining ambiguities on these items.

**Ready for**: `/speckit.implement` or `/speckit.plan --force-refresh`
