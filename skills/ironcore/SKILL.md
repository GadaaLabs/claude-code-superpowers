---
name: ironcore
description: State machines, ISRs, RTOS, hardware abstraction, and timing analysis — domain expertise for electrical and embedded systems engineers
type: domain
---

# Embedded Systems Patterns

## Overview

**IRONCORE** — *Iron is hard, precise, and unforgiving — exactly like embedded systems.*
When invoked: assesses hardware context (bare-metal / RTOS / HAL / ISR), loads the relevant pattern file, and enforces embedded discipline — deterministic timing, ISR safety, lock-free queues, type-safe register access.


**Core principle:** Embedded systems have zero margin for error — timing violations, race conditions, and memory corruption cause real-world failures. Design for determinism and verifiability.

**Announce at start:** "Running IRONCORE for embedded systems patterns."

---

## Entry Point — First 5 Minutes

```
HARDWARE CONTEXT ASSESSMENT:

"What platform and RTOS?"
A) Bare-metal (no RTOS) — Cortex-M, AVR, PIC
B) FreeRTOS / Zephyr / ThreadX
C) Linux embedded (Yocto, Buildroot)
D) FPGA / HDL
E) Mixed (Linux + MCU co-processor)

"What is failing or being designed?"
1) State machine / control flow
2) ISR / interrupt handling
3) RTOS task design / scheduling
4) Hardware register / peripheral driver
5) Timing / real-time requirements
6) Communication protocol (SPI, I2C, UART, CAN)
7) Memory / stack corruption
```

**Context → Section mapping:**
- Any + 1 → State Machine Design (patterns/state-machines.md)
- Any + 2 → ISR Safety Rules (patterns/isr-safety.md)
- B + 3 → RTOS Task Decomposition (patterns/rtos-tasks.md)
- Any + 4 → Hardware Register Abstraction (patterns/hardware-abstraction.md)
- Any + 5 → Deadline Analysis (patterns/rtos-tasks.md — WCRT section)
- Any + 7 → Stack Size Estimation + run `hunter`

**Critical first question for ALL embedded work:**
"Is this hard real-time (missed deadline = failure) or soft real-time (missed deadline = degraded performance)?"

---

## State Machine Design

Load patterns: **`patterns/state-machines.md`**

Required elements:
1. **HSM structure** — entry/exit actions, parent states for hierarchy
2. **Transition table** — explicit (from, event, to, action) rows — no implicit transitions
3. **Guard conditions** — typed guards, not raw conditionals inside handlers
4. **Tests** — transition coverage, no unreachable states

Rule: **All events must be handled in all states** (even if the handler is explicit ignore).

---

## ISR Safety Rules

Load patterns: **`patterns/isr-safety.md`**

Non-negotiable rules:
1. **Minimal ISR work** — read hardware register, push to buffer, set flag. Nothing else.
2. **volatile for all ISR-shared variables** — compiler cannot cache these
3. **Memory barriers** — `__DMB()` before setting flags, before reading data
4. **Lock-free queues for ISR→main** — SPSC queue, no mutex (mutexes block ISRs)
5. **No malloc/free in ISRs** — ever

---

## RTOS Task Decomposition

Load patterns: **`patterns/rtos-tasks.md`**

Steps:
1. **Identify tasks** by rate: control loop, communication, UI, logging
2. **Assign priorities** by rate monotonic: shorter period = higher priority
3. **Verify schedulability**: Σ(WCET/period) ≤ n(2^(1/n)−1) (for n=3: ≤ 0.78)
4. **Measure stack usage** with watermark pattern, add 25% margin
5. **Choose IPC** — queue for data, semaphore for events, mutex for shared resources

**Priority inversion:** Always use `xSemaphoreCreateMutex()` (has priority inheritance), never binary semaphore for resource protection.

---

## Hardware Register Abstraction

Load patterns: **`patterns/hardware-abstraction.md`**

Required:
1. **Type-safe register structs** — volatile fields, bitfield macros (REG_SET/GET/MASK)
2. **MMIO safety** — NULL check, alignment check, `__DMB()` after writes
3. **Endianness macros** — HTONS/HTONL/NTOHS/NTOHL for all network/protocol data
4. **Timing checklist** — clock freq, setup/hold times, interrupt latency, watchdog timeout

---

## Red Flags

**Never:**
- Do blocking operations in ISR
- Share ISR↔main data without volatile
- Use malloc/free in ISRs or time-critical code
- Ignore stack overflow potential
- Skip deadline analysis for hard real-time tasks

**Always:**
- Use memory barriers for ISR-main communication
- Verify RMS utilization bound before deploying
- Test state machines for unreachable states
- Validate MMIO access bounds
- Document timing requirements and verify them

---

## Integration with Superpowers

| Skill | Integration |
|-------|-------------|
| `forge` | Write hardware-in-loop tests first |
| `hunter` | Debug timing violations, race conditions |
| `sentinel` | Verify timing budgets before claiming success |
| `chronicle` | Store hardware-specific patterns |

---

## Final Checklist

- [ ] State machine has no unreachable states
- [ ] ISR does minimal work (deferred processing used)
- [ ] Lock-free data structures for ISR-main communication
- [ ] Memory barriers in place
- [ ] RMS utilization bound verified (≤ 0.78 for 3 tasks)
- [ ] Stack sizes validated with watermark + 25% margin
- [ ] WCRT analysis passes for all tasks
- [ ] MMIO access validated and bounded
- [ ] Endianness handled correctly
- [ ] Timing requirements documented and verified
