#!/bin/sh

cert=`openssl x509 -noout -modulus -in $1 | openssl md5`
key=`openssl rsa -noout -modulus -in $2 | openssl md5`
csr=`openssl req -noout -modulus -in $3 | openssl md5`

echo "cert is $cert"
echo "key is $key"
echo "csr is $csr"

if [ "$cert" = "$key" ] && [ "$key" = "$csr" ];
then
    echo "All 3 match"
else
    echo "NOT A MATCH $1 $2 $3"
    exit 1
fi