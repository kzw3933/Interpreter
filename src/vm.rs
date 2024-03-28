use crate::chunk::Chunk;
use crate::opcode::OpCode;
use crate::value::Value;
use crate::compiler::Compiler;
use crate::define_const;

define_const!(DEBUG_TRACE_EXECUTION, true, bool);
define_const!(STACK_MAX, 256, usize);

pub enum Result {
    success,
    compile_error,
    runtime_error,
}


#[derive(Default)]

pub struct Vm {
    pub chunk: Chunk,
    stack: Vec<Value>,
    ip: usize,
    compiler: Compiler,
}


impl Vm {

    pub fn default() -> Self {
        Self {
            chunk: Chunk::default(),
            stack: Vec::with_capacity(STACK_MAX),
            ip: 0,
            compiler: Compiler::default(),
        }
    }

    pub fn interpret(&mut self, line: String) -> Result {
        self.compiler.compile(line);
        return Result::success;
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
                return Result::success;
            }

            if DEBUG_TRACE_EXECUTION {
                self.trace_execute();
            }

            let inst = self.read_byte();
            match inst.into() {
                OpCode::constant => {
                    let value = self.read_constant();
                    self.stack.push(value);
                },
                OpCode::neg => {
                    let value = self.stack.pop().unwrap();
                    self.stack.push(-value);
                },
                OpCode::add => {
                    let rhs = self.stack.pop().unwrap();
                    let lhs = self.stack.pop().unwrap();
                    self.stack.push(lhs + rhs);
                },
                OpCode::sub => {
                    let rhs = self.stack.pop().unwrap();
                    let lhs = self.stack.pop().unwrap();
                    self.stack.push(lhs - rhs);
                },
                OpCode::mul => {
                    let rhs = self.stack.pop().unwrap();
                    let lhs = self.stack.pop().unwrap();
                    self.stack.push(lhs * rhs);
                },
                OpCode::div => {
                    let rhs = self.stack.pop().unwrap();
                    let lhs = self.stack.pop().unwrap();
                    self.stack.push(lhs / rhs);
                },
                OpCode::ret => {
                    self.stack.pop()
                            .unwrap()
                            .print();
                }
            }
        }
    }

}