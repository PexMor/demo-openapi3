# demo-openapi3

Conceptual demo of simple openapi3 using conexion for quick prototyping.

* [API at glance](https://pexmor.github.io/demo-openapi3/elements.html)
* [Github pages](https://pexmor.github.io/demo-openapi3/)

## Curl tests

__JSON__

```bash
curl -X 'POST' \
  'http://localhost:8080/v1/json/user_007%40example.com' \
  -H 'accept: */*' \
  -H 'X-Auth: abcd' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": "IyEvYmluL2Jhc2gKCkZMQVNLX0RFQlVHPTEgTE9HTEVWRUw9REVCVUcgcHl0aG9uMyBhcGlTcnYucHkK",
  "hash": "ce94a9e855cdaa04d95da193611236b6adec16256865662a3d2105858b00fb42",
  "hash_type": "sha256",
  "vars": {
    "infra": "one",
    "ipv4": [
      "1.2.3.4/32"
    ],
    "ssh_pub_key": [
      "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDL...= your-id",
      "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDL...= your-id2"
    ]
  }
}'
```

__Multipart form__

```bash
curl -X 'POST' \
  'http://localhost:8080/v1/multipart/user_007%40example.com' \
  -H 'accept: */*' \
  -H 'X-Auth: abcd' \
  -H 'Content-Type: multipart/form-data' \
  -F 'data=@LICENSE;type=text/plain' \
  -F 'hash=ce94a9e855cdaa04d95da193611236b6adec16256865662a3d2105858b00fb42' \
  -F 'hash_type=sha256' \
  -F 'vars={
  "infra": "one",
  "ipv4": [
    "1.2.3.4/32"
  ],
  "ssh_pub_key": [
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDL...= your-id",
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDL...= your-id2"
  ]
}'
```
