use crate::scanner::Scanner;
use crate::token::TokenType;

#[derive(Default)]
pub struct Compiler {
    scanner: Scanner,
}

impl Compiler {
    pub fn compile(&mut self, codes: String) {
        self.scanner.init(codes);
        let mut line = -1;
        loop {
            let token = self.scanner.scan_token();
            if token.line != line {
                print!("{:4} ", token.line);
                line = token.line;
            } else {
                print!("   | ");
            }
            println!("{:2} '{}'", token.ty as u8, &self.scanner.codes[token.start..token.start+token.length]);
            if token.ty == TokenType::eof {
                break;
            }
        }
    }
}