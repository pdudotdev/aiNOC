Important notes about the configuration files:

- The router configurations in this folder are considered the **default configuration** for this network and in **this version of the project**, and they are **subject to change** with each new release, as the topology grows in complexity.

- Since these configurations are considered the **default configuration** for the current network version, they are going to be your fallback config whenever you use `containerlab redeploy -t lab.yml`

- Check the **MikroTik REST API** from your Ubuntu terminal with:
```
curl -u admin:admin http://172.20.20.218/rest/system/resource
curl -u admin:admin http://172.20.20.219/rest/interface
curl -u admin:admin http://172.20.20.219/rest/ip/route
curl -u admin:admin -X POST http://172.20.20.220/rest/tool/ping -H "Content-Type: application/json" -d '{"address":"172.16.77.9","count":4}'
```