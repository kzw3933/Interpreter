#![allow(non_snake_case)]
// #![allow(non_camel_case_types)]

pub mod chunk;
pub mod value;
pub mod opcode;

use chunk::Chunk;
use opcode::OpCode;

fn main() {
    let mut chunk = Chunk::default();
    let constant = chunk.write_constant((1.2).into());
    chunk.write_code(OpCode::CONSTANT as u8, 123);
    chunk.write_code(constant as u8, 123);
    chunk.write_code(OpCode::RETURN as u8, 123);
    chunk.disassemble("test chunk");
    chunk.clear();
}