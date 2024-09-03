# Serial Image Processing in Python

## Overview

This Python script is designed to read data from a serial port, process the received data into an image, and then save and display the image. The script performs tasks such as listing available serial ports, reading data in a threaded environment, reversing the bits of each byte received, constructing an image from these bits, and finally, displaying the image.

## Features

- **Serial Port Management**: List and select available serial ports for data reading.
- **Bit Manipulation**: Reverse bits of each byte to correct data orientation.
- **Image Construction**: Convert serial data bits into a grayscale image.
- **Threaded Execution**: Utilize threading to keep the main program responsive while reading serial data.
- **Cross-Platform Support**: Open saved images using the default viewer on Windows, macOS, or Linux.

## Modules and Libraries

- **serial & serial.tools.list_ports**: Serial communication and port listing.
- **numpy**: Array manipulation for reshaping data into image form.
- **PIL (Pillow)**: Image creation, manipulation, and saving.
- **os**: OS-specific file handling.
- **platform**: Detects the operating system for file operations.
- **time**: Time functions for delays and timeouts.
- **threading**: Manage serial data reading in a separate thread.

## Installation

Ensure that the required libraries are installed:

```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Script**:
   - The script will list available serial ports and prompt you to select one.
   - It will then start reading data from the selected port, process the incoming bits, and create an image.

2. **Stopping the Script**:
   - Use `Ctrl+C` to stop the script at any time.

3. **Output**:
   - The processed image is saved as `received_image.png` and opened automatically with the default image viewer.

## Function Descriptions

- **`list_serial_ports()`**: Lists all available serial ports on the machine.
- **`reverse_bits(byte)`**: Reverses the bits of a given byte.
- **`bits_to_image(bits, width, height)`**: Converts a list of bits into a grayscale image, rotates, and mirrors it for correct orientation.
- **`open_image(filename)`**: Opens an image file using the default viewer based on the operating system.
- **`process_image(bits, height)`**: Processes a list of bits, creates and saves an image as `received_image.png`.
- **`read_from_serial(port, baudrate, height, packet_size)`**: Manages the serial port data reading, reversing bits, and constructing an image.
- **`main()`**: The entry point of the script, lists available serial ports, prompts for selection, and starts the serial data reading in a thread.

## Notes

- **Threading**: Ensures responsive user interaction by reading serial data in a separate thread.
- **Bit Manipulation**: Handles specific bit operations to format the data correctly for image construction.
- **Image Orientation**: Adjusts the image orientation to match the expected visual output based on the source data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

This script is ideal for scenarios where serial data is transmitted in bits that need to be reconstructed into images, such as from embedded systems or custom hardware interfaces.


















