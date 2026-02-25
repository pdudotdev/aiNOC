# IT-003 — MCP Tool Test Results
*Generated: 2026-02-25 13:46:54 UTC*

## IT-003a: Platform Connectivity

### test_connectivity_ios (R3C — SSH)
```json
{
  "device": "R3C",
  "cli_style": "ios",
  "cache_hit": false,
  "parsed": {
    "version": {
      "version_short": "17.16",
      "platform": "Linux",
      "version": "17.16.1a",
      "image_id": "X86_64BI_LINUX-ADVENTERPRISEK9-M",
      "label": "RELEASE SOFTWARE (fc1)",
      "os": "IOS",
      "location": "IOSXE",
      "image_type": "production image",
      "copyright_years": "1986-2024",
      "compiled_date": "Thu 19-Dec-24 17:54",
      "compiled_by": "mcpre",
      "rom": "Bootstrap program is Linux",
      "hostname": "R3C",
      "uptime": "9 hours, 17 minutes",
      "system_restarted_at": "04:28:45 UTC Wed Feb 25 2026",
      "system_image": "unix:/iol/iol.bin",
      "last_reload_reason": "Unknown reason",
      "chassis_sn": "14",
      "number_of_intfs": {
        "Ethernet": "8"
      },
      "processor_board_flash": "1024K",
      "curr_config_register": "0x0"
    }
  }
}
```

### test_connectivity_eos (R1A — eAPI)
```json
{
  "device": "R1A",
  "cli_style": "eos",
  "cache_hit": false,
  "parsed": [
    {
      "mfgName": "Arista",
      "modelName": "cEOSLab",
      "hardwareRevision": "",
      "serialNumber": "88F838957495E4CE2476B8BA54D6510D",
      "systemMacAddress": "00:1c:73:a4:d7:d8",
      "hwMacAddress": "00:00:00:00:00:00",
      "configMacAddress": "00:00:00:00:00:00",
      "version": "4.35.0F-44178984.4350F (engineering build)",
      "architecture": "x86_64",
      "internalVersion": "4.35.0F-44178984.4350F",
      "internalBuildId": "33b708fe-8b04-48db-bb84-7f77a6b3cc66",
      "imageFormatVersion": "1.0",
      "imageOptimization": "None",
      "kernelVersion": "6.17.0-14-generic",
      "bootupTimestamp": 1771993713.3228443,
      "uptime": 33490.58578681946,
      "memTotal": 32819004,
      "memFree": 18128880,
      "isIntlVersion": false
    }
  ]
}
```

