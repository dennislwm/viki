# State Management Improvements

## Problem
State files store raw command output (33KB+) with embedded passwords instead of useful data. Cannot detect server changes or compare configurations.

## Core Issues
1. **Unparseable Output**: Raw strings like `"[sudo] password for user: CONTAINER ID..."`
2. **No Change Detection**: Cannot tell if server state changed
3. **Missing Metadata**: No timestamps or server identification
4. **File Size**: 33KB for simple docker container list

## Cost Impact
Teams spend 2-4 hours weekly manually parsing state files that should provide instant server status.

## Solution
Store command success/failure status and timestamps instead of raw output.

### Minimal Changes Required
1. **Replace raw output** with success status and basic counts
2. **Add timestamps** for change detection  
3. **Remove sensitive data** (no more embedded sudo prompts)

### New State Format
```json
{
  "viki": {
    "captured_at": "2025-08-06T10:30:45Z",
    "hostname": "qemu-vm-ubuntu-dev",
    "data": {
      "docker": {
        "home": {
          "success": true,
          "container_count": 9,
          "captured_at": "2025-08-06T10:30:45Z"
        }
      }
    }
  }
}
```

### Benefits
- **2KB vs 33KB**: 94% file size reduction
- **Change Detection**: Compare timestamps and counts
- **No Passwords**: Clean state files
- **Readable**: Human-parseable JSON structure

## Implementation
**Time Required**: 2-3 days (1 developer)

### Code Changes
1. **Modify `FetchResponse.fetch()`**: Extract basic metrics from command output instead of storing raw strings
2. **Update `CliRequest.write_state()`**: Add timestamp and hostname to state JSON
3. **Enhance `PlanResponse`**: Compare timestamps to detect changes

### Quick Wins
- **Docker commands**: Count containers instead of storing full output
- **DF commands**: Extract disk usage percentage only  
- **LS commands**: Count files/directories only
- **All commands**: Store success/failure status

## Expected Results

### Before/After Comparison
**Current state file (33KB)**:
```
"output": "[sudo] password for user: CONTAINER ID IMAGE..."
```

**New state file (2KB)**:
```json
{
  "captured_at": "2025-08-06T10:30:45Z",
  "docker": {
    "home": {
      "success": true,
      "container_count": 9
    }
  }
}
```

### Improved Plan Output
```bash
$ python viki.py -p /config plan

Changes detected:
- docker.home: 9 containers → 10 containers (last check: 2 hours ago)
- df.home: 55% disk usage → 58% disk usage (last check: 2 hours ago)

Apply changes? [y/N]
```

## Next Steps
1. **Day 1**: Modify `FetchResponse.fetch()` to extract counts/percentages instead of raw output
2. **Day 2**: Add timestamp and hostname to state JSON structure  
3. **Day 3**: Update plan logic to compare state values and timestamps

## Success Criteria
- State files under 5KB (currently 33KB+)
- Change detection works without manual parsing
- No embedded passwords in state files
- Teams save 2+ hours weekly on server state analysis
EOF < /dev/null