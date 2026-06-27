def int_to_base(n: int, base: int) -> str:
    """Converts a non-negative integer to a string in the specified base using uppercase digits."""
    if n == 0:
        return "0"
    
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if base > len(digits):
        raise ValueError(f"Base {base} exceeds maximum supported base ({len(digits)}).")
        
    result = ""
    curr = n
    while curr > 0:
        result = digits[curr % base] + result
        curr //= base
    return result

def base_to_int(s: str, base: int) -> int:
    """Converts a string representation in the specified base back to an integer."""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    val = 0
    for char in s.upper():
        digit_val = digits.index(char)
        if digit_val >= base:
            raise ValueError(f"Digit {char} invalid for base {base}.")
        val = val * base + digit_val
    return val

def encode_payload_for_hop(payload: str, next_codex: int) -> list:
    """Encodes an ASCII string payload into a list of base-converted tokens for the next hop."""
    encoded_list = []
    for char in payload:
        ascii_val = ord(char)
        base_val = int_to_base(ascii_val, next_codex)
        encoded_list.append(base_val)
    return encoded_list

def decode_payload_from_hop(encoded_stream: list, next_codex: int) -> str:
    """Decodes a list of base-converted tokens back into the original ASCII string payload."""
    decoded_chars = []
    for token in encoded_stream:
        ascii_val = base_to_int(str(token), next_codex)
        decoded_chars.append(chr(ascii_val))
    return "".join(decoded_chars)

def get_codex_numeric_tokens(payload: str, next_codex: int) -> list:
    """Returns the codex dialect translation tokens for a payload."""
    return encode_payload_for_hop(payload, next_codex)

def tokens_to_bitstream(tokens: list) -> str:
    """
    Implements Approach B: Ingests target base dialect array tokens and maps each digit's
    numerical value segment directly into standard 8-bit pure value binary blocks.
    Example: '200' -> digits 2, 0, 0 -> 00000010 00000000 00000000
    """
    digits_ref = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    blocks = []
    for token in tokens:
        clean_token = str(token).strip().upper()
        for char in clean_token:
            if char in digits_ref:
                digit_val = digits_ref.index(char)
                blocks.append(f"{int(digit_val):08b}")
    return " ".join(blocks).strip()


def get_void_transmission_bitstream(payload_or_tokens, next_codex: int = None) -> str:
    """
    Returns the Void Transmission Bitstream matching Approach B.
    Accepts either an encoded token list directly or a payload string + next_codex.
    """
    if isinstance(payload_or_tokens, list):
        return tokens_to_bitstream(payload_or_tokens)
    elif isinstance(payload_or_tokens, str) and next_codex is not None:
        tokens = encode_payload_for_hop(payload_or_tokens, next_codex)
        return tokens_to_bitstream(tokens)
    else:
        raise ValueError("Invalid parameters for get_void_transmission_bitstream")