### test_connectivity_ros (R18M — REST)
```json
{
  "device": "R18M",
  "cli_style": "routeros",
  "cache_hit": false,
  "parsed": [
    {
      ".id": "*2018A000",
      "active": "true",
      "bgp": "true",
      "distance": "20",
      "dst-address": "0.0.0.0/0",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018B000",
      "bgp": "true",
      "distance": "20",
      "dst-address": "0.0.0.0/0",
      "dynamic": "true",
      "gateway": "220.50.50.1",
      "immediate-gw": "220.50.50.1%ether3",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018C030",
      "distance": "110",
      "dst-address": "0.0.0.0/0",
      "dynamic": "true",
      "gateway": "172.16.77.1%ether4",
      "immediate-gw": "172.16.77.1%ether4",
      "inactive": "false",
      "ospf": "true",
      "routing-table": "main",
      "scope": "20",
      "target-scope": "10"
    },
    {
      ".id": "*201830B0",
      "active": "true",
      "connect": "true",
      "distance": "0",
      "dst-address": "18.18.18.0/24",
      "dynamic": "true",
      "ecmp": "true",
      "gateway": "lo1",
      "immediate-gw": "lo1",
      "inactive": "false",
      "local-address": "18.18.18.1%lo1",
      "routing-table": "main",
      "scope": "10",
      "target-scope": "5"
    },
    {
      ".id": "*201830D0",
      "active": "true",
      "connect": "true",
      "distance": "0",
      "dst-address": "18.18.18.0/24",
      "dynamic": "true",
      "ecmp": "true",
      "gateway": "lo3",
      "immediate-gw": "lo3",
      "inactive": "false",
      "local-address": "18.18.18.3%lo3",
      "routing-table": "main",
      "scope": "10",
      "target-scope": "5"
    },
    {
      ".id": "*2018C000",
      "active": "true",
      "distance": "110",
      "dst-address": "19.19.19.0/24",
      "dynamic": "true",
      "gateway": "172.16.77.1%ether4",
      "immediate-gw": "172.16.77.1%ether4",
      "inactive": "false",
      "ospf": "true",
      "routing-table": "main",
      "scope": "20",
      "target-scope": "10"
    },
    {
      ".id": "*2018C010",
      "active": "true",
      "distance": "110",
      "dst-address": "20.20.20.0/24",
      "dynamic": "true",
      "gateway": "172.16.77.6%ether5",
      "immediate-gw": "172.16.77.6%ether5",
      "inactive": "false",
      "ospf": "true",
      "routing-table": "main",
      "scope": "20",
      "target-scope": "10"
    },
    {
      ".id": "*20183090",
      "active": "true",
      "connect": "true",
      "distance": "0",
      "dst-address": "172.16.77.0/30",
      "dynamic": "true",
      "gateway": "ether4",
      "immediate-gw": "ether4",
      "inactive": "false",
      "local-address": "172.16.77.2%ether4",
      "routing-table": "main",
      "scope": "10",
      "target-scope": "5"
    },
    {
      ".id": "*201830A0",
      "active": "true",
      "connect": "true",
      "distance": "0",
      "dst-address": "172.16.77.4/30",
      "dynamic": "true",
      "gateway": "ether5",
      "immediate-gw": "ether5",
      "inactive": "false",
      "local-address": "172.16.77.5%ether5",
      "routing-table": "main",
      "scope": "10",
      "target-scope": "5"
    },
    {
      ".id": "*2018C020",
      "active": "true",
      "distance": "110",
      "dst-address": "172.16.77.8/30",
      "dynamic": "true",
      "ecmp": "true",
      "gateway": "172.16.77.6%ether5",
      "immediate-gw": "172.16.77.6%ether5",
      "inactive": "false",
      "ospf": "true",
      "routing-table": "main",
      "scope": "20",
      "target-scope": "10"
    },
    {
      ".id": "*2018C040",
      "active": "true",
      "distance": "110",
      "dst-address": "172.16.77.8/30",
      "dynamic": "true",
      "ecmp": "true",
      "gateway": "172.16.77.1%ether4",
      "immediate-gw": "172.16.77.1%ether4",
      "inactive": "false",
      "ospf": "true",
      "routing-table": "main",
      "scope": "20",
      "target-scope": "10"
    },
    {
      ".id": "*80000001",
      "active": "true",
      "distance": "1",
      "dst-address": "172.20.20.0/24",
      "dynamic": "false",
      "gateway": "172.31.255.29",
      "immediate-gw": "172.31.255.29%ether1",
      "inactive": "false",
      "routing-table": "main",
      "scope": "30",
      "static": "true",
      "target-scope": "10"
    },
    {
      ".id": "*20183060",
      "active": "true",
      "connect": "true",
      "distance": "0",
      "dst-address": "172.31.255.28/30",
      "dynamic": "true",
      "gateway": "ether1",
      "immediate-gw": "ether1",
      "inactive": "false",
      "local-address": "172.31.255.30%ether1",
      "routing-table": "main",
      "scope": "10",
      "target-scope": "5"
    },
    {
      ".id": "*2018A010",
      "active": "true",
      "bgp": "true",
      "distance": "20",
      "dst-address": "200.40.40.0/30",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018A020",
      "active": "true",
      "bgp": "true",
      "distance": "20",
      "dst-address": "200.40.40.4/30",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018B010",
      "active": "true",
      "bgp": "true",
      "distance": "20",
      "dst-address": "200.50.50.0/30",
      "dynamic": "true",
      "gateway": "220.50.50.1",
      "immediate-gw": "220.50.50.1%ether3",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018A050",
      "bgp": "true",
      "distance": "20",
      "dst-address": "200.50.50.0/30",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018B020",
      "active": "true",
      "bgp": "true",
      "distance": "20",
      "dst-address": "200.50.50.4/30",
      "dynamic": "true",
      "gateway": "220.50.50.1",
      "immediate-gw": "220.50.50.1%ether3",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018A060",
      "bgp": "true",
      "distance": "20",
      "dst-address": "200.50.50.4/30",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*20183070",
      "active": "true",
      "connect": "true",
      "distance": "0",
      "dst-address": "220.40.40.0/30",
      "dynamic": "true",
      "gateway": "ether2",
      "immediate-gw": "ether2",
      "inactive": "false",
      "local-address": "220.40.40.2%ether2",
      "routing-table": "main",
      "scope": "10",
      "target-scope": "5"
    },
    {
      ".id": "*2018A030",
      "bgp": "true",
      "distance": "20",
      "dst-address": "220.40.40.0/30",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018A040",
      "active": "true",
      "bgp": "true",
      "distance": "20",
      "dst-address": "220.40.40.4/30",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*20183080",
      "active": "true",
      "connect": "true",
      "distance": "0",
      "dst-address": "220.50.50.0/30",
      "dynamic": "true",
      "gateway": "ether3",
      "immediate-gw": "ether3",
      "inactive": "false",
      "local-address": "220.50.50.2%ether3",
      "routing-table": "main",
      "scope": "10",
      "target-scope": "5"
    },
    {
      ".id": "*2018B030",
      "bgp": "true",
      "distance": "20",
      "dst-address": "220.50.50.0/30",
      "dynamic": "true",
      "gateway": "220.50.50.1",
      "immediate-gw": "220.50.50.1%ether3",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018A070",
      "bgp": "true",
      "distance": "20",
      "dst-address": "220.50.50.0/30",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018B040",
      "active": "true",
      "bgp": "true",
      "distance": "20",
      "dst-address": "220.50.50.4/30",
      "dynamic": "true",
      "gateway": "220.50.50.1",
      "immediate-gw": "220.50.50.1%ether3",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    },
    {
      ".id": "*2018A080",
      "bgp": "true",
      "distance": "20",
      "dst-address": "220.50.50.4/30",
      "dynamic": "true",
      "gateway": "220.40.40.1",
      "immediate-gw": "220.40.40.1%ether2",
      "inactive": "false",
      "routing-table": "main",
      "scope": "40",
      "target-scope": "10"
    }
  ]
}
```

