# Minimal TDD Design: viki State Management Parsing

## Problem
State files store raw command output as strings (30KB+). Need structured data for programmatic use.

**Current:** `{"docker": {"home": {"output": "CONTAINER ID   IMAGE..."}}}`  
**Target:** `{"docker": {"home": {"success": true, "container_count": 2, "containers": ["nginx"]}}}`

## Minimal Implementation

### Simple Parser Functions
```python
def parse_docker(output: str, success: bool = True) -> dict:
    result = {"success": success, "timestamp": datetime.utcnow().isoformat() + "Z"}
    if not success or not output.strip():
        return {**result, "container_count": 0, "containers": []}
    
    lines = [line for line in output.split('\n') if line and not line.startswith('[sudo]')]
    containers = [line.split()[-1] for line in lines[1:] if line.split()]
    return {**result, "container_count": len(containers), "containers": containers}

def parse_ls(output: str, success: bool = True) -> dict:
    result = {"success": success, "timestamp": datetime.utcnow().isoformat() + "Z"}
    if not success or not output.strip():
        return {**result, "item_count": 0, "items": []}
    
    items = output.replace('\t', ' ').split()
    return {**result, "item_count": len(items), "items": items}

def parse_df(output: str, success: bool = True) -> dict:
    result = {"success": success, "timestamp": datetime.utcnow().isoformat() + "Z"}
    if not success or not output.strip():
        return {**result, "max_usage_percent": 0}
    
    lines = [line for line in output.split('\n')[1:] if line.strip()]
    percentages = [int(line.split()[4].replace('%', '')) for line in lines if len(line.split()) >= 5]
    return {**result, "max_usage_percent": max(percentages) if percentages else 0}
```

### Essential Tests
```python
def test_parse_docker_with_containers():
    output = """CONTAINER ID   IMAGE   COMMAND   NAMES
123abc   nginx   nginx     web_server
456def   redis   redis     cache"""
    result = parse_docker(output)
    assert result["success"] is True
    assert result["container_count"] == 2
    assert "web_server" in result["containers"]
    assert "cache" in result["containers"]

def test_parse_docker_empty():
    result = parse_docker("CONTAINER ID   IMAGE   COMMAND   NAMES")
    assert result["container_count"] == 0
    assert result["containers"] == []

def test_parse_ls():
    result = parse_ls("file1.txt\tfile2.log\ndir1")
    assert result["item_count"] == 3
    assert "file1.txt" in result["items"]

def test_parse_df():
    output = "Filesystem Size Used Avail Use% Mounted\n/dev/sda1 10G 8G 2G 80% /"
    result = parse_df(output)
    assert result["max_usage_percent"] == 80
```

### Integration
```python
# Simple parser mapping
PARSERS = {
    "docker": parse_docker,
    "ls": parse_ls,
    "lsl": parse_ls,
    "df": parse_df
}

def get_parser(command_type: str):
    return PARSERS.get(command_type, lambda output, success=True: 
        {"success": success, "raw_output": output, "timestamp": datetime.utcnow().isoformat() + "Z"})
```

### Modify FetchResponse
```python
# In fetch() method, add after getting output:
parser_func = get_parser(mod)
parsed_data = parser_func(output, success=(status == 0))
state[mod][name] = {**param, **parsed_data}  # Remove raw output
```

### Modify ApplyResponse
```python
# Same pattern - add parser call after getting output:
parser_func = get_parser(mod)
parsed_data = parser_func(output, success=(status == 0))
self.state[mod][name] = {**param, **parsed_data}
```

### Simple Migration
```python
def migrate_legacy_state(state):
    """Convert 'output' fields to parsed data"""
    for section in ["data", "mods"]:
        if section in state.get("viki", {}):
            for mod, names in state["viki"][section].items():
                for name, data in names.items():
                    if "output" in data:
                        parser_func = get_parser(mod)
                        parsed = parser_func(data["output"], success=True)
                        data.pop("output")
                        data.update(parsed)
    return state
```

### CliRequest Changes
```python
# In __load_state method, add migration check:
if any("output" in data for section in state.get("viki", {}).values() 
       for names in section.values() for data in names.values()):
    state = migrate_legacy_state(state)
    self.write_state(state, file)  # Save migrated version
```

## Implementation Plan
- **Day 1**: Write parser functions and basic tests
- **Day 2**: Integrate with FetchResponse and ApplyResponse  
- **Day 3**: Add migration logic and test with existing state files

## Success Criteria
- State files reduce from 30KB+ to <3KB
- Docker, ls, df commands return structured data instead of raw text  
- Legacy state files auto-migrate on first load
- All existing functionality works unchanged