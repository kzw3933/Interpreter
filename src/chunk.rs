use crate::value::Value;
use crate::opcode::OpCode;



#[derive(Default)]
pub struct Chunk {
    pub codes: Vec<u8>,
    pub lines: Vec<u32>,
    pub values: Vec<Value>,
}


impl Chunk {
    pub fn clear(&mut self) {
        self.codes.clear();
        self.lines.clear();
        self.values.clear();
    }

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
            OpCode::CONSTANT => return self.constant_instruction(inst, offset),
            OpCode::NEGATE => return self.simple_instruction(inst, offset),
            OpCode::ADD => return self.simple_instruction(inst, offset),
            OpCode::SUBTRACT => return self.simple_instruction(inst, offset),
            OpCode::MULTIPLY => return self.simple_instruction(inst, offset),
            OpCode::DIVIDE => return self.simple_instruction(inst, offset),
            OpCode::RETURN => return self.simple_instruction(inst, offset),
            
        }
    }

    fn simple_instruction(&self, inst: OpCode, offset: usize) -> usize {
        println!("{:?}", inst);
        return offset + 1;
    }

    fn constant_instruction(&self, inst: OpCode, offset: usize) -> usize {
        let constant = self.codes[offset+1];
        print!("{:?}\t{:4} '", inst, constant);
        let value = &self.values[constant as usize];
        value.print();
        print!("'\n");
        return offset + 2;
    }

}