## IT-003b: Protocol Tools

### test_ospf_eos (R1A — eAPI)
```json
{
  "device": "R1A",
  "cli_style": "eos",
  "cache_hit": false,
  "parsed": [
    {
      "vrfs": {
        "default": {
          "instList": {
            "1": {
              "ospfNeighborEntries": [
                {
                  "routerId": "2.2.2.2",
                  "interfaceAddress": "10.0.0.2",
                  "interfaceName": "Ethernet4",
                  "priority": 1,
                  "adjacencyState": "full",
                  "drState": null,
                  "options": {
                    "multitopologyCapability": false,
                    "externalRoutingCapability": true,
                    "multicastCapability": false,
                    "nssaCapability": false,
                    "linkLocalSignaling": false,
                    "demandCircuitsSupport": false,
                    "opaqueLsaSupport": false,
                    "doNotUseInRouteCalc": false
                  },
                  "inactivity": 1772027237.9383678,
                  "details": {
                    "areaId": "0.0.0.0",
                    "designatedRouter": "0.0.0.0",
                    "backupDesignatedRouter": "0.0.0.0",
                    "numberOfStateChanges": 6,
                    "stateTime": 1772009729.938387,
                    "inactivityDefers": 0,
                    "retransmissionCount": 0,
                    "bfdState": "adminDown",
                    "bfdRequestSent": false,
                    "grHelperTimer": null,
                    "grNumAttempts": 0,
                    "grLastRestartTime": null
                  }
                },
                {
                  "routerId": "3.3.3.3",
                  "interfaceAddress": "10.0.0.6",
                  "interfaceName": "Ethernet3",
                  "priority": 1,
                  "adjacencyState": "full",
                  "drState": null,
                  "options": {
                    "multitopologyCapability": false,
                    "externalRoutingCapability": true,
                    "multicastCapability": false,
                    "nssaCapability": false,
                    "linkLocalSignaling": false,
                    "demandCircuitsSupport": false,
                    "opaqueLsaSupport": false,
                    "doNotUseInRouteCalc": false
                  },
                  "inactivity": 1772027238.938532,
                  "details": {
                    "areaId": "0.0.0.0",
                    "designatedRouter": "0.0.0.0",
                    "backupDesignatedRouter": "0.0.0.0",
                    "numberOfStateChanges": 7,
                    "stateTime": 1772020368.9385433,
                    "inactivityDefers": 0,
                    "retransmissionCount": 2,
                    "bfdState": "adminDown",
                    "bfdRequestSent": false,
                    "grHelperTimer": null,
                    "grNumAttempts": 0,
                    "grLastRestartTime": null
                  }
                },
                {
                  "routerId": "11.11.11.11",
                  "interfaceAddress": "172.16.0.10",
                  "interfaceName": "Ethernet2",
                  "priority": 1,
                  "adjacencyState": "full",
                  "drState": null,
                  "options": {
                    "multitopologyCapability": false,
                    "externalRoutingCapability": false,
                    "multicastCapability": false,
                    "nssaCapability": false,
                    "linkLocalSignaling": false,
                    "demandCircuitsSupport": false,
                    "opaqueLsaSupport": false,
                    "doNotUseInRouteCalc": false
                  },
                  "inactivity": 1772027241.9386666,
                  "details": {
                    "areaId": "0.0.0.2",
                    "designatedRouter": "0.0.0.0",
                    "backupDesignatedRouter": "0.0.0.0",
                    "numberOfStateChanges": 7,
                    "stateTime": 1771993801.9386773,
                    "inactivityDefers": 0,
                    "retransmissionCount": 1,
                    "bfdState": "adminDown",
                    "bfdRequestSent": false,
                    "grHelperTimer": null,
                    "grNumAttempts": 0,
                    "grLastRestartTime": null
                  }
                },
                {
                  "routerId": "10.10.10.10",
                  "interfaceAddress": "172.16.0.6",
                  "interfaceName": "Ethernet1",
                  "priority": 1,
                  "adjacencyState": "full",
                  "drState": null,
                  "options": {
                    "multitopologyCapability": false,
                    "externalRoutingCapability": false,
                    "multicastCapability": false,
                    "nssaCapability": false,
                    "linkLocalSignaling": false,
                    "demandCircuitsSupport": false,
                    "opaqueLsaSupport": false,
                    "doNotUseInRouteCalc": false
                  },
                  "inactivity": 1772027235.9388402,
                  "details": {
                    "areaId": "0.0.0.2",
                    "designatedRouter": "0.0.0.0",
                    "backupDesignatedRouter": "0.0.0.0",
                    "numberOfStateChanges": 7,
                    "stateTime": 1771993803.9388523,
                    "inactivityDefers": 0,
                    "retransmissionCount": 0,
                    "bfdState": "adminDown",
                    "bfdRequestSent": false,
                    "grHelperTimer": null,
                    "grNumAttempts": 0,
                    "grLastRestartTime": null
                  }
                }
              ]
            }
          }
        }
      }
    }
  ]
}
```

