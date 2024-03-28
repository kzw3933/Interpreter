#![allow(non_snake_case)]
#![allow(non_camel_case_types)]

pub mod chunk;
pub mod value;
pub mod opcode;
pub mod macros;
pub mod vm;
pub mod compiler;
pub mod scanner;
pub mod token;

use vm::Vm;

use std::io::prelude::*;

fn main() {
    let vm = Vm::default();
    let args: Vec<String> = std::env::args().collect();
    if args.len() == 1 {
        run_repl(vm);
    } else if args.len() == 2 {
        run_file(vm, &args[1]);
    } else {
        println!("Usage: rlox [path]");
    }
} 

fn run_repl(mut vm: Vm) {
    let stdin = std::io::stdin();
    let mut stdout = std::io::stdout();
    println!("=== rlox repl (type `exit()` to quit)=== ");
    loop {
        let mut line = String::new();
        print!("> ");
        stdout.flush().unwrap();

        stdin.read_line(&mut line)
             .expect("Failed to read line");

        if line.trim() == "exit()" {
            break;
        }
        
        vm.interpret(line);
    }

}

fn run_file(mut vm: Vm, path: &str) {
     let codes = std::fs::read_to_string(path).unwrap();
     vm.interpret(codes);
}