import gzip, base64, json

def decode_gzip_response_body(response_body):
    decoded_data = base64.b64decode(response_body)
    decompressed_binary = gzip.decompress(decoded_data)
    decompressed_text = decompressed_binary.decode('utf-8')
    decompressed_json = json.loads(decompressed_text)

    return decompressed_json