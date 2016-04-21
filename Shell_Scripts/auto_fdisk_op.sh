#!/bin/bash
fdisk $1 << EOF
n
p
1


t
8e
w
EOF
