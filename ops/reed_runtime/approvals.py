from __future__ import annotations

from dataclasses import dataclass

from .spec import load_runtime_spec


@dataclass(frozen=True)
class ApprovalDecision:
    action: str
    tier: str
    allowed_without_approval: bool
    reason: str


def classify_action(action: str) -> ApprovalDecision:
    normalized = action.strip().lower()
    tiers = load_runtime_spec().autonomy_tiers
    for tier_name, actions in tiers.items():
        if normalized in {item.lower() for item in actions}:
            if tier_name == "approval_gated":
                return ApprovalDecision(
                    action=normalized,
                    tier=tier_name,
                    allowed_without_approval=False,
                    reason="Action is explicitly hard-gated in runtime spec.",
                )
            return ApprovalDecision(
                action=normalized,
                tier=tier_name,
                allowed_without_approval=True,
                reason="Action is permitted by current autonomy tier.",
            )
    return ApprovalDecision(
        action=normalized,
        tier="unknown",
        allowed_without_approval=False,
        reason="Action is not classified in runtime spec and must be treated as approval-gated.",
    )
