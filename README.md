# qrcodea# QR Code Generator & Scanner 🔲

A CLI tool for generating and scanning QR codes with features like batch generation and automatic file uploads.

## Features

- Generate QR codes with custom data
- Scan QR codes from local files or URLs
- Batch generation of multiple QR codes
- Automatic upload to uguu.se (24-hour hosting)
- ASCII preview of generated QR codes
- Progress tracking and rich CLI interface

## Installation

```bash
git clone https://github.com/notsopreety/qrcode.git
cd qrcode
pip install -r requirements.txt
```

### Additional Requirements
- For QR scanning, you need to install `zbar`:
  - Ubuntu/Debian: `sudo apt-get install zbar-tools`
  - macOS: `brew install zbar`
  - Windows: Download from [here](http://zbar.sourceforge.net/)

## Usage

### Interactive Mode
```bash
python qr.py
```

### Command Line Arguments
```bash
# Generate a QR code
python qr.py --generate "Your data here"

# Scan a QR code
python qr.py --scan "path/to/qrcode.png"
python qr.py --scan "https://example.com/qrcode.png"

# Batch generate QR codes
python qr.py --batch
```

## Features Details

1. **QR Generation**
   - Error correction
   - Custom filenames
   - ASCII preview
   - Automatic upload to uguu.se

2. **QR Scanning**
   - Local file support
   - URL support
   - Multiple QR code detection

3. **Batch Operations**
   - Multiple QR codes in one go
   - Custom base filenames
   - Bulk uploading

## Contributing

Feel free to open issues and pull requests!

## License

MIT License

## Author

[notsopreety](https://github.com/notsopreety)
