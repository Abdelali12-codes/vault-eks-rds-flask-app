# enable database secret engine (mysql)
```
vault secrets enable database

vault write database/config/rds-mysql \
    plugin_name=mysql-database-plugin \
    connection_url="{{username}}:{{password}}@tcp(database.civprmsgnbew.us-west-2.rds.amazonaws.com:3306)/" \
    allowed_roles="dbrole" \
    username="demo" \
    password="demodemo"
```
# Create a database secrets engine role named readonly
```
vault write database/roles/dbrole \
    db_name=rds-mysql \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';GRANT SELECT ON *.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"
    
vault read database/creds/dbrole
```

# enable kubernetes auth method

```
vault auth enable kubernetes
KUBERNETES_PORT_443_TCP_ADDR=$(aws eks describe-cluster --name eks-cluster --query "cluster.endpoint" --output text)  
vault write auth/kubernetes/config \
    kubernetes_host="$KUBERNETES_PORT_443_TCP_ADDR:443"
```

# create vault policy
```
vault policy write flaskapp - <<EOF
path "database/creds/dbrole" {
  capabilities = ["read"]
}
EOF
```
# create auth role 
```
vault write auth/kubernetes/role/flaskapp \
      bound_service_account_names=rds-sa \
      bound_service_account_namespaces=default \
      policies=flaskapp \
      ttl=24h

```