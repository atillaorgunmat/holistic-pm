# Project Governance

- **Time zone**: Europe/Istanbul
- **Daily summary snapshot**: 21:00 (local)
- **Daily blocker scan**: 09:00 (local)

## Checkpoint Rules

- **Minor tasks** (≤6h): ChatGPT authorized
- **Major tasks** (>6h): User approval required
- **Scope amendments**: User approval mandatory



### Phase-Gate Checklist
- [ ] All tasks in current phase marked **Done** or migrated forward
- [ ] FactLog reviewed; zero open `risk:blocker` issues tagged with current phase
- [ ] Governor comment “PROCEED-PH-<num>” on the related PR

### Disaster Recovery
If GitHub Actions fail for more than 24 h:
1. Run `/scripts/restore_ctx.ps1` locally or in the runner.
2. Open a PR labelled `governance`.
3. Ping ChatGPT with the PR link for review.
