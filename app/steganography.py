from PIL import Image
import numpy as np

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text) + '00000000'

def encode_image(image_path, text):
    try:
        # Open and prepare image
        img = Image.open(image_path)
        img_array = np.array(img.convert('RGB'), dtype=np.uint8)
        
        # Prepare binary message
        binary = text_to_binary(text)
        binary_length = len(binary)
        
        if binary_length > img_array.size:
            raise ValueError("Text too long for this image")
        
        # Convert message to bits
        binary_data = np.array([int(bit) for bit in binary], dtype=np.uint8)
        
        # Create working copy
        modified_array = img_array.copy()
        binary_index = 0
        
        # Process pixels
        height, width = modified_array.shape[:2]
        for y in range(height):
            for x in range(width):
                for c in range(3):
                    if binary_index < binary_length:
                        # Safely modify LSB
                        pixel_value = int(modified_array[y, x, c])
                        new_value = (pixel_value & 0xFE) | binary_data[binary_index]
                        modified_array[y, x, c] = np.uint8(new_value)
                        binary_index += 1
        
        # Convert back to image
        return Image.fromarray(modified_array)
        
    except Exception as e:
        raise Exception(f"Encoding failed: {str(e)}")

def decode_image(image_path):
    try:
        # Read image
        img = Image.open(image_path)
        img_array = np.array(img.convert('RGB'), dtype=np.uint8)
        
        # Extract bits
        binary = []
        height, width = img_array.shape[:2]
        
        # Collect LSBs
        for y in range(height):
            for x in range(width):
                for c in range(3):
                    bit = img_array[y, x, c] & 1
                    binary.append(str(bit))
                    
                    # Check for message end
                    if len(binary) >= 8 and len(binary) % 8 == 0:
                        # Convert current segment to string
                        current_binary = ''.join(binary[-32:])
                        if '00000000' in current_binary:
                            # Convert all collected bits to message
                            full_binary = ''.join(binary)
                            message = binary_to_text(full_binary)
                            if message:
                                return message
        
        return "No message found"
        
    except Exception as e:
        raise Exception(f"Decoding failed: {str(e)}")

def binary_to_text(binary):
    message = []
    try:
        # Process complete bytes
        for i in range(0, len(binary)-7, 8):
            byte = binary[i:i+8]
            if byte == '00000000':
                break
            char_code = int(byte, 2)
            if 32 <= char_code <= 126:  # Printable ASCII
                message.append(chr(char_code))
    except Exception:
        pass
    
    return ''.join(message) if message else ''