# Cerebri

## Goal
The goal of Cerebri is to create a minimalistic flight controller that it developed for:
* Verification
	* Minimum Lines of Code
	* Use C only
	* Generated estimator/control code with tracking error bound proofs
* Development
	* Simple development using vscode and dev containers
	* Documented debugging process

At the completion of this project, we hope to have a flight controller that is useful
for research and can rapidly deploy new algorithms that can be verified.

## Design Decisions

* A point to point communication mechanism must be created for the onboard computer. It is assumed that all complicated decisions involving multiple vehicles will be handled by an onboard computer. Therefore it is likely that an ethernet stack will not be used. We are investigating protobuf serialization and framing techniques that will result in the most efficient and maintainable code.

## Quick Start

On host
```bash
code .
```

### Protobuf UART Test
In container terminal within vscode
```bash
west build -b native_posix protobuf_uart -p
```

### Ethernet Test
In container terminal within vscode
```bash
west build -b native_posix eth_native_posix -p
```
