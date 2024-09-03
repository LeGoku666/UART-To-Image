import serial
import serial.tools.list_ports
import numpy as np
from PIL import Image, ImageOps
import os
import platform
import time
import threading

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in ports:
        print(f"{port}: {desc} [{hwid}]")
    return ports

def reverse_bits(byte):
    reversed_byte = 0
    for i in range(8):
        reversed_byte |= ((byte >> i) & 1) << (7 - i)
    return reversed_byte

def bits_to_image(bits, width, height):
    array = np.array(bits, dtype=np.uint8).reshape((width, height))
    array = 1 - array  # Invert the bits: 0 becomes 1, and 1 becomes 0
    
    img = Image.fromarray(array * 255)  # Convert bits to values 0 or 255
    img = img.transpose(Image.ROTATE_270)  # Rotate by 270 degrees (i.e., 90 degrees to the left)
    img = ImageOps.mirror(img)  # Horizontal mirror flip
    
    return img

def open_image(filename):
    if platform.system() == "Windows":
        os.startfile(filename)
    elif platform.system() == "Darwin":
        os.system(f"open {filename}")
    else:
        os.system(f"xdg-open {filename}")

def process_image(bits, height):
    if len(bits) % height != 0:
        print("Incomplete columns. Adding padding to achieve full columns.")
        bits.extend([0] * (height - (len(bits) % height)))
    
    width = len(bits) // height  # The width of the image is the number of full columns

    img = bits_to_image(bits, width, height)
    img.save("received_image.png")  # Save the file in the current directory
    
    image_size = f"w:{width}, h:{height} pixels"
    print(f"Image saved as received_image.png ({image_size}) with {len(bits)} bits received.")

    open_image("received_image.png")

def read_from_serial(port, baudrate, height, packet_size):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f'Opened {port} at {baudrate} baudrate.')
    except serial.SerialException as e:
        print(f'Failed to open {port}: {e}')
        return
    
    buffer = bytearray()
    bits = []
    total_bits_received = 0
    last_read_time = time.time()
    data_incoming = False

    try:
        while True:
            if ser.in_waiting > 0:
                if not data_incoming:
                    print("Data incoming... waiting for end of transmission.")
                    data_incoming = True

                data = ser.read(ser.in_waiting)
                buffer.extend(data)
                last_read_time = time.time()
                
                while len(buffer) >= packet_size:
                    packet = buffer[:packet_size]
                    buffer = buffer[packet_size:]
                    packet_bits = []
                    for byte in packet:
                        reversed_byte = reverse_bits(byte)
                        for i in range(8):
                            bit = (reversed_byte >> (7 - i)) & 1
                            packet_bits.append(bit)
                    
                    packet_bits = packet_bits[1:-1]
                    bits.extend(packet_bits)
                    total_bits_received += len(packet_bits)

            elif time.time() - last_read_time > 0.9 and bits:
                print("Processing image...")
                process_image(bits, height)
                print("Transmission ended. Waiting for new data...")

                # Clear buffers and counters
                buffer.clear()
                bits.clear()
                total_bits_received = 0
                data_incoming = False
                last_read_time = time.time()
            else:
                time.sleep(0.1)  # Add a small delay to avoid overloading the CPU

    except KeyboardInterrupt:
        print('Stopping the script.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        ser.close()
        print('Closed the serial port.')

def main():
    print("Available ports:")
    ports = list_serial_ports()

    if not ports:
        print("No serial ports found.")
        return

    port = input("Enter the port you want to use (e.g., COM4 or /dev/ttyUSB0): ")
    baudrate = 115200
    packet_size = 64  # 64 bytes = 512 bits
    height = 510

    serial_thread = threading.Thread(target=read_from_serial, args=(port, baudrate, height, packet_size))
    serial_thread.daemon = True  # Set the thread as a daemon so it terminates when the main thread ends
    serial_thread.start()

    try:
        while True:
            time.sleep(1)  # Slow down the main thread to avoid overloading the CPU.
    except KeyboardInterrupt:
        print('Stopping the main thread.')

if __name__ == '__main__':
    main()
