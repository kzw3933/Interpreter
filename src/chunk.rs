use crate::value::Value;
use crate::opcode::OpCode;



#[derive(Default)]
pub struct Chunk {
    pub codes: Vec<u8>,
    pub lines: Vec<u32>,
    pub values: Vec<Value>,
}


impl Chunk {

    pub fn write_codes(&mut self, codes: &[(u8, u32)]) {
        self.codes.extend(codes.iter().map(|(code, _)| *code));
        self.lines.extend(codes.iter().map(|(_, line)| *line));
    }

    pub fn write_code(&mut self, code: u8, line: u32) {
        self.codes.push(code);
        self.lines.push(line);
    }

    pub fn write_constant(&mut self, value: Value) -> usize{
        self.values.push(value);
        return self.values.len()-1;
    }

    pub fn disassemble(&self, name: &str) {
        println!("== {} ==", name);
        let mut offset: usize = 0;
        while  offset < self.codes.len() {
            offset = self.disassemble_inst(offset);
        }
    }

    pub fn disassemble_inst(&self, offset: usize) -> usize {
        print!("{:04} ", offset);
        if offset > 0 && self.lines[offset] == self.lines[offset-1] {
            print!("   | ")
        } else {
            print!("{:4} ", self.lines[offset]);
        }
        let inst = self.codes[offset];
        let inst: OpCode = inst.into();

        match inst {
            OpCode::constant => return self.constant_instruction(inst, offset),
            OpCode::neg => return self.simple_instruction(inst, offset),
            OpCode::add => return self.simple_instruction(inst, offset),
            OpCode::sub => return self.simple_instruction(inst, offset),
            OpCode::mul => return self.simple_instruction(inst, offset),
            OpCode::div => return self.simple_instruction(inst, offset),
            OpCode::ret => return self.simple_instruction(inst, offset),
            
        }
    }

    fn simple_instruction(&self, inst: OpCode, offset: usize) -> usize {
        println!("{:?}", inst);
        return offset + 1;
    }

    fn constant_instruction(&self, inst: OpCode, offset: usize) -> usize {
        let constant_index = self.codes[offset+1];
        print!("{:?}\t{:4} '", inst, constant_index);
        let value = &self.values[constant_index as usize];
        value.print();
        print!("'\n");
        return offset + 2;
    }

}