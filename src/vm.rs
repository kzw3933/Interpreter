use crate::chunk::Chunk;
use crate::opcode::OpCode;
use crate::value::Value;
use crate::define_const;

define_const!(DEBUG_TRACE_EXECUTION, true, bool);
define_const!(STACK_MAX, 256, usize);

pub enum Result {
    SUCCESS,
    CERROR,
    RERROR,
}


#[derive(Default)]

pub struct Vm {
    pub chunk: Chunk,
    stack: Vec<Value>,
    ip: usize,
}


impl Vm {

    pub fn default() -> Self {
        Self {
            chunk: Chunk::default(),
            stack: Vec::with_capacity(STACK_MAX),
            ip: 0,
        }
    }

    pub fn free(&mut self) {
        self.chunk.clear();
        self.stack.clear();
    }

    pub fn interpret(&mut self) -> Result {
        return self.run()
    }    

    #[inline]
    pub fn read_byte(&mut self) -> u8 {
        let inst = self.chunk.codes[self.ip];
        self.ip += 1;
        return inst;
    }

    #[inline]
    pub fn read_constant(&mut self) -> Value {
        let index = self.read_byte();
        return self.chunk.values[index as usize];
    }

    #[inline]
    pub fn trace_execute(&self) {
        print!("[ ");
        for value in &self.stack {
            print!(" ");
            value.print();
            print!(" ");
        }
        print!(" ]");
        print!("\n");
        self.chunk.disassemble_inst(self.ip);
    }


    pub fn run(&mut self) -> Result {
        loop {
            if self.ip >= self.chunk.codes.len() {
                return Result::SUCCESS;
            }

            if DEBUG_TRACE_EXECUTION {
                self.trace_execute();
            }

            let inst = self.read_byte();
            match inst.into() {
                OpCode::CONSTANT => {
                    let value = self.read_constant();
                    self.stack.push(value);
                },
                OpCode::NEGATE => {
                    let value = self.stack.pop().unwrap();
                    self.stack.push(-value);
                },
                OpCode::ADD => {
                    let rhs = self.stack.pop().unwrap();
                    let lhs = self.stack.pop().unwrap();
                    self.stack.push(lhs + rhs);
                },
                OpCode::SUBTRACT => {
                    let rhs = self.stack.pop().unwrap();
                    let lhs = self.stack.pop().unwrap();
                    self.stack.push(lhs - rhs);
                },
                OpCode::MULTIPLY => {
                    let rhs = self.stack.pop().unwrap();
                    let lhs = self.stack.pop().unwrap();
                    self.stack.push(lhs * rhs);
                },
                OpCode::DIVIDE => {
                    let rhs = self.stack.pop().unwrap();
                    let lhs = self.stack.pop().unwrap();
                    self.stack.push(lhs / rhs);
                },
                OpCode::RETURN => {
                    self.stack.pop()
                            .unwrap()
                            .print();
                }
            }
        }
    }

    pub fn clear_stack(&mut self) {
        self.stack.clear();
    }


}