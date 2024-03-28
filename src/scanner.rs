use crate::token::*;


#[derive(Default)]
pub struct Scanner {
    start: usize,
    current: usize,
    line: i32,
    pub codes: String
}


fn is_digit(ch: u8) -> bool {
    return ch >= b'0' && ch <= b'9';
}

fn is_alpha(ch: u8) -> bool {
    return ch >= b'a' && ch <= b'z' ||
           ch >= b'A' && ch <= b'Z' ||
           ch == b'_';
}


impl Scanner {
    pub fn init(&mut self, codes: String) {
        self.start = 0;
        self.current = 0;
        self.line = 0;
        self.codes = codes;
    }

    #[inline]
    fn is_at_end(&self) -> bool {
        return self.current == self.codes.len();
    }

    fn make_token(&self, tokentype: TokenType) -> Token {
        return Token {
            ty: tokentype,
            start: self.start,
            length: self.current - self.start,
            line: self.line
        }
    }

    fn error_token(&self) -> Token {
        return Token {
            ty: TokenType::error,
            start: 0,
            length: 0,
            line: self.line
        }
    }

    fn advance(&mut self) -> u8 {
        self.current += 1;
        return self.codes.bytes().nth(self.current-1).unwrap_or(b'\0');
    }

    fn matched(&mut self, expected: u8) -> bool {
        if self.is_at_end() {
            return false;
        }
        if self.codes.bytes().nth(self.current).unwrap_or(b'\0') == expected {
            self.current += 1;
            return true;
        }
        return false;
    } 

    fn peek(&self) -> u8 {
        return self.codes.bytes().nth(self.current).unwrap_or(b'\0');
    }

    fn peek_next(&self) -> u8 {
        return self.codes.bytes().nth(self.current+1).unwrap_or(b'\0');
    }

    fn skip_whitespace(&mut self) {
        loop {
            let ch = self.peek();
            match ch {
                b' ' | b'\r' | b'\t' => {
                    self.advance();
                }
                b'\n' => {
                    self.line += 1;
                    self.advance();
                }
                b'/' => {
                    if self.peek_next() == b'/' {
                        while self.peek() != b'\n' && !self.is_at_end() {
                            self.advance();
                        }
                    } else {
                        return;
                    }
                }
                _ => return ,
            }
        }
    }

    fn string(&mut self) -> Token {
        while self.peek() != b'"' && !self.is_at_end() {
            if self.peek() == b'\n' {
                self.line += 1;
            }
            self.advance();
        } 

        if self.is_at_end() {
            return self.error_token();
        }

        self.advance();
        return self.make_token(TokenType::string);
    }

    fn number(&mut self) -> Token {
        while is_digit(self.peek()) {
            self.advance();
        }

        if self.peek() == b'.' && is_digit(self.peek_next()) {
            self.advance();
            while is_digit(self.peek()) {
                self.advance();
            }
        }

        return self.make_token(TokenType::number);
    }

    fn identifier_type(&mut self) -> TokenType {

        match &self.codes[self.start..self.current] {
            "and" => return TokenType::and,
            "class" => return TokenType::class,
            "else" => return TokenType::else_,
            "false" => return TokenType::false_,
            "fun" => return TokenType::fun,
            "for" => return TokenType::for_,
            "if" => return TokenType::if_,
            "nil" => return TokenType::nil,
            "or" => return TokenType::or,
            "print" => return TokenType::print,
            "return" => return TokenType::return_,
            "super" => return TokenType::super_,
            "this" => return TokenType::this,
            "true" => return TokenType::true_,
            "var" => return TokenType::var,
            "while" => return TokenType::while_,
            _ => return TokenType::identifier,
        }
    }

    fn identifier(&mut self) -> Token {
        while is_alpha(self.peek()) || is_digit(self.peek()) {
            self.advance();
        }
        let identifier_type = self.identifier_type();
        return self.make_token(identifier_type);
    }

    pub fn scan_token(&mut self) -> Token {

        self.skip_whitespace();
        self.start = self.current;
        if self.is_at_end() {
            return self.make_token(TokenType::eof);
        }   
        
        let ch = self.advance();

        if is_alpha(ch) {
            return self.identifier();
        }
        
        if is_digit(ch) {
            return self.number();
        }

        match ch {
            b'(' => return self.make_token(TokenType::left_paren),
            b')' => return self.make_token(TokenType::right_paren),
            b'{' => return self.make_token(TokenType::left_brace),
            b'}' => return self.make_token(TokenType::right_brace),
            b';' => return self.make_token(TokenType::semicolon),
            b',' => return self.make_token(TokenType::comma),
            b'.' => return self.make_token(TokenType::dot),
            b'-' => return self.make_token(TokenType::minus),
            b'+' => return self.make_token(TokenType::plus),
            b'/' => return self.make_token(TokenType::slash),
            b'*' => return self.make_token(TokenType::star),
            b'!' => {
                if self.matched(b'=') {
                    return  self.make_token(TokenType::bang_equal);
                } else {
                    return self.make_token(TokenType::bang);
                }
            },
            b'=' => {
                if self.matched(b'=') {
                    return  self.make_token(TokenType::equal_equal);
                } else {
                    return self.make_token(TokenType::equal);
                }
            },
            b'<' => {
                if self.matched(b'=') {
                    return  self.make_token(TokenType::less_equal);
                } else {
                    return self.make_token(TokenType::less);
                }
            },
            b'>' => {
                if self.matched(b'=') {
                    return  self.make_token(TokenType::greater_equal);
                } else {
                    return self.make_token(TokenType::greater);
                }
            }
            b'"' => return self.string(),
            _ => return self.error_token()
        }
        
    }
}