#!/usr/bin/env bash

# ==============================================================================
# push_swap automated test suite
# ==============================================================================
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0;3m' # No Color
BOLD='\033[1m'
UNDERLINE='\033[4m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0

print_header() {
    echo -e "\n${BOLD}${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
    ((TESTS_PASSED++))
    ((TESTS_RUN++))
}

print_failure() {
    echo -e "${RED}✗ $1${NC}"
    ((TESTS_RUN++))
}

# Helper to check if valgrind is available
VALGRIND_CMD=""
if command -v valgrind &> /dev/null; then
    VALGRIND_CMD="valgrind --leak-check=full --show-leak-kinds=all --error-limit=no --error-exitcode=42 -q"
fi

# 1. Compilation Check
print_header "1. Compilation Check"
make re > /dev/null
if [ $? -eq 0 ] && [ -f ./push_swap ] && [ -f ./checker ]; then
    print_success "Compilation completed successfully with 'make re'."
else
    print_failure "Compilation failed."
    exit 1
fi

# 2. Error Handling Check
print_header "2. Error Handling Check"

run_error_test() {
    local args="$1"
    local desc="$2"
    
    # Test push_swap stderr
    local ps_err
    ps_err=$(./push_swap $args 2>&1 >/dev/null)
    local ps_exit=$?
    
    # Test checker stderr
    local ch_err
    ch_err=$(./checker $args 2>&1 >/dev/null)
    local ch_exit=$?
    
    if [ "$ps_err" = "Error" ] && [ $ps_exit -ne 0 ] && [ "$ch_err" = "Error" ] && [ $ch_exit -ne 0 ]; then
        print_success "Error handled correctly for: $desc (both exited with non-zero code and printed 'Error')"
    else
        print_failure "Failed error handling for: $desc"
        echo "  push_swap: exit=$ps_exit, stderr='$ps_err'"
        echo "  checker:   exit=$ch_exit, stderr='$ch_err'"
        exit 1
    fi
}

run_error_test "1 2 3 1" "Duplicate numbers"
run_error_test "1 a 3" "Non-numeric input"
run_error_test "2147483648" "Integer overflow (> INT_MAX)"
run_error_test "-2147483649" "Integer underflow (< INT_MIN)"

# Test empty inputs (should not print Error, should exit 0)
ps_out=$(./push_swap "" 2>&1)
ps_exit=$?
ch_out=$(./checker "" 2>&1)
ch_exit=$?

if [ $ps_exit -eq 0 ] && [ -z "$ps_out" ] && [ $ch_exit -eq 0 ] && [ -z "$ch_out" ]; then
    print_success "Empty input handled correctly (exited 0 with no output)"
else
    print_failure "Empty input failed (expected exit 0, no output)"
    echo "  push_swap: exit=$ps_exit, out='$ps_out'"
    echo "  checker: exit=$ch_exit, out='$ch_out'"
    exit 1
fi

# 3. Identity (Sorted) Test
print_header "3. Identity (Already Sorted) Check"

ps_out=$(./push_swap 42 2>&1)
ps_exit=$?
if [ $ps_exit -eq 0 ] && [ -z "$ps_out" ]; then
    print_success "Identity test for 1 element passed (0 operations)"
else
    print_failure "Identity test for 1 element failed"
    exit 1
fi

ps_out=$(./push_swap 1 2 3 4 5 2>&1)
ps_exit=$?
if [ $ps_exit -eq 0 ] && [ -z "$ps_out" ]; then
    print_success "Identity test for 5 elements passed (0 operations)"
else
    print_failure "Identity test for 5 elements failed"
    exit 1
fi

# 4. Correctness & Performance Benchmarks
print_header "4. Correctness & Performance Benchmarks"

# Helper to generate random non-duplicate integers
generate_random_list() {
    local size=$1
    if command -v ruby &> /dev/null; then
        ruby -e "puts (1..$size).to_a.shuffle.join(' ')"
    elif command -v python3 &> /dev/null; then
        python3 -c "import random; l = list(range(1, $size + 1)); random.shuffle(l); print(' '.join(map(str, l)))"
    else
        # Fallback using shuf
        shuf -i 1-"$size" | tr '\n' ' '
    fi
}

