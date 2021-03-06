#!/bin/bash
openssl genrsa -out ca.key 4096
openssl req -new -x509 -nodes -days 3650 -key ca.key -sha256 -extensions v3_ca -out ca.crt
openssl req -config site.conf -new -newkey rsa:4096 -nodes -keyout site.key -days 730 -out site.req
openssl x509 -sha256 -req -in site.req -CA ca.crt -CAkey ca.key -CAcreateserial -out site.crt -days 730 -extensions req_extensions -extensions cert_extensions -extfile site.conf