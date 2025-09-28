# Secret Extraction Tool (sex)

A powerful multi-threaded tool for scanning directories and extracting secrets, API keys, tokens, and other sensitive information from various file types including APK, HTML, source code, and more.

> **Note**: This tool is based on the original [secretx](https://github.com/xyele/secretx) script with significant improvements.

## Features

- **Multi-threaded scanning**: Process multiple files simultaneously for faster results
- **Comprehensive pattern matching**: Pre-configured with patterns for 30+ common secret types (Slack tokens, AWS keys, API tokens, etc.)
- **Colorful output**: Easy-to-read colored console output (can be disabled with `--colorless`)
- **Automatic dependency installation**: Installs required packages automatically on first run
- **Cross-platform compatibility**: Works on Windows, Linux, and macOS
- **Error-resilient**: Gracefully handles file encoding issues and permission errors

## Installation

### Prerequisites
- Python 3.6 or higher

### Quick Start
1. Download or clone the repository
2. Navigate to the tool's directory
3. Run the tool - dependencies will be installed automatically

## Usage

### Basic Command
```bash
python sex.py --dir /path/to/scan --threads 10
```

### Command Line Arguments
| Argument | Description | Required |
|----------|-------------|----------|
| `--dir` | Directory to scan recursively | Yes |
| `--threads` | Number of parallel threads to use | Yes |
| `--colorless` | Disable colored output | No |

### Examples

**Scan an Android APK extraction directory:**
```bash
python sex.py --dir '/home/user/apk_extracted/' --threads 20
```

**Scan a web application source code with colorless output:**
```bash
python sex.py --dir '/var/www/html/' --threads 8 --colorless
```

**Scan a Windows directory:**
```bash
python sex.py --dir 'C:\Projects\app\' --threads 12
```

## How It Works

### 1. Pattern Loading
The tool loads detection patterns from `patterns.json`, which contains regular expressions for identifying various types of secrets including:
- API keys (Google, AWS, Stripe, etc.)
- OAuth tokens
- Database connection strings
- Private keys
- Authentication tokens

### 2. File Discovery
The tool recursively walks through all subdirectories of the specified path, collecting file paths for scanning.

### 3. Multi-threaded Processing
- Files are distributed across the specified number of threads
- Each file is read with UTF-8 encoding (errors are ignored)
- File contents are scanned against all loaded patterns
- Matches are collected in a thread-safe manner

### 4. Result Presentation
When a secret is found, the tool displays:
- **Pattern Name**: Type of secret detected (e.g., "AWS Access Key")
- **Key**: The actual matched sensitive string
- **URL**: File path where the secret was found

Results are printed in random colors for easy visual scanning (unless `--colorless` is specified).

## Pattern Configuration

The tool uses `patterns.json` for secret detection. You can customize this file to add new patterns or modify existing ones.

### Pattern Structure
Each pattern consists of a name and a regular expression:
```json
{
    "Pattern Name": "regular_expression",
    "Slack Token": "xox[pboa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}"
}
```

### Adding Custom Patterns
1. Edit `patterns.json`
2. Add your pattern following the existing format
3. Save the file and run the tool

## Performance Optimization

- **Thread Count**: Adjust based on your CPU cores (typically 2x core count)
- **Large Directories**: Start with fewer threads to test, then increase
- **Network Drives**: Use fewer threads for network-mounted directories

## Error Handling

The tool includes comprehensive error handling:
- **File Permission Errors**: Skipped silently
- **Encoding Issues**: Handled with error ignoring
- **Keyboard Interrupts** (Ctrl+C): Graceful shutdown
- **Missing Dependencies**: Automatic installation on first run

## Security Considerations

⚠️ **Important**: This tool is designed for legitimate security testing purposes only. Always ensure you have proper authorization before scanning systems or files.

## Troubleshooting

**Dependencies not installing automatically:**
```bash
pip install -r requirements.txt
```

**Python 2.x compatibility:**
This tool requires Python 3.6 or higher.

**Unicode errors:**
The tool automatically handles encoding issues by ignoring errors.

## Support

For issues and feature requests, please check the original [secretx](https://github.com/xyele/secretx) repository or create an issue in this project's repository.

## License

This tool is based on the original secretx script. Please refer to the original repository for licensing information.