run_benchmarks() {
    local size=$1
    local iterations=$2
    local threshold_max=$3
    local threshold_5pts=$4
    
    local total_ops=0
    local max_ops=0
    local min_ops=999999
    local pass_count=0
    
    echo -e "${BOLD}Running Benchmark for Size $size ($iterations iterations)...${NC}"
    
    for ((i=1; i<=iterations; i++)); do
        local arg
        arg=$(generate_random_list "$size")
        
        # Execute push_swap
        local ops
        ops=$(./push_swap $arg)
        local ops_count
        ops_count=$(echo -n "$ops" | grep -c -E "^(sa|sb|ss|pa|pb|ra|rb|rr|rra|rrb|rrr)$")
        
        # Validate sorting with checker
        local checker_res
        checker_res=$(echo "$ops" | ./checker $arg)
        
        if [ "$checker_res" != "OK" ]; then
            print_failure "Incorrect sort on iteration $i for size $size! Checker returned: $checker_res"
            echo "Arguments: $arg"
            exit 1
        fi
        
        total_ops=$((total_ops + ops_count))
        [ $ops_count -gt $max_ops ] && max_ops=$ops_count
        [ $ops_count -lt $min_ops ] && min_ops=$ops_count
        
        if [ -n "$threshold_max" ] && [ $ops_count -gt $threshold_max ]; then
            print_failure "Iteration $i for size $size exceeded maximum allowed limit! Ops: $ops_count (Limit: $threshold_max)"
            echo "Arguments: $arg"
            exit 1
        fi
    done
    
    local avg_ops=$((total_ops / iterations))
    echo -e "  -> Min operations: $min_ops"
    echo -e "  -> Max operations: $max_ops"
    echo -e "  -> Avg operations: ${BOLD}$avg_ops${NC}"
    
    if [ -n "$threshold_5pts" ]; then
        if [ $avg_ops -le $threshold_5pts ]; then
            print_success "Size $size benchmark passed! Average: $avg_ops ops (5/5 threshold: <= $threshold_5pts)"
        else
            echo -e "${YELLOW}⚠ Size $size benchmark passed correctness but failed 5/5 score. Avg: $avg_ops ops (5/5 threshold: <= $threshold_5pts)${NC}"
            ((TESTS_RUN++))
        fi
    else
        print_success "Size $size benchmark passed! Max ops recorded: $max_ops (Allowed limit: $threshold_max)"
    fi
}

# Run correctness & performance checks
run_benchmarks 3 20 3      # 3 numbers, limit: 3 ops
run_benchmarks 5 20 12     # 5 numbers, limit: 12 ops
run_benchmarks 100 20 1500 700 # 100 numbers, limit: <1500, 5/5 threshold: <700
run_benchmarks 500 10 11500 5500 # 500 numbers, limit: <11500, 5/5 threshold: <5500

# 5. Memory Leak Verification
print_header "5. Memory Leak Verification (Valgrind)"

if [ -n "$VALGRIND_CMD" ]; then
    val_arg="3 2 1 5 4"
    echo -e "Running valgrind on push_swap..."
    $VALGRIND_CMD ./push_swap $val_arg > /dev/null
    if [ $? -eq 0 ]; then
        print_success "No leaks/errors found in push_swap."
    else
        print_failure "Leaks/errors found in push_swap."
        exit 1
    fi
    
    echo -e "Running valgrind on checker..."
    ps_ops=$(./push_swap $val_arg)
    echo "$ps_ops" | $VALGRIND_CMD ./checker $val_arg > /dev/null
    if [ $? -eq 0 ]; then
        print_success "No leaks/errors found in checker."
    else
        print_failure "Leaks/errors found in checker."
        exit 1
    fi
else
    echo -e "${YELLOW}Valgrind not installed. Skipping memory leak checks.${NC}"
fi

# Summary
print_header "Summary"
echo -e "Passed: ${GREEN}$TESTS_PASSED / $TESTS_RUN${NC}"
if [ $TESTS_PASSED -eq $TESTS_RUN ]; then
    echo -e "${GREEN}${BOLD}ALL TESTS PASSED SUCCESSFULLY!${NC}"
    exit 0
else
    echo -e "${RED}${BOLD}SOME TESTS FAILED!${NC}"
    exit 1
fi
