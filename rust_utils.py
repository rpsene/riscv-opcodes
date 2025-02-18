import logging
import pprint

from constants import *

# from shared_utils import overlaps, overlap_allowed, extension_overlap_allowed, instruction_overlap_allowed, process_enc_line, same_base_isa, add_segmented_vls_insn, expand_nf_field
from shared_utils import *

pp = pprint.PrettyPrinter(indent=2)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:: %(message)s")


def make_rust(instr_dict: InstrDict):
    mask_match_str = ""
    for i in instr_dict:
        mask_match_str += f'const MATCH_{i.upper().replace(".","_")}: u32 = {(instr_dict[i]["match"])};\n'
        mask_match_str += f'const MASK_{i.upper().replace(".","_")}: u32 = {(instr_dict[i]["mask"])};\n'
    for num, name in csrs + csrs32:
        mask_match_str += f"const CSR_{name.upper()}: u16 = {hex(num)};\n"
    for num, name in causes:
        mask_match_str += (
            f'const CAUSE_{name.upper().replace(" ","_")}: u8 = {hex(num)};\n'
        )
    rust_file = open("inst.rs", "w")
    rust_file.write(
        f"""
/* Automatically generated by parse_opcodes */
{mask_match_str}
"""
    )
    rust_file.close()
