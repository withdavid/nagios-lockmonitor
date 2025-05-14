#!/usr/bin/env python3
"""
Nagios plugin to monitor the number of locks on the system.
"""

import argparse
import sys
import os

# Nagios return codes
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Check number of system locks')
    parser.add_argument('--type', required=True, choices=['POSIX', 'FLOCK'],
                        help='Type of lock to monitor (POSIX or FLOCK)')
    parser.add_argument('--warning', required=True, type=int,
                        help='Warning threshold for number of locks')
    parser.add_argument('--critical', required=True, type=int,
                        help='Critical threshold for number of locks')
    
    return parser.parse_args()

def count_locks(lock_type):
    """Count the number of locks of specified type in /proc/locks."""
    try:
        if not os.path.exists('/proc/locks'):
            print("UNKNOWN: /proc/locks file not found")
            sys.exit(UNKNOWN)
            
        with open('/proc/locks', 'r') as f:
            locks_content = f.readlines()
        
        lock_count = 0
        for line in locks_content:
            # The lock type is the 3rd field (index 2) in each line
            fields = line.strip().split()
            if len(fields) > 2 and fields[2] == lock_type:
                lock_count += 1
                
        return lock_count
    except Exception as e:
        print(f"UNKNOWN: Error reading /proc/locks - {str(e)}")
        sys.exit(UNKNOWN)

def main():
    args = parse_arguments()
    
    # Normalize lock types to match /proc/locks format
    lock_type_map = {
        'POSIX': 'POSIX',
        'FLOCK': 'FLOCK'
    }
    
    # Get the normalized lock type
    lock_type = lock_type_map[args.type]
    
    # Count locks of the specified type
    lock_count = count_locks(lock_type)
    
    # Check thresholds and return appropriate status
    if lock_count >= args.critical:
        print(f"CRITICAL: The system has {lock_count} {args.type} locks, exceeding the critical threshold ({args.critical})")
        sys.exit(CRITICAL)
    elif lock_count >= args.warning:
        print(f"WARNING: The system has {lock_count} {args.type} locks, exceeding the warning threshold ({args.warning})")
        sys.exit(WARNING)
    else:
        print(f"OK: The system has {lock_count} {args.type} locks, which is within the normal range")
        sys.exit(OK)

if __name__ == "__main__":
    main() 