### test_eigrp_ios (R3C — SSH)
```json
{
  "device": "R3C",
  "cli_style": "ios",
  "cache_hit": false,
  "parsed": {
    "eigrp_instance": {
      "10": {
        "vrf": {
          "default": {
            "address_family": {
              "ipv4": {
                "name": "",
                "named_mode": false,
                "eigrp_interface": {
                  "Ethernet0/2": {
                    "eigrp_nbr": {
                      "192.168.10.2": {
                        "peer_handle": 1,
                        "hold": 13,
                        "uptime": "03:14:15",
                        "srtt": 0.001,
                        "rto": 100,
                        "q_cnt": 0,
                        "last_seq_number": 194
                      }
                    }
                  },
                  "Ethernet0/1": {
                    "eigrp_nbr": {
                      "192.168.10.6": {
                        "peer_handle": 0,
                        "hold": 10,
                        "uptime": "03:14:16",
                        "srtt": 0.001,
                        "rto": 100,
                        "q_cnt": 0,
                        "last_seq_number": 191
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### test_bgp_ros (R18M — REST)
```json
{
  "device": "R18M",
  "cli_style": "routeros",
  "cache_hit": false,
  "parsed": [
    {
      ".id": "*1",
      "as": "2020",
      "inactive": "false",
      "instance": "default",
      "local.default-address": "220.40.40.2",
      "local.role": "ebgp",
      "name": "TO-R14C",
      "remote.address": "220.40.40.1",
      "remote.as": "4040",
      "routing-table": "main"
    },
    {
      ".id": "*2",
      "as": "2020",
      "inactive": "false",
      "instance": "default",
      "local.default-address": "220.50.50.2",
      "local.role": "ebgp",
      "name": "TO-R17C",
      "remote.address": "220.50.50.1",
      "remote.as": "5050",
      "routing-table": "main"
    }
  ]
}
```

### test_interfaces_ros (R19M — REST)
```json
{
  "device": "R19M",
  "cli_style": "routeros",
  "cache_hit": false,
  "parsed": [
    {
      ".id": "*2",
      "actual-mtu": "1500",
      "default-name": "ether1",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:29:47",
      "link-downs": "0",
      "mac-address": "0C:00:0F:87:79:00",
      "mtu": "1500",
      "name": "ether1",
      "running": "true",
      "rx-byte": "264237",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "2762",
      "tx-byte": "4178091",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "15502",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*3",
      "actual-mtu": "1500",
      "comment": "TO-R18M",
      "default-name": "ether2",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:29:47",
      "link-downs": "0",
      "mac-address": "AA:C1:AB:80:13:9B",
      "mtu": "1500",
      "name": "ether2",
      "running": "true",
      "rx-byte": "1126408",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "8864",
      "tx-byte": "1393873",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "12783",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*4",
      "actual-mtu": "1500",
      "comment": "TO-R17C",
      "default-name": "ether3",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:29:47",
      "link-downs": "0",
      "mac-address": "AA:C1:AB:A1:C4:8C",
      "mtu": "1500",
      "name": "ether3",
      "running": "true",
      "rx-byte": "840676",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "6696",
      "tx-byte": "1133026",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "9915",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*5",
      "actual-mtu": "1500",
      "comment": "TO-R14C",
      "default-name": "ether4",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:29:47",
      "link-downs": "0",
      "mac-address": "AA:C1:AB:C9:B1:35",
      "mtu": "1500",
      "name": "ether4",
      "running": "true",
      "rx-byte": "865253",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "7056",
      "tx-byte": "1158028",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "10279",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*6",
      "actual-mtu": "1500",
      "comment": "TO-R20M",
      "default-name": "ether5",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:29:47",
      "link-downs": "0",
      "mac-address": "AA:C1:AB:4F:6E:1E",
      "mtu": "1500",
      "name": "ether5",
      "running": "true",
      "rx-byte": "1672057",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "17199",
      "tx-byte": "1405044",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "13264",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*1",
      "actual-mtu": "65536",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:29:37",
      "link-downs": "0",
      "mac-address": "00:00:00:00:00:00",
      "mtu": "65536",
      "name": "lo",
      "running": "true",
      "rx-byte": "0",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "0",
      "tx-byte": "0",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "0",
      "tx-queue-drop": "0",
      "type": "loopback"
    },
    {
      ".id": "*7",
      "actual-mtu": "1500",
      "comment": "Loopback1",
      "disabled": "false",
      "dynamic": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "l2mtu": "65535",
      "last-link-up-time": "2026-02-25 04:29:54",
      "link-downs": "0",
      "mac-address": "42:CB:8A:1D:B3:09",
      "mtu": "auto",
      "name": "lo1",
      "running": "true",
      "rx-byte": "0",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "0",
      "tx-byte": "767923",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "4461",
      "tx-queue-drop": "0",
      "type": "bridge"
    }
  ]
}
```

### test_routing_ios (R5C — SSH)
```json
{
  "device": "R5C",
  "cli_style": "ios",
  "cache_hit": false,
  "parsed": {
    "entry": {
      "10.0.0.8/30": {
        "ip": "10.0.0.8",
        "mask": "30",
        "known_via": "eigrp 10",
        "distance": "170",
        "metric": "281856",
        "type": "routine ",
        "redist_via": "eigrp",
        "redist_via_tag": "10",
        "update": {
          "from": "192.168.10.5",
          "interface": "Ethernet0/1",
          "age": "03:14:16"
        },
        "paths": {
          "1": {
            "nexthop": "192.168.10.5",
            "from": "192.168.10.5",
            "age": "03:14:16",
            "interface": "Ethernet0/1",
            "prefer_non_rib_labels": false,
            "merge_labels": false,
            "metric": "281856",
            "share_count": "1"
          }
        }
      }
    },
    "total_prefixes": 1
  }
}
```

### test_ping_eos (R6A — eAPI)
```json
{
  "device": "R6A",
  "cli_style": "eos",
  "cache_hit": false,
  "parsed": [
    {
      "messages": [
        "PING 10.1.1.5 (10.1.1.5) 72(100) bytes of data.\n80 bytes from 10.1.1.5: icmp_seq=1 ttl=255 time=0.515 ms\n80 bytes from 10.1.1.5: icmp_seq=2 ttl=255 time=0.209 ms\n80 bytes from 10.1.1.5: icmp_seq=3 ttl=255 time=0.292 ms\n80 bytes from 10.1.1.5: icmp_seq=4 ttl=255 time=0.209 ms\n80 bytes from 10.1.1.5: icmp_seq=5 ttl=255 time=0.319 ms\n\n--- 10.1.1.5 ping statistics ---\n5 packets transmitted, 5 received, 0% packet loss, time 2ms\nrtt min/avg/max/mdev = 0.209/0.308/0.515/0.112 ms, ipg/ewma 0.468/0.410 ms\n"
      ]
    }
  ]
}
```

### test_routing_policies_ios (R8C — SSH)
```json
{
  "device": "R8C",
  "cli_style": "ios",
  "cache_hit": false,
  "raw": "route-map OSPF-TO-EIGRP, permit, sequence 10\n  Match clauses:\n  Set clauses:\n    metric 1000000 1 255 1 1500\n  Policy routing matches: 0 packets, 0 bytes\nroute-map ACCESS-R2-LO, permit, sequence 10\n  Match clauses:\n    ip address (access-lists): 100\n  Set clauses:\n    ip next-hop 10.1.1.6\n  Policy routing matches: 32 packets, 2190 bytes"
}
```

### test_traceroute_ros (R20M — REST)
```json
{
  "device": "R20M",
  "cli_style": "routeros",
  "cache_hit": false,
  "parsed": [
    {
      ".section": "0",
      "address": "172.16.77.9",
      "avg": "0.5",
      "best": "0.5",
      "last": "0.5",
      "loss": "0",
      "sent": "1",
      "status": "",
      "std-dev": "0",
      "worst": "0.5"
    },
    {
      ".section": "0",
      "address": "172.16.77.2",
      "avg": "0.5",
      "best": "0.5",
      "last": "0.5",
      "loss": "0",
      "sent": "1",
      "status": "",
      "std-dev": "0",
      "worst": "0.5"
    }
  ]
}
```

### test_run_show_eos (R7A — eAPI)
```json
{
  "device": "R7A",
  "cli_style": "eos",
  "cache_hit": false,
  "parsed": [
    {
      "ipV4Neighbors": [
        {
          "address": "10.1.1.10",
          "age": 7164,
          "hwAddress": "aabb.cc00.0d20",
          "interface": "Ethernet1"
        },
        {
          "address": "10.1.1.5",
          "age": 8350,
          "hwAddress": "aabb.cc00.1320",
          "interface": "Ethernet2"
        },
        {
          "address": "172.20.20.1",
          "age": 0,
          "hwAddress": "167c.6efc.feac",
          "interface": "Management0"
        }
      ],
      "totalEntries": 3,
      "staticEntries": 0,
      "dynamicEntries": 3,
      "notLearnedEntries": 0
    }
  ]
}
```

### test_redistribution_ros (R18M — REST)
```json
{
  "device": "R18M",
  "error": "Routing policy query 'redistribution' not supported on ROUTEROS"
}
```

## IT-003c: Cache Behavior

### test_cache_behavior (R3C — SSH)
```json
{
  "call_1_miss": {
    "device": "R3C",
    "cli_style": "ios",
    "cache_hit": true,
    "parsed": {
      "time": "13:46:46.575",
      "timezone": "UTC",
      "day_of_week": "Wed",
      "month": "Feb",
      "day": "25",
      "year": "2026"
    }
  },
  "call_2_hit": {
    "device": "R3C",
    "cli_style": "ios",
    "cache_hit": true,
    "parsed": {
      "time": "13:46:46.575",
      "timezone": "UTC",
      "day_of_week": "Wed",
      "month": "Feb",
      "day": "25",
      "year": "2026"
    }
  },
  "call_3_miss_after_ttl": {
    "device": "R3C",
    "cli_style": "ios",
    "cache_hit": false,
    "parsed": {
      "time": "13:46:52.879",
      "timezone": "UTC",
      "day_of_week": "Wed",
      "month": "Feb",
      "day": "25",
      "year": "2026"
    }
  }
}
```

## IT-003d: push_config (Loopback CRUD)

### test_push_config_ios (R3C)

#### Create
```json
{
  "R3C": {
    "transport_used": "asyncssh",
    "result": "interface Loopback99\nip address 10.99.99.1 255.255.255.255\nno shutdown\n"
  },
  "execution_time_seconds": 0.62,
  "risk_assessment": {
    "risk": "high",
    "devices": 1,
    "reasons": [
      "Interface disruption possible"
    ]
  }
}
```

#### Verify
```json
{
  "device": "R3C",
  "cli_style": "ios",
  "cache_hit": false,
  "parsed": {
    "interface": {
      "Ethernet0/0": {
        "ip_address": "172.20.20.203",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "up",
        "protocol": "up"
      },
      "Ethernet0/1": {
        "ip_address": "192.168.10.5",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "up",
        "protocol": "up"
      },
      "Ethernet0/2": {
        "ip_address": "192.168.10.1",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "up",
        "protocol": "up"
      },
      "Ethernet0/3": {
        "ip_address": "10.0.0.6",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "up",
        "protocol": "up"
      },
      "Ethernet1/0": {
        "ip_address": "10.0.0.10",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "up",
        "protocol": "up"
      },
      "Ethernet1/1": {
        "ip_address": "200.50.50.5",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "up",
        "protocol": "up"
      },
      "Ethernet1/2": {
        "ip_address": "200.40.40.5",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "up",
        "protocol": "up"
      },
      "Ethernet1/3": {
        "ip_address": "unassigned",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "administratively down",
        "protocol": "down"
      },
      "Loopback1": {
        "ip_address": "3.3.3.3",
        "interface_is_ok": "YES",
        "method": "NVRAM",
        "status": "up",
        "protocol": "up"
      },
      "Loopback99": {
        "ip_address": "10.99.99.1",
        "interface_is_ok": "YES",
        "method": "manual",
        "status": "up",
        "protocol": "up"
      }
    }
  }
}
```

#### Delete
```json
{
  "R3C": {
    "transport_used": "asyncssh",
    "result": "no interface Loopback99\n"
  },
  "execution_time_seconds": 0.43,
  "risk_assessment": {
    "risk": "low",
    "devices": 1,
    "reasons": [
      "Minor configuration change"
    ]
  }
}
```

### test_push_config_eos (R1A)

#### Create
```json
{
  "R1A": {
    "transport_used": "eapi",
    "result": [
      {
        "output": ""
      },
      {
        "output": ""
      },
      {
        "output": ""
      },
      {
        "output": ""
      }
    ]
  },
  "execution_time_seconds": 0.03,
  "risk_assessment": {
    "risk": "low",
    "devices": 1,
    "reasons": [
      "Minor configuration change"
    ]
  }
}
```

#### Verify
```json
{
  "device": "R1A",
  "cli_style": "eos",
  "cache_hit": false,
  "parsed": [
    {
      "interfaces": {
        "Ethernet1": {
          "name": "Ethernet1",
          "interfaceStatus": "connected",
          "lineProtocolStatus": "up",
          "mtu": 1500,
          "ipv4Routable240": false,
          "ipv4Routable0": false,
          "interfaceAddress": {
            "ipAddr": {
              "address": "172.16.0.5",
              "maskLen": 30
            }
          },
          "nonRoutableClassEIntf": false
        },
        "Ethernet2": {
          "name": "Ethernet2",
          "interfaceStatus": "connected",
          "lineProtocolStatus": "up",
          "mtu": 1500,
          "ipv4Routable240": false,
          "ipv4Routable0": false,
          "interfaceAddress": {
            "ipAddr": {
              "address": "172.16.0.9",
              "maskLen": 30
            }
          },
          "nonRoutableClassEIntf": false
        },
        "Ethernet3": {
          "name": "Ethernet3",
          "interfaceStatus": "connected",
          "lineProtocolStatus": "up",
          "mtu": 1500,
          "ipv4Routable240": false,
          "ipv4Routable0": false,
          "interfaceAddress": {
            "ipAddr": {
              "address": "10.0.0.5",
              "maskLen": 30
            }
          },
          "nonRoutableClassEIntf": false
        },
        "Ethernet4": {
          "name": "Ethernet4",
          "interfaceStatus": "connected",
          "lineProtocolStatus": "up",
          "mtu": 1500,
          "ipv4Routable240": false,
          "ipv4Routable0": false,
          "interfaceAddress": {
            "ipAddr": {
              "address": "10.0.0.1",
              "maskLen": 30
            }
          },
          "nonRoutableClassEIntf": false
        },
        "Loopback99": {
          "name": "Loopback99",
          "interfaceStatus": "connected",
          "lineProtocolStatus": "up",
          "mtu": 65535,
          "ipv4Routable240": false,
          "ipv4Routable0": false,
          "interfaceAddress": {
            "ipAddr": {
              "address": "10.99.99.1",
              "maskLen": 32
            }
          },
          "nonRoutableClassEIntf": false
        },
        "Loopback111": {
          "name": "Loopback111",
          "interfaceStatus": "connected",
          "lineProtocolStatus": "up",
          "mtu": 65535,
          "ipv4Routable240": false,
          "ipv4Routable0": false,
          "interfaceAddress": {
            "ipAddr": {
              "address": "1.11.111.1",
              "maskLen": 24
            }
          },
          "nonRoutableClassEIntf": false
        },
        "Loopback222": {
          "name": "Loopback222",
          "interfaceStatus": "connected",
          "lineProtocolStatus": "up",
          "mtu": 65535,
          "ipv4Routable240": false,
          "ipv4Routable0": false,
          "interfaceAddress": {
            "ipAddr": {
              "address": "2.22.222.2",
              "maskLen": 24
            }
          },
          "nonRoutableClassEIntf": false
        },
        "Management0": {
          "name": "Management0",
          "interfaceStatus": "connected",
          "lineProtocolStatus": "up",
          "mtu": 1500,
          "ipv4Routable240": false,
          "ipv4Routable0": false,
          "interfaceAddress": {
            "ipAddr": {
              "address": "172.20.20.201",
              "maskLen": 24
            }
          },
          "nonRoutableClassEIntf": false
        }
      }
    }
  ]
}
```

#### Delete
```json
{
  "R1A": {
    "transport_used": "eapi",
    "result": [
      {
        "output": ""
      },
      {
        "output": ""
      },
      {
        "output": ""
      }
    ]
  },
  "execution_time_seconds": 0.02,
  "risk_assessment": {
    "risk": "low",
    "devices": 1,
    "reasons": [
      "Minor configuration change"
    ]
  }
}
```

### test_push_config_ros (R18M)

#### Create
```json
{
  "R18M": {
    "transport_used": "rest",
    "result": [
      {
        ".id": "*C",
        "actual-mtu": "1500",
        "ageing-time": "5m",
        "arp": "enabled",
        "arp-timeout": "auto",
        "auto-mac": "true",
        "comment": "Test loopback",
        "dhcp-snooping": "false",
        "disabled": "false",
        "dynamic": "false",
        "fast-forward": "true",
        "forward-delay": "15s",
        "igmp-snooping": "false",
        "l2mtu": "65535",
        "mac-address": "72:54:A8:E2:DA:AF",
        "max-learned-entries": "auto",
        "max-message-age": "20s",
        "mtu": "auto",
        "mvrp": "false",
        "name": "Loopback99",
        "port-cost-mode": "long",
        "priority": "0x8000",
        "protocol-mode": "rstp",
        "running": "true",
        "transmit-hold-count": "6",
        "vlan-filtering": "false"
      }
    ]
  },
  "execution_time_seconds": 0.01,
  "risk_assessment": {
    "risk": "low",
    "devices": 1,
    "reasons": [
      "Minor configuration change"
    ]
  }
}
```

#### Verify
```json
{
  "device": "R18M",
  "cli_style": "routeros",
  "cache_hit": false,
  "parsed": [
    {
      ".id": "*2",
      "actual-mtu": "1500",
      "default-name": "ether1",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:30:00",
      "link-downs": "0",
      "mac-address": "0C:00:54:82:36:00",
      "mtu": "1500",
      "name": "ether1",
      "running": "true",
      "rx-byte": "292968",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "3061",
      "tx-byte": "4272937",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "15760",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*3",
      "actual-mtu": "1500",
      "comment": "TO-R14C",
      "default-name": "ether2",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:30:00",
      "link-downs": "0",
      "mac-address": "AA:C1:AB:34:67:80",
      "mtu": "1500",
      "name": "ether2",
      "running": "true",
      "rx-byte": "779532",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "5760",
      "tx-byte": "1070958",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "8974",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*4",
      "actual-mtu": "1500",
      "comment": "TO-R17C",
      "default-name": "ether3",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:30:00",
      "link-downs": "0",
      "mac-address": "AA:C1:AB:4C:04:58",
      "mtu": "1500",
      "name": "ether3",
      "running": "true",
      "rx-byte": "801663",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "6110",
      "tx-byte": "1093746",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "9329",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*5",
      "actual-mtu": "1500",
      "comment": "TO-R19M",
      "default-name": "ether4",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:30:00",
      "link-downs": "0",
      "mac-address": "AA:C1:AB:45:1A:48",
      "mtu": "1500",
      "name": "ether4",
      "running": "true",
      "rx-byte": "1392052",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "12776",
      "tx-byte": "1127187",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "8866",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*6",
      "actual-mtu": "1500",
      "comment": "TO-R20M",
      "default-name": "ether5",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:30:00",
      "link-downs": "0",
      "mac-address": "AA:C1:AB:07:5C:EB",
      "mtu": "1500",
      "name": "ether5",
      "running": "true",
      "rx-byte": "1552732",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "15492",
      "tx-byte": "1827470",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "19518",
      "tx-queue-drop": "0",
      "type": "ether"
    },
    {
      ".id": "*C",
      "actual-mtu": "1500",
      "comment": "Test loopback",
      "disabled": "false",
      "dynamic": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "l2mtu": "65535",
      "last-link-up-time": "2026-02-25 13:46:54",
      "link-downs": "0",
      "mac-address": "72:54:A8:E2:DA:AF",
      "mtu": "auto",
      "name": "Loopback99",
      "running": "true",
      "rx-byte": "0",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "0",
      "tx-byte": "0",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "0",
      "tx-queue-drop": "0",
      "type": "bridge"
    },
    {
      ".id": "*1",
      "actual-mtu": "65536",
      "disabled": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "last-link-up-time": "2026-02-25 04:29:50",
      "link-downs": "0",
      "mac-address": "00:00:00:00:00:00",
      "mtu": "65536",
      "name": "lo",
      "running": "true",
      "rx-byte": "0",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "0",
      "tx-byte": "0",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "0",
      "tx-queue-drop": "0",
      "type": "loopback"
    },
    {
      ".id": "*7",
      "actual-mtu": "1500",
      "comment": "Loopback1",
      "disabled": "false",
      "dynamic": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "l2mtu": "65535",
      "last-link-up-time": "2026-02-25 04:30:07",
      "link-downs": "0",
      "mac-address": "6A:39:26:93:F9:9E",
      "mtu": "auto",
      "name": "lo1",
      "running": "true",
      "rx-byte": "0",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "0",
      "tx-byte": "767923",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "4461",
      "tx-queue-drop": "0",
      "type": "bridge"
    },
    {
      ".id": "*A",
      "actual-mtu": "1500",
      "comment": "Loopback3",
      "disabled": "false",
      "dynamic": "false",
      "fp-rx-byte": "0",
      "fp-rx-packet": "0",
      "fp-tx-byte": "0",
      "fp-tx-packet": "0",
      "l2mtu": "65535",
      "last-link-up-time": "2026-02-25 12:37:37",
      "link-downs": "0",
      "mac-address": "FA:F1:28:AB:AC:6C",
      "mtu": "auto",
      "name": "lo3",
      "running": "true",
      "rx-byte": "0",
      "rx-drop": "0",
      "rx-error": "0",
      "rx-packet": "0",
      "tx-byte": "97140",
      "tx-drop": "0",
      "tx-error": "0",
      "tx-packet": "567",
      "tx-queue-drop": "0",
      "type": "bridge"
    }
  ]
}
```

#### Delete
```json
{
  "R18M": {
    "transport_used": "rest",
    "result": [
      {
        "status": "deleted"
      }
    ]
  },
  "execution_time_seconds": 0.03,
  "risk_assessment": {
    "risk": "low",
    "devices": 1,
    "reasons": [
      "Minor configuration change"
    ]
  }
}
```
