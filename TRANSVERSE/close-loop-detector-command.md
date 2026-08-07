---
name: close-loop-detector
description: "Detect semantic loop and force session close if needed"
intent_hash: 0xCLOSE_LOOP_DETECTOR_20260730
---

# close-loop-detector

## Usage
`close-loop-detector [--force]`

- `--force` : force the close even if the loop isn't clearly detected (reserved for emergency cases).  

## Workflow
1. The trigger `session-closeout` automatically invokes this skill at the end of a session.  
2. The skill returns `STOP` / `CONTINUE` with a JSON payload detailing any detected loop.  
3. If the result is `STOP`, the system interrupts the session immediately and creates a follow-up ticket `[#S-YYYYMMDD]` via the ECOS CLI.  

## Options
- `--force` : Skip the normal "CONTINUE" check when a loop is suspected (use only when you are certain a loop exists).  

## Integration
This skill is automatically routed by the **pattern-router** whenever one of the following keywords is detected:
- "détecter boucle sémantique"
- "boucle sémantique"
- "est-ce fini ?"
- "close-loop-detector"

---  

## Example

```bash
# Detect loop and optionally force close
close-loop-detector --force
```