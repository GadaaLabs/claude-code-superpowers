---
name: LEGION — Star Topology
description: Hub-and-spoke with independent parallel spokes for batch work with no cross-dependencies
---

# Star (Hub-and-spoke)

**Structure:** Central hub coordinates. Spokes work completely independently. No spoke-to-spoke communication.

**Best for:** Parallel feature development, batch processing, multi-language localization, parallel test suites.

**Use when:**
- All subtasks independent (no dependencies)
- Same operation repeated on different inputs
- No cross-spoke coordination needed

**Don't use when:** Subtasks have dependencies (use Hierarchical), spokes need to collaborate (use Mesh), sequential processing needed (use Ring).

## Prompt Template

```
SWARM TOPOLOGY: Star (Hub-and-spoke)

HUB AGENT:
- Assign independent tasks to spokes
- Track completion status
- Merge results when all complete
- No coordination between spokes needed

SPOKE AGENTS:
- Complete your assigned task independently
- No need to communicate with other spokes
- Report directly to hub when done

INDEPENDENT TASKS:
Spoke 1: <task 1>
Spoke 2: <task 2>
Spoke 3: <task 3>
Spoke 4: <task 4>
```

## Example: Parallel Features

```
Hub: coordinator (track progress, merge results)
Spoke 1: Add user profile page
Spoke 2: Add settings page
Spoke 3: Add dashboard widget
Spoke 4: Add notification system
```
