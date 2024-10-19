import sys
import struct
from binascii import *

png_file_signature = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
png_file_footer = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
chunklist = []

def png_ihdr_info(png_path):
    global png_file_signature
        
    try:
        with open(png_path, 'rb') as f:
            # PNG File Header Signature
            signature = f.read(8)
            if signature == png_file_signature:
                edit_signature = ' '.join([signature.hex()[i:i+2] for i in range(0, len(signature.hex()), 2)])
                print(f'\n# File Header signature (Magic Number)')
                print(f'{edit_signature}\n')
            else:
                print(f'PNG File Signature is not valid.')
                return False
                
            # PNG File Length
            length = f.read(4)
            
            # PNG Chunk Type
            chunk_type = f.read(4)
            
            # IHDR info
            print(f'# IHDR info')
            
            # IHDR Width
            width = f.read(4)
            int_width = int.from_bytes(width, byteorder='big')
            print(f'Width: {int_width}')
            
            # IHDR Height 
            height = f.read(4)
            int_height = int.from_bytes(height, byteorder='big')
            print(f'Height: {int_height}')
            
            # IHDR Bit Depth
            depth = f.read(1)
            int_depth = int.from_bytes(depth, byteorder='big')
            print(f'Bit depth: {int_depth}')
            
            # IHDR Color Type
            color_type = f.read(1)
            int_color_type = int.from_bytes(color_type, byteorder='big')
            print(f'Color Type: {int_color_type}')
            
            # IHDR Compression method
            compression_method = f.read(1)
            int_compression_method = int.from_bytes(compression_method, byteorder='big')
            print(f'Compression method: {int_compression_method}')
            
            # Filter method
            filter_method = f.read(1)
            int_filter_method = int.from_bytes(filter_method, byteorder='big')
            print(f'Filter method: {int_filter_method}')
            
            # Interlace method
            interface_method = f.read(1)
            int_interface_method = int.from_bytes(interface_method, byteorder='big')
            print(f'Interlace method: {int_interface_method}\n')
            
            return True
            
    except FileNotFoundError:
        print(f"File {png_path} can't find.")
        return False
    
def chunk_list(png_path):
    global png_file_signature
    global png_file_footer
    
    try:
        with open(png_path, 'rb') as f:
            
            f.seek(0)
            
            # PNG File Header Signature
            signature = f.read(8)
            if signature != png_file_signature:
                print(f'PNG File Signature is not valid.')
                return False
            
            while True:
                
                length = f.read(4)
                
                if len(length) == 0:
                    break  
                
                chunk_length = int.from_bytes(length, byteorder='big')
                chunk_type = f.read(4)
                chunklist.append(chunk_type)
                chunk_data = f.read(chunk_length)
                chunk_crc = f.read(4)
                
                if chunk_type == b'IEND':
                    footer = chunk_type + chunk_crc
                    edit_footer = ' '.join([footer.hex()[i:i+2] for i in range(0, len(signature.hex()), 2)])
                    
            print(f"# Chunk list")
            print(f"{chunklist}\n")
            
            print(f'# File Footer signature')
            print(f'{edit_footer}\n')
            
            return True
            
    except FileNotFoundError:
        print(f"File {png_path} can't find.")
        return False


if __name__=='__main__':
    # usage
    if len(sys.argv) != 2:
        print("usage : python ./png_parse.py ./png_path")
        sys.exit()

    # png path
    png_path = sys.argv[1]
    
    # def Check
    png_ihdr_info_CHK = png_ihdr_info(png_path)
    chunk_list_CHK = chunk_list(png_path)
    
    if png_ihdr_info_CHK and chunk_list_CHK:
        print(f'Chunk 영역 추출 완료.\n')
        print(f'프로그램 종료.')
    
