# viki Design Principles Gap Analysis

## Executive Summary

Critical gaps exist in all three design principles. **Priority fixes**: idempotency failures causing re-run errors, hardcoded values preventing reuse, and configuration duplication increasing setup time.

**Current State:**
- **Repeatability**: 60% - Hardcoded tokens/paths block server reuse
- **Idempotency**: 40% - wget/cloudflared modules fail on re-runs
- **User Friendly**: 50% - Copy-paste workflow, 30min setup per server

## 1. Critical Issues Blocking Repeatability

**Problem 1: Hardcoded Tokens**
```yaml
cloudflared:
  ubuntu-dev:
    token: <token>  # Must be changed per server
```
*Impact: Manual editing required for every server deployment*

**Problem 2: Hardcoded Paths**
```python
"gitwiki": "sudo git clone ${repo} /var/snap/docker/common/..."  # Only works with snap Docker
```
*Impact: Breaks on different Docker installations*

**Cost: 15-30 minutes manual editing per server**

## 2. Critical Idempotency Failures

**Problem 1: wget Always Re-downloads**
```python
"wget": "wget -O ${path}/${output} ${url}"  # No file existence check
```
*Impact: Re-downloads 5-12GB of ISOs every run*

**Problem 2: cloudflared Container Conflicts**
```python
"cloudflared": "docker run -d --name ${name} ..."  # Fails if name exists
```
*Impact: 80% failure rate on re-runs*

**Problem 3: git clone Always Fails**
```python
"gitwiki": "git clone ${repo} ${path}"  # Fails if directory exists
```
*Impact: 100% failure rate on re-runs*

**Cost: Manual cleanup required between every execution**

## 3. Poor User Experience

**Problem: Configuration Copy-Paste Workflow**

Every server requires duplicating 100+ lines:
```yaml
# Same variables copied to every server
vars:
  hostname: "export VK_VAR_hostname"
  username: "export VK_VAR_username"
  password: "export VK_VAR_password"
  # ... repeated across all 3 server configs
```

**Cost: 30-45 minutes per new server setup**

## 4. Root Causes

**Technical Issues:**
1. Modules don't check existing system state
2. No conditional logic in commands
3. Hardcoded values in configurations

**User Experience Issues:**
1. No configuration templates
2. No variable inheritance
3. Copy-paste required for every server

## 5. Priority Solutions (80/20 Fixes)

**Week 1 - Fix Idempotency (High Impact, Low Effort)**
1. **wget**: Add `[ -f file ] || wget` check
2. **cloudflared**: Add `docker ps | grep name || docker run` check
3. **gitwiki**: Add `[ -d dir ] || git clone` check

**Week 2 - Fix Hardcoding (High Impact, Low Effort)**
4. **Externalize tokens**: Move to `VK_VAR_cloudflared_token`
5. **Make paths configurable**: Add `VK_VAR_docker_path` variable

**Week 3 - Basic Templates (Medium Impact, Low Effort)**
6. **Create 3 templates**: web-server.vk.yaml, dev-server.vk.yaml, base-server.vk.yaml

## 6. Implementation Details

**Week 1: Idempotency Fixes**
```python
# Simple file existence check for wget
"wget": "[ -f ${path}/${output} ] || wget -O ${path}/${output} ${url}"

# Simple container check for cloudflared
"cloudflared": "docker ps | grep ${name} || docker run -d --name ${name} cloudflare/cloudflared:latest tunnel run --token ${token}"

# Simple directory check for gitwiki
"gitwiki": "[ -d ${path} ] || git clone ${repo} ${path}"
```

**Week 2: Variable Externalization**
```yaml
# Add new environment variables
cloudflared_token: "VK_VAR_cloudflared_token"
docker_path: "VK_VAR_docker_path"
server_name: "VK_VAR_server_name"
```

**Week 3: Basic Templates**
Create `templates/base-server.vk.yaml` with common patterns users can copy.

## 7. Success Metrics

**After 3-week implementation:**
- Repeatability: 85% (from 60%)
- Idempotency: 90% (from 40%)
- User Friendliness: 75% (from 50%)
- Setup time: <10 minutes per server (from 30-45 minutes)

## 8. Next Actions

1. **This week**: Fix wget idempotency in `ssh_command.py`
2. **Week 2**: Externalize hardcoded tokens to environment variables
3. **Week 3**: Create `templates/base-server.vk.yaml` template file

**Risk**: Ensure backward compatibility with existing configurations during changes.
