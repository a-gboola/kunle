# Wazuh Agent Deployment Lab

## Objective

The objective of this lab was to deploy a Wazuh agent on a Windows machine, connect it to the Wazuh Manager, and verify that security events were successfully collected.

---

# Lab Environment

## Monitoring Box (Wazuh Server)

- Operating System: Ubuntu
- IP Address: 192.168.0.129

## Target Machine

- Operating System: Windows 10 Enterprise
- Hostname: DESKTOP-T0B6RQF
- IP Address: 192.168.0.160

---

# Network Diagram

```
                +-----------------------------+
                |      Wazuh Manager          |
                | Ubuntu Server              |
                | 192.168.0.129              |
                +-------------+--------------+
                              |
                              |
                     Wazuh Agent (TCP 1514)
                              |
                              |
                +-------------+--------------+
                | Windows 10 Target Machine |
                | DESKTOP-T0B6RQF           |
                | 192.168.0.160             |
                +---------------------------+
```

---

# Steps Performed

### Step 1

Installed the Wazuh server and verified that the Manager, Indexer, Dashboard and Filebeat services were running.

### Step 2

Opened the **Deploy New Agent** wizard from the Wazuh Dashboard.

### Step 3

Selected Windows as the operating system and generated the installation command.

### Step 4

Installed the Wazuh agent on the Windows machine and configured it to communicate with the Wazuh Manager at **192.168.0.129**.

### Step 5

Started the Wazuh agent service and confirmed that it was running successfully.

### Step 6

Verified that the Windows agent successfully registered with the Wazuh Manager and its status changed to **Active**.

### Step 7

Generated Windows events and confirmed that the events were received by the Wazuh Dashboard. The dashboard successfully displayed alerts and MITRE ATT&CK mappings, confirming end-to-end telemetry.

---

# Results

- Wazuh Agent successfully installed.
- Agent connected to Manager.
- Agent status changed to Active.
- Security events were collected.
- MITRE ATT&CK detections were displayed.

---

# Screenshots

## Agent Status

*(Insert screenshot showing DESKTOP-T0B6RQF is Active.)*

## Security Events

*(Insert screenshot showing the generated event or MITRE ATT&CK dashboard.)*

---

# Conclusion

The Wazuh deployment was completed successfully. The Windows endpoint was enrolled with the Wazuh Manager and successfully transmitted security events, demonstrating that the monitoring pipeline was functioning correctly.