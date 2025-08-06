# Stage-Based Execution Enhancement - viki Configuration Management

## Problem Statement

Users rely on filename-based ordering (00.vk.yaml, 01.vk.yaml) to control execution sequence. This creates pain points:

- Manual file renaming when inserting new steps
- Maintenance overhead when reordering operations
- Unclear intent from numeric filename prefixes

**Current Implementation**: Files processed via `glob()` without guaranteed order, requiring users to use numbered filename conventions.

## Solution Overview

Add optional `stage` field to control execution order:

```yaml
viki:
  stage: 2  # New field controlling execution order (default: 0)
  vars:
    hostname: "VK_VAR_hostname"
  mods:
    mkdir:
      docker:
        path: "~/docker"
```

**Execution**: Sort configurations by `stage` field before merging.

### Key Benefits
- Declarative execution order in configuration files
- Backward compatible (files without `stage` default to 0)
- No file renaming required to reorder operations

## Implementation

**Minimal Changes**: Enhance existing `__load_config` method to sort by stage before merging.

**Core Logic**:
1. Load all configurations with stage information (default stage 0)
2. Sort by stage number
3. Merge in stage order using existing logic

**Configuration Schema**: Add optional `stage` integer field (default: 0).

## Usage Example

**Before (filename-based)**:
```
00.vk.yaml  # Setup directories
01.vk.yaml  # Download files
02.vk.yaml  # Configure services
```

**After (stage-based)**:
```yaml
# setup.vk.yaml
viki:
  stage: 1
  mods:
    mkdir:
      docker:
        path: "~/docker"

# downloads.vk.yaml
viki:
  stage: 2
  mods:
    wget:
      compose-file:
        path: "~/docker"
        url: "https://example.com/docker-compose.yml"
```

## Backward Compatibility

**Zero Breaking Changes**: Files without `stage` field default to stage 0. Existing configurations work unchanged.

## Implementation Plan

**Scope**: 4-6 hours development time

### Tasks
- [ ] Modify `__load_config` method to sort by stage field
- [ ] Add stage field parsing (default to 0)
- [ ] Test with existing configurations
- [ ] Update documentation

### Quality Requirements
- [ ] Stages execute in numeric order
- [ ] Files without stage field default to stage 0
- [ ] Existing configurations work unchanged
- [ ] No performance regression

## Success Metrics

**Technical Success**:
- 100% existing configurations work unchanged
- No performance regression
- Implementation adds <20 lines of code

**User Value**:
- Eliminate file renaming for execution order changes
- Clear declarative execution sequence

## Out of Scope

**Explicitly Excluded**:
- Stage dependencies or conditional logic
- Stage enable/disable functionality
- Parallel execution
- Stage-specific logging or error handling

This enhancement provides maximum user value with minimal implementation complexity - a simple sorting mechanism that eliminates filename-based ordering pain points.
