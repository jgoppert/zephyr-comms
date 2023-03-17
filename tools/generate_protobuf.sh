#!/bin/bash
protoc -I ../protobuf_ethernet/src/ simple.proto --python_out=.
