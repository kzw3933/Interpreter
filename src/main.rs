#![allow(non_snake_case)]
// #![allow(non_camel_case_types)]

pub mod chunk;
pub mod value;
pub mod opcode;
pub mod macros;
pub mod vm;

use opcode::OpCode;
use vm::Vm;

fn main() {
    let mut vm = Vm::default();
    let constant1 = vm.chunk.write_constant((1.2).into());
    let constant2 = vm.chunk.write_constant((3.4).into());
    let constant3 = vm.chunk.write_constant((5.6).into());
    vm.chunk.write_codes(&[
        (OpCode::CONSTANT as u8, 123),
        (constant1 as u8, 123),

        (OpCode::CONSTANT as u8, 123),
        (constant2 as u8, 123),

        (OpCode::ADD as u8, 123),

        (OpCode::CONSTANT as u8, 123),
        (constant3 as u8, 123),

        (OpCode::DIVIDE as u8, 123),
        (OpCode::NEGATE as u8, 123),

        (OpCode::RETURN as u8, 123)
    ]);
    vm.interpret();
    vm.free();
}