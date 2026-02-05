## Troubleshooting Intro
In this file you'll find troubleshooting scenarios based on the structure discussed in the [README](https://github.com/pdudotdev/netaimcp/tree/main?tab=readme-ov-file#-automation-and-troubleshooting), ranging from basic to more advanced. I will update this list periodically.

⚠️ **NOTE**: Make sure to use `containerlab redeploy -t lab.yml` after each scenario to start clean from the default network configuration.

## 🍀 CCNA-level scenarios

### Scenario 1

- [x] **Summary**:
```
R1A OSPF adjacency stuck in EXCHANGE, while R2A is stuck in EXCH START state.
```
- [x] **Causing Failure**: 
```
Changing the MTU on R2A Eth3 to 1400 to cause a mismatch with R1A, using the commands below:

interface Eth3
 mtu 1400
```
- [x] **Confirming Failure**:
```
Checking the effects of the commands above:

R2A(config-if-Et3)#show interfaces eth3 | i MTU
  IP MTU 1400 bytes, BW 1000000 kbit
R2A(config-if-Et3)#show ip ospf neighbor 
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
3.3.3.3         1        default  1   FULL                   00:00:35    10.0.0.10       Ethernet4
1.1.1.1         1        default  0   EXCH START             00:00:34    10.0.0.1        Ethernet3
7.7.7.7         1        default  0   FULL                   00:00:34    10.1.1.9        Ethernet2
6.6.6.6         1        default  0   FULL                   00:00:33    10.1.1.13       Ethernet1

R1A#show ip ospf neighbor
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
2.2.2.2         1        default  0   EXCHANGE               00:00:32    10.0.0.2        Ethernet4
3.3.3.3         1        default  1   FULL                   00:00:38    10.0.0.6        Ethernet3
11.11.11.11     1        default  1   FULL                   00:00:32    172.16.0.10     Ethernet2
10.10.10.10     1        default  1   FULL                   00:00:30    172.16.0.6      Ethernet1
```
- [x] **User Prompt**:
```
Why is the R1A-R2A OSPF adjacency stuck? Can you check and fix please?
```
- [x] **Commands issued by Claude**:
```
show ip ospf neighbor
show ip ospf interface Ethernet3
show running-config interface Ethernet3
interface Ethernet3
no mtu 1400
```
- [x] **Confirmation**:
```
R2A#show ip ospf neighbor
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
3.3.3.3         1        default  1   FULL                   00:00:34    10.0.0.10       Ethernet4
1.1.1.1         1        default  0   FULL                   00:00:38    10.0.0.1        Ethernet3
7.7.7.7         1        default  0   FULL                   00:00:29    10.1.1.9        Ethernet2
6.6.6.6         1        default  0   FULL                   00:00:33    10.1.1.13       Ethernet1 
```

### Scenario 2

- [x] **Summary**:
```
R1A and R3C OSPF adjancency is broken.
```
- [x] **Causing Failure**: 
```
Wrong OSPF area number configured on R3C's Eth0/3 interface, using the commands below:

router ospf 1
 network 10.0.0.4 0.0.0.3 area 1
```
- [x] **Confirming Failure**:
```
Checking the effects of the commands above:

R3C#show ip ospf interface Eth0/3 | i Area
  Internet Address 10.0.0.6/30, Interface ID 5, Area 1
R3C#show ip ospf neighbor                  

Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           0   FULL/  -        00:00:37    10.0.0.9        Ethernet1/0
```
- [x] **User Prompt**:
```
R1A and R3C OSPF adjancency seems to be broken. Please take a look and solve the issue.
```
- [x] **Commands issued by Claude**:
```
show ip ospf neighbor
show ip ospf interface Ethernet3
show ip interface brief
show running-config | section router ospf
router ospf 1
no network 10.0.0.4 0.0.0.3 area 1
network 10.0.0.4 0.0.0.3 area 0
```
- [x] **Confirmation**:
```
R3C#show ip ospf neighbor 

Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           0   FULL/  -        00:00:39    10.0.0.9        Ethernet1/0
1.1.1.1           0   FULL/  -        00:00:30    10.0.0.5        Ethernet0/3
```

### Scenario 3

- [x] **Summary**:
```
OSPF adjacency between R2A and R3C fails.
```
- [x] **Causing Failure**: 
```
Changing the Hello and Dead timers on R2A to cause a mismatch with R3C, using the commands below:

interface Ethernet4
 ip ospf hello-interval 5
 ip ospf dead-interval 20
```
- [x] **Confirming Failure**:
```
Checking the effects of the commands above:

R2A#show ip ospf interface Ethernet 4
Ethernet4 is up
  Interface Address 10.0.0.9/30, instance 1, VRF default, Area 0.0.0.0
  Network Type Point-To-Point, Cost: 100
  Transmit Delay is 1 sec, State P2P
  Interface Speed: 1000 mbps
  No Designated Router on this network
  No Backup Designated Router on this network
  Timer intervals configured, Hello 5, Dead 20, Retransmit 5
  Neighbor Count is 0
  Message-digest authentication, using key id 1
  Traffic engineering is disabled
  TI-LFA protection is disabled
R2A#show ip ospf neighbor
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
1.1.1.1         1        default  0   FULL                   00:00:38    10.0.0.1        Ethernet3
7.7.7.7         1        default  0   FULL                   00:00:29    10.1.1.9        Ethernet2
6.6.6.6         1        default  0   FULL                   00:00:33    10.1.1.13       Ethernet1
```
- [x] **User Prompt**:
```
OSPF neighborship between R2A and R3C fails. Investigate and apply a fix.
```
- [x] **Commands issued by Claude**:
```
show ip ospf neighbor
show ip ospf interface Ethernet4
show running-config interface Ethernet4
interface Ethernet4
no ip ospf hello-interval 5
no ip ospf dead-interval 20
```
- [x] **Confirmation**:
```
R2A#show ip ospf neighbor
Neighbor ID     Instance VRF      Pri State                  Dead Time   Address         Interface
3.3.3.3         1        default  1   FULL                   00:00:34    10.0.0.10       Ethernet4
1.1.1.1         1        default  0   FULL                   00:00:38    10.0.0.1        Ethernet3
7.7.7.7         1        default  0   FULL                   00:00:29    10.1.1.9        Ethernet2
6.6.6.6         1        default  0   FULL                   00:00:33    10.1.1.13       Ethernet1 
```

## 🔥 CCNP-level scenarios

