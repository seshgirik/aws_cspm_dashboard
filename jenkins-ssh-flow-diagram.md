# Jenkins Agent SSH Connection Flow Diagram

```mermaid
flowchart LR
    A[Jenkins Agent] <-->|SSH Connection<br/>Port 22| B[10.224.78.219:22]
    
    style A fill:#326CE5,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#2ECC71,stroke:#fff,stroke-width:2px,color:#fff
```

## Connection Details

### Bidirectional Traffic Flow

**Outbound (Jenkins Agent → Target Server)**
- SSH connection establishment
- Command execution requests
- File transfers (SCP/SFTP)
- Build artifacts upload
- Job execution instructions

**Inbound (Target Server → Jenkins Agent)**
- SSH authentication responses
- Command execution results
- File transfers (SCP/SFTP)
- Build logs and output
- Status updates

### Connection Parameters
- **Target IP**: 10.224.78.219
- **Port**: 22 (SSH)
- **Protocol**: SSH (Secure Shell)
- **Traffic Direction**: Bidirectional

```mermaid
sequenceDiagram
    participant JA as Jenkins Agent
    participant TS as 10.224.78.219:22
    
    JA->>TS: SSH Connection Request
    TS->>JA: SSH Challenge
    JA->>TS: Authentication (Key/Password)
    TS->>JA: Authentication Success
    
    loop Build Execution
        JA->>TS: Execute Commands
        TS->>JA: Command Output
        JA->>TS: Transfer Files
        TS->>JA: Acknowledgment
    end
    
    JA->>TS: Close Connection
    TS->>JA: Connection Closed
```
