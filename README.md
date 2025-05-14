# Nagios Lock Monitor Plugin

A Nagios plugin to monitor the number of locks on the system as listed in `/proc/locks`.

## Features

- Monitors the number of POSIX or FLOCK locks on the system
- Configurable warning and critical thresholds
- Available in both Python and Bash versions

## Requirements

### Python Version
- Python 3.x

### Bash Version
- Bash shell
- GNU grep

## Installation

1. Copy either `check_locks.py` or `check_locks.sh` to your Nagios plugins directory (typically `/usr/lib/nagios/plugins/`)
2. Make the file executable:

```bash
chmod +x /usr/lib/nagios/plugins/check_locks.py
# or
chmod +x /usr/lib/nagios/plugins/check_locks.sh
```

## Usage

### Python Version

```bash
./check_locks.py --type=POSIX --warning=50 --critical=100
```

### Bash Version

```bash
./check_locks.sh --type=POSIX --warning=50 --critical=100
```

### Parameters

- `--type`: Type of lock to monitor. Must be either `POSIX` or `FLOCK`.
- `--warning`: Warning threshold for the number of locks.
- `--critical`: Critical threshold for the number of locks.

## Example Output

- `OK: The system has 30 POSIX locks, which is within the normal range`
- `WARNING: The system has 55 POSIX locks, exceeding the warning threshold (50)`
- `CRITICAL: The system has 110 POSIX locks, exceeding the critical threshold (100)`

## Nagios Configuration Example

### Command Definition

```
define command{
    command_name    check_locks
    command_line    $USER1$/check_locks.py --type=$ARG1$ --warning=$ARG2$ --critical=$ARG3$
}
```

### Service Definition

```
define service{
    use                     generic-service
    host_name               localhost
    service_description     POSIX Locks
    check_command           check_locks!POSIX!50!100
}
```

## License

MIT

## Author

Created for Nagios monitoring systems. 