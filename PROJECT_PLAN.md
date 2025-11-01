# Auralis - Core Vulnerability Detection

## 1. Re-entrancy Attacks
- Detect external calls before state changes
- Identify .call() and .transfer() patterns

## 2. Integer Overflow/Underflow
- Detect unchecked arithmetic operations
- Identify potential overflow in loops

## 3. Access Control Violations
- Detect missing authorization checks
- Identify public functions that should be private

## 4. Unchecked Return Values
- Detect low-level calls without success checks
- Identify missing error handling